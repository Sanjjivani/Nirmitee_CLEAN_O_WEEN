from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, CleanupActivity, init_db, login_manager
from config import Config
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, folder):
    """Save uploaded file with unique filename"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        
        # Ensure directory exists
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folder), exist_ok=True)
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, unique_filename)
        file.save(file_path)
        
        return unique_filename
    return None

# Authentication Routes
@app.route('/')
def index():
    """Redirect to login page as home"""
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation checks
        if not all([name, email, password, confirm_password]):
            flash('All fields are required!', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('signup.html')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered! Please use a different email.', 'error')
            return render_template('signup.html')
        
        # Create new user
        try:
            new_user = User(name=name, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            print(f"Error: {e}")
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([email, password]):
            flash('Please fill in all fields!', 'error')
            return render_template('login.html')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('login'))

# Dashboard Routes
@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard overview"""
    try:
        # Get user statistics
        total_points = current_user.points
        user_rank = current_user.get_rank()
        total_cleanups = current_user.total_cleanups
        total_waste = current_user.total_waste
        
        # Get recent activities (ordered properly)
        recent_cleanups = CleanupActivity.query.filter_by(user_id=current_user.id)\
            .order_by(CleanupActivity.created_at.desc()).limit(3).all()
        
        # Motivational messages based on activity
        motivational_messages = [
            "Every cleanup makes our planet greener! 🌍",
            "Keep up the great work! Your efforts matter. 💚",
            "Small actions lead to big changes. Continue your journey! 🌱",
            "You're making a difference one cleanup at a time! ✨",
            "The Earth thanks you for your dedication! 🍃"
        ]
        
        # Select message based on user's activity level
        if total_cleanups == 0:
            message = "Start your first cleanup and begin your eco-journey! 🚀"
        elif total_cleanups < 5:
            message = motivational_messages[0]
        elif total_cleanups < 10:
            message = motivational_messages[1]
        else:
            message = motivational_messages[2]
        
        return render_template(
            'dashboard.html',
            user=current_user,
            total_points=total_points,
            user_rank=user_rank,
            total_cleanups=total_cleanups,
            total_waste=total_waste,
            recent_cleanups=recent_cleanups,
            motivational_message=message
        )
        
    except Exception as e:
        print(f"Dashboard error: {e}")
        flash('Error loading dashboard data.', 'error')
        return render_template('dashboard.html', user=current_user)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    try:
        # Get recent cleanups ordered properly in the route
        recent_cleanups = CleanupActivity.query.filter_by(user_id=current_user.id)\
            .order_by(CleanupActivity.created_at.desc()).limit(5).all()
        
        return render_template('profile.html', 
                             user=current_user, 
                             recent_cleanups=recent_cleanups)
    except Exception as e:
        print(f"Profile error: {e}")
        flash('Error loading profile data.', 'error')
        return render_template('profile.html', user=current_user)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Upload cleanup photos page"""
    if request.method == 'POST':
        try:
            # Get form data
            location = request.form.get('location', '').strip()
            waste_collected = request.form.get('waste_collected', '').strip()
            waste_kg = float(request.form.get('waste_kg', 0))
            
            # Get uploaded files
            before_photo = request.files.get('before_photo')
            after_photo = request.files.get('after_photo')
            
            # Validate required fields
            if not all([location, waste_collected, before_photo, after_photo]):
                flash('Please fill all required fields and upload both images!', 'error')
                return render_template('upload.html')
            
            if waste_kg <= 0:
                flash('Please enter a valid waste amount (greater than 0).', 'error')
                return render_template('upload.html')
            
            # Save uploaded files
            before_filename = save_uploaded_file(before_photo, 'before')
            after_filename = save_uploaded_file(after_photo, 'after')
            
            if not before_filename or not after_filename:
                flash('Invalid file type. Please upload images only (PNG, JPG, JPEG, GIF).', 'error')
                return render_template('upload.html')
            
            # Create cleanup activity
            new_cleanup = CleanupActivity(
                user_id=current_user.id,
                location=location,
                waste_collected=waste_collected,
                waste_kg=waste_kg,
                before_photo=before_filename,
                after_photo=after_filename
            )
            
            # Calculate and assign points
            points_earned = new_cleanup.calculate_points()
            new_cleanup.points_earned = points_earned
            
            # Update user stats
            current_user.add_points(points_earned)
            current_user.add_cleanup_stats(waste_kg)
            
            # Save to database
            db.session.add(new_cleanup)
            db.session.commit()
            
            flash(f'Cleanup submitted successfully! You earned {points_earned} points! 🌟', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Upload error: {e}")
            flash('Error submitting cleanup. Please try again.', 'error')
    
    return render_template('upload.html')

@app.route('/leaderboard')
@login_required
def leaderboard():
    """Community leaderboard page"""
    try:
        # Get all users ordered by points
        users = User.query.order_by(User.points.desc()).all()
        user_rank = current_user.get_rank()
        
        return render_template(
            'leaderboard.html',
            users=users,
            user_rank=user_rank,
            user=current_user
        )
    except Exception as e:
        print(f"Leaderboard error: {e}")
        flash('Error loading leaderboard.', 'error')
        return render_template('leaderboard.html', users=[], user=current_user)

@app.route('/charts')
@login_required
def charts():
    """Progress charts page"""
    try:
        # Get chart data
        weekly_data = get_weekly_activity_data(current_user.id)
        monthly_data = get_monthly_activity_data(current_user.id)
        
        return render_template(
            'charts.html',
            user=current_user,
            weekly_data=weekly_data,
            monthly_data=monthly_data
        )
    except Exception as e:
        print(f"Charts error: {e}")
        flash('Error loading charts.', 'error')
        return render_template('charts.html', user=current_user)

@app.route('/uploads/<folder>/<filename>')
@login_required
def uploaded_file(folder, filename):
    """Serve uploaded files"""
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename)

# Helper Functions
def get_weekly_activity_data(user_id):
    """Generate weekly activity data for charts"""
    try:
        dates = []
        activity_counts = []
        
        for i in range(6, -1, -1):
            date = (datetime.utcnow() - timedelta(days=i)).date()
            dates.append(date.strftime('%a'))
            
            day_start = datetime.combine(date, datetime.min.time())
            day_end = datetime.combine(date, datetime.max.time())
            
            day_activities = CleanupActivity.query.filter(
                CleanupActivity.user_id == user_id,
                CleanupActivity.created_at >= day_start,
                CleanupActivity.created_at <= day_end
            ).count()
            
            activity_counts.append(day_activities)
        
        return {
            'dates': dates,
            'activity_counts': activity_counts
        }
    except Exception as e:
        print(f"Weekly data error: {e}")
        return {'dates': [], 'activity_counts': []}

def get_monthly_activity_data(user_id):
    """Generate monthly activity data"""
    try:
        months = []
        cleanups = []
        waste_collected = []
        
        for i in range(5, -1, -1):
            month_start = (datetime.utcnow().replace(day=1) - timedelta(days=30*i))
            month_name = month_start.strftime('%b')
            months.append(month_name)
            
            month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            month_activities = CleanupActivity.query.filter(
                CleanupActivity.user_id == user_id,
                CleanupActivity.created_at >= month_start,
                CleanupActivity.created_at <= month_end
            ).all()
            
            cleanups.append(len(month_activities))
            waste_collected.append(sum(activity.waste_kg for activity in month_activities))
        
        return {
            'months': months, 
            'cleanups': cleanups,
            'waste_collected': waste_collected
        }
    except Exception as e:
        print(f"Monthly data error: {e}")
        return {'months': [], 'cleanups': [], 'waste_collected': []}

# Initialize database when app starts
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
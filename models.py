from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from datetime import datetime
import os

db = SQLAlchemy()
login_manager = LoginManager()

class User(UserMixin, db.Model):
    """
    User model for storing user authentication and profile details
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    total_cleanups = db.Column(db.Integer, default=0, nullable=False)
    total_waste = db.Column(db.Float, default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with cleanup activities
    cleanups = db.relationship('CleanupActivity', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password securely using werkzeug"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify hashed password"""
        return check_password_hash(self.password, password)
    
    def add_points(self, points):
        """Add points to user's total"""
        self.points += points
        db.session.commit()
    
    def add_cleanup_stats(self, waste_kg):
        """Update user's cleanup statistics"""
        self.total_cleanups += 1
        self.total_waste += waste_kg
        db.session.commit()
    
    def get_rank(self):
        """Get user's rank based on points"""
        rank = User.query.filter(User.points > self.points).count() + 1
        return rank
    
    def __repr__(self):
        return f'<User {self.email}>'

class CleanupActivity(db.Model):
    """
    Model for storing user cleanup activities with before/after photos
    """
    __tablename__ = 'cleanup_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    waste_collected = db.Column(db.String(100), nullable=False)
    waste_kg = db.Column(db.Float, default=0.0, nullable=False)
    before_photo = db.Column(db.String(500), nullable=False)
    after_photo = db.Column(db.String(500), nullable=False)
    points_earned = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def calculate_points(self):
        """Calculate points based on waste collected"""
        base_points = 10  # Base points for any cleanup
        return base_points

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login session management"""
    return User.query.get(int(user_id))

def init_db():
    """Initialize database with sample data"""
    try:
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create upload directories
        os.makedirs('static/uploads/before', exist_ok=True)
        os.makedirs('static/uploads/after', exist_ok=True)
        
        # Create sample user if no users exist
        if not User.query.first():
            sample_user = User(
                name="Eco Warrior",
                email="eco@example.com",
                points=150,
                total_cleanups=3,
                total_waste=5.5
            )
            sample_user.set_password("password123")
            db.session.add(sample_user)
            
            db.session.commit()
            print(" Sample data added successfully!")
            
    except Exception as e:
        print(f" Database initialization error: {e}")
        db.session.rollback()
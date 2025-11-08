 🌍 CleanEarth - Campus Cleanup Platform

🚨 Problem Statement

 The Campus Garbage Crisis
Educational campuses across India face a severe garbage management challenge. Despite cleanup efforts, the impact remains invisible and unmeasured, leading to:

- **Permanent garbage spots** reappearing without monitoring
- **Low student participation** in cleanup drives due to lack of motivation  
- **No visual proof** of environmental impact demotivating volunteers
- **Inefficient resource allocation** by campus administration
- **Lost campus pride** as public spaces remain littered

### The Impact
Students feel their efforts go unnoticed, while campus administrators lack data-driven insights for effective cleanup planning and resource allocation.

---

## 💡 Our Solution

**CleanEarth** transforms campus cleanup from a chore into an engaging mission through visual verification and gamification.

### 🎯 Core Features

#### 📸 Visual Proof System
- **Before/After Photo Documentation** with GPS tagging
- **Timeline Validation** ensuring authentic cleanup sequences
- **Real-time Impact Tracking**

#### 🎮 Gamification Engine  
- **Points & Badges** for cleanup activities
- **Campus Leaderboards** fostering healthy competition
- **Achievement System** with milestones and recognition

#### 📊 Live Campus Dashboard
- **Interactive Maps** showing cleaned areas across campus
- **Progress Analytics** with real-time statistics
- **Administrative Insights** for better resource planning

#### 🤖 AI-Powered Verification
- **RunAnywhere SDK Integration** for image analysis
- **Automated Cleanup Validation**
- **Fraud Detection** preventing fake submissions

---

## 🛠️ Technology Stack

### Backend
- **Python Flask** - Web framework
- **SQLAlchemy** - Database ORM  
- **MySQL** - Database management
- **Flask-Login** - Authentication system

### Frontend
- **HTML5/CSS3/JavaScript** - Frontend technologies
- **Bootstrap 5** - UI framework
- **Jinja2 Templates** - Server-side rendering

### Mobile
- **Android Kotlin** - Mobile application
- **WebView** - Web app integration
- **RunAnywhere SDK** - AI capabilities

---

## 📁 Project Structure

### 1. Web Application Files
```
CleanEarth-Platform/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── script.js     # Client-side JavaScript
└── templates/
    ├── base.html         # Base template
    ├── dashboard.html    # User dashboard
    ├── login.html        # Login page
    ├── signup.html       # Registration page
    ├── upload.html       # Photo upload interface
    ├── leaderboard.html  # Rankings display
    ├── charts.html       # Analytics charts
    └── profile.html      # User profile page
```

### 2. Android Application Files
```
CleanEarth-Android/
├── app/
│   ├── src/main/
│   │   ├── java/com/cleanearth/app/
│   │   │   └── MainActivity.kt    # Main Android activity
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   └── activity_main.xml  # App layout
│   │   │   └── values/
│   │   │       └── strings.xml        # String resources
│   │   └── AndroidManifest.xml        # App configuration
│   └── build.gradle                   # App-level build config
├── build.gradle                       # Project-level build config
└── README.md                          # Android setup guide
```

---

## 🚀 Quick Start

### Web Platform Setup
```bash
cd CleanEarth-Platform
pip install -r requirements.txt
python app.py
```
Access: http://localhost:5000

### Android App Setup
1. Open `CleanEarth-Android` in Android Studio
2. Update `WEBSITE_URL` in `MainActivity.kt`
3. Build and run on device/emulator

---

## 🎯 Impact & Vision

**CleanEarth** aims to create cleaner, greener campuses by making environmental responsibility engaging, measurable, and socially rewarding. By combining visual proof with gamification, we're building a sustainable culture of campus cleanliness where every student's effort counts and becomes part of a larger, visible impact.

*Join us in transforming campus cleanup from invisible chore to celebrated achievement!* 🌱

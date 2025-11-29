from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, g
import sqlite3
import bcrypt
from datetime import datetime
import os
import sys

# Thêm thư mục gốc vào path để import config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.config import Config

# Risk Matrix Configuration (định nghĩa trực tiếp để tránh lỗi import)
RISK_MATRIX = {
    'rare': {'insignificant': 1, 'minor': 2, 'moderate': 3, 'major': 4, 'catastrophic': 5},
    'unlikely': {'insignificant': 2, 'minor': 4, 'moderate': 6, 'major': 8, 'catastrophic': 10},
    'possible': {'insignificant': 3, 'minor': 6, 'moderate': 9, 'major': 12, 'catastrophic': 15},
    'likely': {'insignificant': 4, 'minor': 8, 'moderate': 12, 'major': 16, 'catastrophic': 20},
    'almost_certain': {'insignificant': 5, 'minor': 10, 'moderate': 15, 'major': 20, 'catastrophic': 25}
}

RISK_LEVELS = {
    (1, 4): 'Thấp',
    (5, 9): 'Trung bình', 
    (10, 16): 'Cao',
    (17, 25): 'Rất cao'
}

def format_sqlite_date(date_string):
    """Format SQLite date string to DD/MM/YYYY"""
    if date_string and len(date_string) >= 10:
        return f"{date_string[8:10]}/{date_string[5:7]}/{date_string[0:4]}"
    return date_string

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

def get_db():
    """Kết nối đến SQLite database"""
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Đóng kết nối database"""
    if hasattr(g, 'db'):
        g.db.close()

def calculate_risk_level(score):
    for range_val, level in RISK_LEVELS.items():
        if range_val[0] <= score <= range_val[1]:
            return level
    return 'Không xác định'

def log_activity(user_id, activity_type, description, ip_address=None, user_agent=None):
    try:
        db = get_db()
        db.execute("""
            INSERT INTO activity_logs (user_id, activity_type, description, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, activity_type, description, ip_address, user_agent))
        db.commit()
    except Exception as e:
        print(f"Logging error: {e}")

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute(
            "SELECT * FROM employees WHERE username = ? AND is_active = 1", 
            (username,)
        ).fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            
            # Update last login
            db.execute("UPDATE employees SET last_login = datetime('now') WHERE id = ?", (user['id'],))
            db.commit()
            
            # Log activity
            log_activity(user['id'], 'login', 'User logged in')
            
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_activity(session['user_id'], 'logout', 'User logged out')
    session.clear()
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    
    # Thống kê tổng quan
    total_assets = db.execute("SELECT COUNT(*) as total_assets FROM information_assets").fetchone()[0]
    total_risks = db.execute("SELECT COUNT(*) as total_risks FROM risk_assessments").fetchone()[0]
    open_incidents = db.execute("SELECT COUNT(*) as open_incidents FROM security_incidents WHERE status != 'closed'").fetchone()[0]
    total_checks = db.execute("SELECT COUNT(*) as total_checks FROM security_checks").fetchone()[0]
    
    # Phân bố mức độ rủi ro
    risk_distribution = db.execute("""
        SELECT risk_level, COUNT(*) as count 
        FROM risk_assessments 
        GROUP BY risk_level
    """).fetchall()
    
    # Sự cố gần đây
    recent_incidents = db.execute("""
        SELECT si.*, e1.full_name as reported_by_name
        FROM security_incidents si
        LEFT JOIN employees e1 ON si.reported_by = e1.id
        ORDER BY si.created_at DESC LIMIT 5
    """).fetchall()
    
    # Kiểm tra gần đây - Format dates
    recent_checks_data = db.execute("""
        SELECT cr.*, sc.check_name, e.full_name as checked_by_name
        FROM check_results cr
        JOIN security_checks sc ON cr.check_id = sc.id
        JOIN employees e ON cr.checked_by = e.id
        ORDER BY cr.check_date DESC LIMIT 5
    """).fetchall()
    
    # Format dates for template
    recent_checks = []
    for check in recent_checks_data:
        check_dict = dict(check)
        if check_dict['check_date']:
            check_dict['formatted_date'] = format_sqlite_date(check_dict['check_date'])
        recent_checks.append(check_dict)
    
    return render_template('dashboard.html', 
                         total_assets=total_assets,
                         total_risks=total_risks,
                         open_incidents=open_incidents,
                         total_checks=total_checks,
                         risk_distribution=risk_distribution,
                         recent_incidents=recent_incidents,
                         recent_checks=recent_checks)

@app.route('/risk-matrix')
def risk_matrix():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    risks = db.execute("""
        SELECT ra.*, ia.asset_name, ia.asset_type
        FROM risk_assessments ra 
        JOIN information_assets ia ON ra.asset_id = ia.id
        ORDER BY ra.risk_score DESC
    """).fetchall()
    
    return render_template('risk_matrix.html', risks=risks, RISK_MATRIX=RISK_MATRIX)

@app.route('/add-risk', methods=['GET', 'POST'])
def add_risk():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        asset_id = request.form['asset_id']
        threat_description = request.form['threat_description']
        vulnerability_description = request.form['vulnerability_description']
        likelihood = request.form['likelihood']
        impact = request.form['impact']
        existing_controls = request.form['existing_controls']
        
        # Calculate risk score and level
        risk_score = RISK_MATRIX[likelihood][impact]
        risk_level = 'extreme' if risk_score >= 17 else 'high' if risk_score >= 10 else 'medium' if risk_score >= 5 else 'low'
        
        db = get_db()
        db.execute("""
            INSERT INTO risk_assessments 
            (asset_id, threat_description, vulnerability_description, likelihood, impact, 
             risk_score, risk_level, existing_controls, assessed_by, assessment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
        """, (asset_id, threat_description, vulnerability_description, likelihood, impact,
              risk_score, risk_level, existing_controls, session['user_id']))
        
        db.commit()
        log_activity(session['user_id'], 'risk_assessment', 'Added new risk assessment')
        
        flash('Đánh giá rủi ro đã được thêm thành công!', 'success')
        return redirect(url_for('risk_matrix'))
    
    # Get assets for dropdown
    db = get_db()
    assets = db.execute("SELECT id, asset_name FROM information_assets").fetchall()
    
    return render_template('add_risk.html', assets=assets)

@app.route('/security-checks')
def security_checks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    checks_data = db.execute("""
        SELECT sc.*, 
               (SELECT status FROM check_results WHERE check_id = sc.id ORDER BY check_date DESC LIMIT 1) as last_status,
               (SELECT check_date FROM check_results WHERE check_id = sc.id ORDER BY check_date DESC LIMIT 1) as last_check,
               (SELECT notes FROM check_results WHERE check_id = sc.id ORDER BY check_date DESC LIMIT 1) as last_notes
        FROM security_checks sc
        ORDER BY sc.category, sc.check_name
    """).fetchall()
    
    # Format dates for template
    checks = []
    for check in checks_data:
        check_dict = dict(check)
        if check_dict['last_check']:
            check_dict['formatted_last_check'] = format_sqlite_date(check_dict['last_check'])
        checks.append(check_dict)
    
    return render_template('security_checks.html', checks=checks)

@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    db = get_db()
    
    # Risk levels count
    risk_levels_data = db.execute("SELECT risk_level, COUNT(*) as count FROM risk_assessments GROUP BY risk_level").fetchall()
    risk_levels = {row['risk_level']: row['count'] for row in risk_levels_data}
    
    # Check results
    check_results_data = db.execute("SELECT status, COUNT(*) as count FROM check_results GROUP BY status").fetchall()
    check_results = {row['status']: row['count'] for row in check_results_data}
    
    return jsonify({
        'risk_levels': risk_levels,
        'check_results': check_results
    })

if __name__ == '__main__':
    # Đảm bảo database tồn tại
    if not os.path.exists(Config.DATABASE_PATH):
        print("⚠️ Database not found. Please run 'python database.py' first.")
        print("🚀 Creating database now...")
        from database import init_database
        init_database()
    
    print("🌐 Starting Cricket Security System...")
    print("📍 Access at: http://localhost:5000")
    print("🔑 Default login: admin / admin123")
    app.run(debug=True, host='0.0.0.0', port=5000)
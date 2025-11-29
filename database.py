import sqlite3
import bcrypt
import os
import sys

# Thêm thư mục gốc vào path để import config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.config import Config

# Risk Matrix Configuration (định nghĩa trực tiếp trong file này)
RISK_MATRIX = {
    'rare': {'insignificant': 1, 'minor': 2, 'moderate': 3, 'major': 4, 'catastrophic': 5},
    'unlikely': {'insignificant': 2, 'minor': 4, 'moderate': 6, 'major': 8, 'catastrophic': 10},
    'possible': {'insignificant': 3, 'minor': 6, 'moderate': 9, 'major': 12, 'catastrophic': 15},
    'likely': {'insignificant': 4, 'minor': 8, 'moderate': 12, 'major': 16, 'catastrophic': 20},
    'almost_certain': {'insignificant': 5, 'minor': 10, 'moderate': 15, 'major': 20, 'catastrophic': 25}
}

def init_database():
    """Khởi tạo database SQLite"""
    try:
        # Xóa database cũ nếu tồn tại
        if os.path.exists(Config.DATABASE_PATH):
            os.remove(Config.DATABASE_PATH)
            print("🗑️ Old database removed")
        
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("📁 Creating new database...")
        
        # Đọc và thực thi schema
        with open('database_schema.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Thực thi từng câu lệnh SQL
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"⚠️ Statement error (ignored): {e}")
        
        print("✅ Database schema created successfully!")
        
        # Chèn dữ liệu mẫu
        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Nhân viên mẫu
        employees_data = [
            ('admin', password_hash, 'Admin', 'admin@cricket.com', 'admin', 'IT'),
            ('manager', password_hash, 'Quản Lý', 'manager@cricket.com', 'manager', 'Quản lý'),
            ('staff1', password_hash, 'Nhân Viên', 'staff1@cricket.com', 'staff', 'Vận hành'),
            ('staff2', password_hash, 'Vận Hành', 'staff2@cricket.com', 'staff', 'Vận hành')
        ]
        
        for emp in employees_data:
            cursor.execute("""
                INSERT INTO employees (username, password_hash, full_name, email, role, department)
                VALUES (?, ?, ?, ?, ?, ?)
            """, emp)
        
        print("✅ Sample employees added!")
        
        # Tài sản thông tin mẫu
        assets_data = [
            ('Tài khoản Admin Shopee', 'account', 'Tài khoản quản trị gian hàng Shopee chính', 1, 'critical', 'critical', 'high'),
            ('Database khách hàng', 'data', 'Thông tin khách hàng từ đơn hàng Shopee', 1, 'high', 'high', 'medium'),
            ('Tài khoản ngân hàng Vietcombank', 'financial', 'Tài khoản kết nối ngân hàng với Shopee', 2, 'critical', 'critical', 'medium'),
            ('Hệ thống Sapo', 'system', 'Hệ thống quản lý bán hàng Sapo', 1, 'high', 'high', 'high'),
            ('Google Drive nội bộ', 'data', 'Lưu trữ dữ liệu kinh doanh nội bộ', 2, 'medium', 'high', 'medium'),
            ('Tài khoản Facebook Business', 'account', 'Tài khoản quảng cáo và fanpage', 1, 'high', 'medium', 'low')
        ]
        
        for asset in assets_data:
            cursor.execute("""
                INSERT INTO information_assets 
                (asset_name, asset_type, description, owner_id, confidentiality_level, integrity_level, availability_level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, asset)
        
        print("✅ Sample assets added!")
        
        # Kiểm tra bảo mật mẫu
        checks_data = [
            ('Xác thực 2FA Shopee', 'Kiểm tra xác thực 2 yếu tố cho tài khoản Shopee', 'account', 1, 'monthly'),
            ('Chính sách mật khẩu', 'Kiểm tra mật khẩu mạnh và thay đổi định kỳ', 'account', 1, 'monthly'),
            ('Phân quyền truy cập', 'Kiểm tra phân quyền nhân viên theo RBAC', 'account', 1, 'quarterly'),
            ('Sao lưu dữ liệu', 'Kiểm tra quy trình sao lưu dữ liệu khách hàng', 'data', 1, 'weekly'),
            ('Phần mềm diệt virus', 'Kiểm tra cập nhật phần mềm diệt virus', 'system', 1, 'daily'),
            ('Kiểm tra session', 'Đảm bảo đăng xuất khi không sử dụng', 'account', 1, 'daily'),
            ('Mã hóa dữ liệu', 'Kiểm tra mã hóa dữ liệu nhạy cảm', 'data', 1, 'monthly'),
            ('Đào tạo nhận thức', 'Kiểm tra đào tạo nhận thức bảo mật', 'process', 1, 'quarterly')
        ]
        
        for check in checks_data:
            cursor.execute("""
                INSERT INTO security_checks (check_name, description, category, is_required, frequency)
                VALUES (?, ?, ?, ?, ?)
            """, check)
        
        print("✅ Security checks added!")
        
        # Đánh giá rủi ro mẫu
        risk_assessments_data = [
            (1, 'Tấn công phishing chiếm đoạt tài khoản', 'Nhân viên không được đào tạo nhận diện phishing', 'possible', 'catastrophic', 'Sử dụng 2FA, đào tạo nhận thức'),
            (2, 'Rò rỉ dữ liệu khách hàng', 'Dữ liệu không được mã hóa khi lưu trữ', 'likely', 'major', 'Mã hóa database, phân quyền truy cập'),
            (3, 'Mất quyền kiểm soát tài chính', 'Kết nối API ngân hàng không an toàn', 'unlikely', 'catastrophic', 'Xác thực 2FA, giám sát giao dịch'),
            (4, 'Đồng bộ dữ liệu thất bại', 'Lỗi kết nối giữa Shopee và Sapo', 'likely', 'moderate', 'Monitoring, backup manual'),
            (5, 'Mã độc tống tiền', 'Nhân viên tải file đính kèm độc hại', 'possible', 'major', 'Antivirus, đào tạo nhận thức')
        ]
        
        for risk in risk_assessments_data:
            asset_id, threat, vulnerability, likelihood, impact, controls = risk
            risk_score = RISK_MATRIX[likelihood][impact]
            risk_level = 'extreme' if risk_score >= 17 else 'high' if risk_score >= 10 else 'medium' if risk_score >= 5 else 'low'
            
            cursor.execute("""
                INSERT INTO risk_assessments 
                (asset_id, threat_description, vulnerability_description, likelihood, impact, 
                 risk_score, risk_level, existing_controls, assessed_by, assessment_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
            """, (asset_id, threat, vulnerability, likelihood, impact, risk_score, risk_level, controls, 1))
        
        print("✅ Sample risk assessments added!")
        
        # Kết quả kiểm tra mẫu
        check_results_data = [
            (1, 1, '2024-01-15', 'passed', '2FA đã được kích hoạt'),
            (2, 1, '2024-01-10', 'failed', 'Mật khẩu yếu được phát hiện'),
            (3, 2, '2024-01-05', 'passed', 'Phân quyền hợp lý'),
            (4, 1, '2024-01-18', 'passed', 'Sao lưu thành công'),
            (5, 3, '2024-01-19', 'passed', 'Antivirus đã cập nhật')
        ]
        
        for result in check_results_data:
            cursor.execute("""
                INSERT INTO check_results (check_id, checked_by, check_date, status, notes)
                VALUES (?, ?, ?, ?, ?)
            """, result)
        
        print("✅ Sample check results added!")
        
        conn.commit()
        print("🎉 Database initialization completed successfully!")
        print(f"📊 Database created at: {Config.DATABASE_PATH}")
        
        # Hiển thị thống kê
        print("\n📈 Database Statistics:")
        print(f"   👥 Employees: {cursor.execute('SELECT COUNT(*) FROM employees').fetchone()[0]}")
        print(f"   💼 Assets: {cursor.execute('SELECT COUNT(*) FROM information_assets').fetchone()[0]}")
        print(f"   ⚠️ Risks: {cursor.execute('SELECT COUNT(*) FROM risk_assessments').fetchone()[0]}")
        print(f"   ✅ Checks: {cursor.execute('SELECT COUNT(*) FROM security_checks').fetchone()[0]}")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    init_database()
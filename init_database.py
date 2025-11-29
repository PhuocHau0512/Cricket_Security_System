import mysql.connector
import bcrypt
from config.config import Config

def init_database():
    try:
        # Kết nối MySQL (chưa chọn database)
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        
        # Tạo database
        cursor.execute("CREATE DATABASE IF NOT EXISTS Cricket_Security")
        cursor.execute("USE Cricket_Security")
        print("✅ Database created successfully!")
        
        # Đọc và thực thi schema
        with open('database_schema.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Thực thi từng câu lệnh SQL
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        
        print("✅ Tables created successfully!")
        
        # Chèn dữ liệu mẫu
        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Nhân viên mẫu
        employees_data = [
            ('admin', password_hash, 'Nguyễn Văn Admin', 'admin@cricket.com', 'admin', 'IT'),
            ('manager', password_hash, 'Trần Quản Lý', 'manager@cricket.com', 'manager', 'Quản lý'),
            ('staff1', password_hash, 'Lê Thị Nhân Viên', 'staff1@cricket.com', 'staff', 'Vận hành'),
            ('staff2', password_hash, 'Phạm Văn Vận Hành', 'staff2@cricket.com', 'staff', 'Vận hành')
        ]
        
        for emp in employees_data:
            cursor.execute("""
                INSERT INTO employees (username, password_hash, full_name, email, role, department)
                VALUES (%s, %s, %s, %s, %s, %s)
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
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, asset)
        
        print("✅ Sample assets added!")
        
        # Kiểm tra bảo mật mẫu
        checks_data = [
            ('Xác thực 2FA Shopee', 'Kiểm tra xác thực 2 yếu tố cho tài khoản Shopee', 'account', True, 'monthly'),
            ('Chính sách mật khẩu', 'Kiểm tra mật khẩu mạnh và thay đổi định kỳ', 'account', True, 'monthly'),
            ('Phân quyền truy cập', 'Kiểm tra phân quyền nhân viên theo RBAC', 'account', True, 'quarterly'),
            ('Sao lưu dữ liệu', 'Kiểm tra quy trình sao lưu dữ liệu khách hàng', 'data', True, 'weekly'),
            ('Phần mềm diệt virus', 'Kiểm tra cập nhật phần mềm diệt virus', 'system', True, 'daily'),
            ('Kiểm tra session', 'Đảm bảo đăng xuất khi không sử dụng', 'account', True, 'daily'),
            ('Mã hóa dữ liệu', 'Kiểm tra mã hóa dữ liệu nhạy cảm', 'data', True, 'monthly'),
            ('Đào tạo nhận thức', 'Kiểm tra đào tạo nhận thức bảo mật', 'process', True, 'quarterly')
        ]
        
        for check in checks_data:
            cursor.execute("""
                INSERT INTO security_checks (check_name, description, category, is_required, frequency)
                VALUES (%s, %s, %s, %s, %s)
            """, check)
        
        print("✅ Security checks added!")
        
        # Đánh giá rủi ro mẫu - Sửa impact levels để khớp với RISK_MATRIX
        risk_assessments_data = [
            (1, 'Tấn công phishing chiếm đoạt tài khoản', 'Nhân viên không được đào tạo nhận diện phishing', 'possible', 'catastrophic', 'Sử dụng 2FA, đào tạo nhận thức'),
            (2, 'Rò rỉ dữ liệu khách hàng', 'Dữ liệu không được mã hóa khi lưu trữ', 'likely', 'major', 'Mã hóa database, phân quyền truy cập'),
            (3, 'Mất quyền kiểm soát tài chính', 'Kết nối API ngân hàng không an toàn', 'unlikely', 'catastrophic', 'Xác thực 2FA, giám sát giao dịch'),
            (4, 'Đồng bộ dữ liệu thất bại', 'Lỗi kết nối giữa Shopee và Sapo', 'likely', 'moderate', 'Monitoring, backup manual'),
            (5, 'Mã độc tống tiền', 'Nhân viên tải file đính kèm độc hại', 'possible', 'major', 'Antivirus, đào tạo nhận thức')
        ]
        
        for i, risk in enumerate(risk_assessments_data, 1):
            asset_id, threat, vulnerability, likelihood, impact, controls = risk
            risk_score = Config.RISK_MATRIX[likelihood][impact]
            risk_level = 'extreme' if risk_score >= 17 else 'high' if risk_score >= 10 else 'medium' if risk_score >= 5 else 'low'
            
            cursor.execute("""
                INSERT INTO risk_assessments 
                (asset_id, threat_description, vulnerability_description, likelihood, impact, 
                 risk_score, risk_level, existing_controls, assessed_by, assessment_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())
            """, (asset_id, threat, vulnerability, likelihood, impact, risk_score, risk_level, controls, 1))
        
        print("✅ Sample risk assessments added!")
        
        # Kết quả kiểm tra mẫu
        from datetime import date, timedelta
        check_results_data = [
            (1, 1, date.today() - timedelta(days=5), 'passed', '2FA đã được kích hoạt'),
            (2, 1, date.today() - timedelta(days=10), 'failed', 'Mật khẩu yếu được phát hiện'),
            (3, 2, date.today() - timedelta(days=15), 'passed', 'Phân quyền hợp lý'),
            (4, 1, date.today() - timedelta(days=2), 'passed', 'Sao lưu thành công'),
            (5, 3, date.today() - timedelta(days=1), 'passed', 'Antivirus đã cập nhật')
        ]
        
        for result in check_results_data:
            cursor.execute("""
                INSERT INTO check_results (check_id, checked_by, check_date, status, notes)
                VALUES (%s, %s, %s, %s, %s)
            """, result)
        
        print("✅ Sample check results added!")
        
        conn.commit()
        print("🎉 Database initialization completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    init_database()
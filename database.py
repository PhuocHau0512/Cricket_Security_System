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
        
        # --- TRONG FILE database.py ---

        # 1. TÀI SẢN THÔNG TIN (Dựa trên Chương 2 Đồ án)
        # Các tài sản: Tài khoản Shopee, Sapo, Dữ liệu khách hàng, Kênh ngân hàng
        assets_data = [
            ('Tài khoản Shopee Mall (Main)', 'account', 'Quyền truy cập cao nhất vào gian hàng Cricket trên Shopee', 1, 'critical', 'critical', 'high'),
            ('Tài khoản Sub-Account (Nhân viên)', 'account', 'Tài khoản phân quyền cho CSKH và Vận hành', 1, 'high', 'medium', 'medium'),
            ('Hệ thống Sapo POS', 'system', 'Hệ thống quản lý kho và đồng bộ đơn hàng đa kênh', 1, 'high', 'high', 'critical'),
            ('Dữ liệu Khách hàng (PII)', 'data', 'Tên, SĐT, Địa chỉ khách hàng từ đơn Shopee', 2, 'critical', 'high', 'medium'),
            ('File Sao kê Tài chính/Ngân hàng', 'financial', 'Dữ liệu đối soát doanh thu Shopee và Ngân hàng', 2, 'critical', 'critical', 'medium'),
            ('Google Drive Nội bộ', 'system', 'Lưu trữ quy trình vận hành và tài liệu công ty', 2, 'medium', 'medium', 'medium')
        ]
        
        for asset in assets_data:
            cursor.execute("""
                INSERT INTO information_assets 
                (asset_name, asset_type, description, owner_id, confidentiality_level, integrity_level, availability_level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, asset)
        
        print("✅ Đã thêm Tài sản đặc thù Shopee/Cricket!")
        
        # 2. KIỂM TRA BẢO MẬT (Dựa trên Chương 3 - Giải pháp)
        checks_data = [
            ('Kiểm tra 2FA Shopee Main', 'Đảm bảo tài khoản chủ shop đã bật xác thực 2 bước', 'account', 1, 'daily'),
            ('Rà soát Sub-account', 'Kiểm tra và xóa các tài khoản nhân viên đã nghỉ việc', 'account', 1, 'monthly'),
            ('Đối soát Sapo & Shopee', 'Kiểm tra lỗi đồng bộ tồn kho tránh sai lệch đơn', 'system', 1, 'daily'),
            ('Scan Máy tính Vận hành', 'Quét virus các máy tính dùng để in đơn hàng', 'system', 1, 'weekly'),
            ('Kiểm tra Log Đăng nhập', 'Phát hiện IP lạ đăng nhập vào Shopee/Sapo', 'process', 1, 'weekly'),
            ('Backup Dữ liệu Đơn hàng', 'Sao lưu thủ công file Excel đơn hàng phòng khi mất Sapo', 'data', 1, 'weekly')
        ]
        
        for check in checks_data:
            cursor.execute("""
                INSERT INTO security_checks (check_name, description, category, is_required, frequency)
                VALUES (?, ?, ?, ?, ?)
            """, check)
        
        print("✅ Đã thêm Checklist vận hành Shopee!")
        
        ## 3. ĐÁNH GIÁ RỦI RO (Dựa trên Risk Matrix 5x5 của đồ án)
        risk_assessments_data = [
            (1, 'Phishing giả mạo Shopee', 'Kẻ gian gửi SMS/Email giả Shopee yêu cầu đăng nhập để chiếm tài khoản', 'likely', 'catastrophic', 'Đào tạo nhận thức, Bật 2FA'),
            (3, 'Lỗi đồng bộ API Sapo', 'Sapo mất kết nối Shopee dẫn đến sai tồn kho, hủy đơn hàng loạt', 'possible', 'major', 'Theo dõi API, Quy trình xử lý đơn thủ công'),
            (4, 'Lộ thông tin khách hàng', 'Nhân viên tải file đơn hàng về máy cá nhân không bảo mật', 'possible', 'catastrophic', 'Phân quyền Sapo, Cấm USB, Giám sát log tải về'),
            (1, 'Mất Cookie trình duyệt', 'Máy tính vận hành bị dính mã độc đánh cắp session đăng nhập', 'possible', 'catastrophic', 'Phần mềm diệt virus, Không lưu mật khẩu trên trình duyệt'),
            (5, 'Gian lận tài chính nội bộ', 'Nhân viên sửa đổi file đối soát ngân hàng', 'unlikely', 'major', 'Quy trình đối soát chéo 2 lớp')
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
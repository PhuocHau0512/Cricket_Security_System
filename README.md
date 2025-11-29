# 🛡️ Cricket Security System

Hệ thống quản lý an ninh mạng cho gian hàng Shopee của Công ty Cổ phần Sản xuất và Thương mại Cricket.

## 📖 Giới thiệu

Cricket Security System là một hệ thống web được phát triển cho khóa luận tốt nghiệp ngành An toàn Thông tin. Hệ thống giúp quản lý và đánh giá rủi ro an ninh mạng cho hoạt động vận hành gian hàng Shopee.

## ✨ Tính năng chính

### 🔐 Bảo mật & Xác thực
- **Hệ thống đăng nhập** với phân quyền (Admin/Manager/Staff)
- **Mã hóa mật khẩu** sử dụng bcrypt
- **Log hoạt động** người dùng
- **Session management**

### 📊 Dashboard & Báo cáo
- **Tổng quan thống kê** (tài sản, rủi ro, sự cố, kiểm tra)
- **Biểu đồ trực quan** phân bố rủi ro và kết quả kiểm tra
- **Sự cố gần đây** và lịch sử kiểm tra

### ⚠️ Quản lý Rủi ro
- **Risk Matrix** tương tác 5x5
- **Đánh giá rủi ro** theo tiêu chuẩn ISO 27005
- **Tính điểm rủi ro** tự động
- **Phân loại rủi ro** (Thấp/Trung bình/Cao/Rất cao)

### 🔍 Security Checks
- **Danh sách kiểm tra** bảo mật định kỳ
- **Theo dõi kết quả** kiểm tra
- **Phân loại theo category** (Account/Data/System/Process)
- **Tần suất kiểm tra** (Daily/Weekly/Monthly/Quarterly)

### 💼 Quản lý Tài sản
- **Danh mục tài sản** thông tin
- **Phân loại tài sản** (Account/Data/System/Financial)
- **Đánh giá CIA** (Confidentiality/Integrity/Availability)

## 🛠 Công nghệ sử dụng

### Backend
- **Python 3.x** với Flask framework
- **SQLite** database (không cần cài đặt thêm)
- **bcrypt** untuk mã hóa mật khẩu

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5** - Responsive design
- **Chart.js** - Biểu đồ trực quan
- **Font Awesome** - Icons

### Security Features
- **Password hashing** với bcrypt
- **Session management**
- **Input validation**
- **SQL injection protection**

## 📁 Cấu trúc dự án
```
Cricket_Security_System/
│
├── app.py # Flask application chính
├── database.py # Khởi tạo database
├── requirements.txt # Python dependencies
├── cricket_security.db # SQLite database (tự động tạo)
│
├── config/
│ └── config.py # Cấu hình ứng dụng
│
├── templates/ # Flask templates
│ ├── base.html # Template chính
│ ├── login.html # Trang đăng nhập
│ ├── dashboard.html # Dashboard chính
│ ├── risk_matrix.html # Ma trận rủi ro
│ ├── add_risk.html # Thêm đánh giá rủi ro
│ └── security_checks.html # Quản lý kiểm tra
│
└── static/ # Static files
├── css/
│ └── custom.css # CSS tùy chỉnh
└── js/
└── custom.js # JavaScript tùy chỉnh
```

## 🚀 Cài đặt và Chạy

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Bước 1: Clone hoặc tải dự án
```bash
git clone <https://github.com/PhuocHau0512/Cricket_Security_System.git>
cd Cricket_Security_System
```

### Bước 2: Tạo virtual environment (khuyến nghị)
```bash
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Khởi tạo database
```bash
python database.py
```

Bước 5: Chạy ứng dụng
```bash
python app.py
```

### Bước 6: Truy cập ứng dụng

Mở trình duyệt và truy cập: http://localhost:5000

## 🔑 Tài khoản mặc định

|Username	|Password	|Vai trò	|Mô tả|
|admin	|admin123	|Admin	|Toàn quyền hệ thống|
|manager	|admin123	|Manager	|Quản lý rủi ro và kiểm tra|
|staff1	|admin123	|Staff	|Xem báo cáo và thông tin|
|staff2	|admin123	|Staff	|Xem báo cáo và thông tin|


## 📊 Risk Matrix
Hệ thống sử dụng ma trận rủi ro 5x5 theo tiêu chuẩn:

1.  **Khả năng xảy ra (Likelihood)**
  -   Rất thấp (Rare) - 1 điểm

  -   Thấp (Unlikely) - 2 điểm

  -   Trung bình (Possible) - 3 điểm

  -   Cao (Likely) - 4 điểm

  -   Rất cao (Almost Certain) - 5 điểm

2.  **Mức độ tác động (Impact)**
  -   Không đáng kể (Insignificant) - 1 điểm

  -    Nhỏ (Minor) - 2 điểm

  -   Trung bình (Moderate) - 3 điểm

  -   Lớn (Major) - 4 điểm

  -   Thảm khốc (Catastrophic) - 5 điểm

3.  **Phân loại rủi ro**
  -   1-4 điểm: 🟢 Rủi ro Thấp

  -   5-9 điểm: 🟡 Rủi ro Trung bình

  -   10-16 điểm: 🟠 Rủi ro Cao

  -   17-25 điểm: 🔴 Rủi ro Rất cao

4.  **🗃 Database Schema**

-   Các bảng chính

  +   employees: Quản lý người dùng và phân quyền

  +   information_assets: Danh mục tài sản thông tin

  +   risk_assessments: Đánh giá rủi ro an ninh

  +   security_checks: Kiểm tra bảo mật định kỳ

  +   check_results: Kết quả kiểm tra

  +   security_incidents: Sự cố an ninh

  +   activity_logs: Nhật ký hoạt động

5.  **🔒 Security Features**

1. Authentication & Authorization
  -   Mật khẩu được mã hóa bằng bcrypt

  -   Phân quyền RBAC (Role-Based Access Control)

  -   Session timeout tự động

2. Data Protection
  -   SQL injection prevention

  -   XSS protection

  -   Input validation và sanitization

3. Audit & Logging
  -   Ghi log đăng nhập/đăng xuất

  -   Theo dõi hoạt động người dùng

  -   Log đánh giá rủi ro và kiểm tra

6.  **📈 Use Cases**

-   Cho Quản trị viên (Admin)

  +   Quản lý người dùng và phân quyền

  +   Xem toàn bộ báo cáo và thống kê

  +   Quản lý danh mục tài sản

-   Cho Quản lý (Manager)

  +   Đánh giá và quản lý rủi ro

  +   Theo dõi kết quả kiểm tra bảo mật

  +   Quản lý sự cố an ninh

-   Cho Nhân viên (Staff)
  +   Xem dashboard và báo cáo

  +   Theo dõi tình hình an ninh

  +   Báo cáo sự cố (nếu được phân quyền)

7.  **🎯 Mục tiêu dự án**

-   Mục tiêu chính
  +   Xây dựng hệ thống quản lý rủi ro an ninh mạng

  +   Đánh giá rủi ro theo khung chuẩn ISO 27005

  +   Cung cấp dashboard báo cáo trực quan

  +   Quản lý kiểm tra bảo mật định kỳ

-   Ứng dụng thực tế
  +   Doanh nghiệp SME: Quản lý rủi ro TMĐT

  +   Cửa hàng Online: Bảo mật gian hàng Shopee

  +   Tổ chức: Hệ thống đánh giá rủi ro nội bộ

## 🐛 Troubleshooting
Lỗi thường gặp
1.  **Port 5000 đã được sử dụng**

```bash
python app.py --port 5001
```

2.  **Lỗi database**

```bash
# Xóa và tạo lại database
rm cricket_security.db
python database.py
```
3.  **Lỗi import**

```bash
# Cài đặt lại dependencies
pip install -r requirements.txt
```

Debug Mode
Ứng dụng đang chạy ở chế độ debug. Để tắt:

python
# Trong app.py, sửa:
app.run(debug=False)

## 📄 Giấy phép
Dự án được phát triển cho mục đích học tập và nghiên cứu.

## 👥 Đóng góp
Đây là dự án khóa luận tốt nghiệp. Mọi đóng góp vui lòng liên hệ tác giả.

## 📞 Liên hệ
Tác giả: Lê Phước Hậu - 2033221314
Email: ph124work@gmail.com
Trường: Đại học Công Thương Thành phố Hồ Chí Minh
Ngành: An toàn Thông tin
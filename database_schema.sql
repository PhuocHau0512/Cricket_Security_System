-- Cricket Security System - SQLite Schema
-- Bảng nhân viên
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role TEXT CHECK(role IN ('admin', 'manager', 'staff')) DEFAULT 'staff',
    department VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT 1
);

-- Bảng tài sản thông tin
CREATE TABLE IF NOT EXISTS information_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_name VARCHAR(200) NOT NULL,
    asset_type TEXT CHECK(asset_type IN ('account', 'data', 'system', 'financial')) NOT NULL,
    description TEXT,
    owner_id INTEGER,
    confidentiality_level TEXT CHECK(confidentiality_level IN ('low', 'medium', 'high', 'critical')) NOT NULL,
    integrity_level TEXT CHECK(integrity_level IN ('low', 'medium', 'high', 'critical')) NOT NULL,
    availability_level TEXT CHECK(availability_level IN ('low', 'medium', 'high', 'critical')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES employees(id)
);

-- Bảng đánh giá rủi ro
CREATE TABLE IF NOT EXISTS risk_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER,
    threat_description TEXT NOT NULL,
    vulnerability_description TEXT NOT NULL,
    likelihood TEXT CHECK(likelihood IN ('rare', 'unlikely', 'possible', 'likely', 'almost_certain')) NOT NULL,
    impact TEXT CHECK(impact IN ('insignificant', 'minor', 'moderate', 'major', 'catastrophic')) NOT NULL,
    risk_score INTEGER,
    risk_level TEXT CHECK(risk_level IN ('low', 'medium', 'high', 'extreme')) NOT NULL,
    existing_controls TEXT,
    assessed_by INTEGER,
    assessment_date DATE NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES information_assets(id),
    FOREIGN KEY (assessed_by) REFERENCES employees(id)
);

-- Bảng sự cố an ninh
CREATE TABLE IF NOT EXISTS security_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    incident_type TEXT CHECK(incident_type IN ('phishing', 'account_compromise', 'data_breach', 'malware', 'dos', 'other')) NOT NULL,
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')) NOT NULL,
    status TEXT CHECK(status IN ('reported', 'investigating', 'contained', 'resolved', 'closed')) DEFAULT 'reported',
    reported_by INTEGER,
    assigned_to INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    resolution_notes TEXT,
    FOREIGN KEY (reported_by) REFERENCES employees(id),
    FOREIGN KEY (assigned_to) REFERENCES employees(id)
);

-- Bảng kiểm tra bảo mật
CREATE TABLE IF NOT EXISTS security_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    check_name VARCHAR(200) NOT NULL,
    description TEXT,
    category TEXT CHECK(category IN ('account', 'data', 'system', 'process')) NOT NULL,
    is_required BOOLEAN DEFAULT 1,
    frequency TEXT CHECK(frequency IN ('daily', 'weekly', 'monthly', 'quarterly')) NOT NULL
);

-- Bảng kết quả kiểm tra
CREATE TABLE IF NOT EXISTS check_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    check_id INTEGER,
    checked_by INTEGER,
    check_date DATE NOT NULL,
    status TEXT CHECK(status IN ('passed', 'failed', 'na')) NOT NULL,
    notes TEXT,
    evidence_file VARCHAR(255),
    FOREIGN KEY (check_id) REFERENCES security_checks(id),
    FOREIGN KEY (checked_by) REFERENCES employees(id)
);

-- Bảng nhật ký hoạt động
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    activity_type VARCHAR(100) NOT NULL,
    description TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES employees(id)
);
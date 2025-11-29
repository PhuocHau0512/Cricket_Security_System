import os

class Config:
    SECRET_KEY = 'cricket_security_key_2024_dev'
    # Sử dụng SQLite
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'cricket_security.db')
    
# Risk Matrix Configuration (có thể bỏ phần này vì đã định nghĩa trong database.py)
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
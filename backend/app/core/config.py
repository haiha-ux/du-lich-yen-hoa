import os

class Config:
    """
    Lớp cấu hình chung cho ứng dụng.
    """
    # Đường dẫn gốc của dự án
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # Đường dẫn đến thư mục chứa dữ liệu
    DATA_DIR = os.path.join(BASE_DIR, 'data')

    # Cấu hình cho session (sẽ được sử dụng bởi API)
    # Trong một ứng dụng thực tế, key này nên được giữ bí mật và phức tạp hơn.
    SECRET_KEY = 'a-very-secret-key-for-session-management'

# Tạo một instance của config để sử dụng trong toàn bộ ứng dụng
settings = Config()

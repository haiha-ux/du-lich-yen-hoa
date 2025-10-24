import sys
import os
from flask import Flask, send_from_directory, request
from flask_cors import CORS

# --- System Path Setup ---
# Thêm đường dẫn của thư mục gốc dự án vào sys.path
# để có thể import các module một cách nhất quán.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Import Modules ---
from backend.app.core.config import settings
from api.routes.content import content_bp
from api.security import session_manager

# --- App Initialization ---
def create_app():
    """
    Hàm khởi tạo và cấu hình ứng dụng Flask.
    """
    app = Flask(__name__)
    CORS(app)  # Kích hoạt CORS

    # Thiết lập secret key cho session từ file config
    app.secret_key = settings.SECRET_KEY

    # Đăng ký Blueprint cho các content routes, với tiền tố /api
    app.register_blueprint(content_bp, url_prefix='/api')

    # --- Request Hook ---
    @app.before_request
    def before_request_func():
        """
        Hàm này sẽ chạy trước mỗi request.
        Tự động tạo session cho người dùng mới.
        """
        session_manager.create_user_session()

    # --- Static File Serving ---
    @app.route('/data/<path:filename>')
    def serve_data_files(filename):
        """
        Phục vụ các file tĩnh (hình ảnh) từ thư mục data của backend.
        """
        return send_from_directory(settings.DATA_DIR, filename)

    return app

# --- Main Execution ---
if __name__ == '__main__':
    app = create_app()
    # Chạy app ở chế độ debug trên port 5000
    app.run(debug=True, port=5000)

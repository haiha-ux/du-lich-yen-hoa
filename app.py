import sys
import os
from flask import Flask, send_from_directory
from flask_cors import CORS

# --- System Path Setup ---
# Thêm đường dẫn của thư mục gốc dự án vào sys.path
project_root = os.path.abspath(os.path.dirname(__file__))
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
    Ứng dụng này sẽ phục vụ cả frontend tĩnh và backend API.
    """
    # Thiết lập thư mục 'frontend' làm thư mục chứa file tĩnh
    app = Flask(__name__, static_folder='frontend', static_url_path='')
    CORS(app)

    # Thiết lập secret key cho session
    app.secret_key = settings.SECRET_KEY

    # Đăng ký API blueprint với tiền tố /api
    app.register_blueprint(content_bp, url_prefix='/api')

    # --- Request Hook ---
    @app.before_request
    def before_request_func():
        """Chạy trước mỗi request để tạo session cho người dùng mới."""
        session_manager.create_user_session()

    # --- Route cho Frontend ---
    @app.route('/')
    def serve_index():
        """Phục vụ file index.html chính."""
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_frontend_files(path):
        """Phục vụ các file khác của frontend (attractions.html, assets/*, etc.)."""
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        # Nếu không tìm thấy file, trả về trang chủ (hữu ích cho Single Page Apps)
        return send_from_directory(app.static_folder, 'index.html')

    # --- Route cho Dữ liệu Backend (Hình ảnh) ---
    @app.route('/data/<path:filename>')
    def serve_data_files(filename):
        """Phục vụ các file tĩnh (hình ảnh) từ thư mục backend/data."""
        return send_from_directory(settings.DATA_DIR, filename)

    return app

# --- Main Execution ---
if __name__ == '__main__':
    app = create_app()
    print("========================================================")
    print(" Server đã sẵn sàng!")
    print(" Vui lòng truy cập trang web tại: http://127.0.0.1:5000")
    print("========================================================")
    app.run(debug=True, port=5000, host='0.0.0.0')

from flask import Blueprint, jsonify, request
import sys
import os

# Thêm đường dẫn của thư mục gốc dự án vào sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import content_service từ backend
from backend.app.services.content_service import content_service

# Tạo một Blueprint. Blueprint giống như một mini-app, giúp tổ chức các route.
content_bp = Blueprint('content', __name__)

@content_bp.route('/content', methods=['GET'])
def get_full_content():
    """API endpoint để lấy toàn bộ nội dung đã được xử lý."""
    return jsonify(content_service.get_full_content())

@content_bp.route('/about', methods=['GET'])
def get_about():
    """API endpoint để lấy thông tin giới thiệu."""
    return jsonify(content_service.get_about_content())

@content_bp.route('/attractions', methods=['GET'])
def get_attractions():
    """
    API endpoint để lấy danh sách điểm đến.
    Hỗ trợ query parameter `featured` để lọc các điểm nổi bật.
    """
    is_featured = request.args.get('featured', 'false').lower() == 'true'
    if is_featured:
        return jsonify(content_service.get_featured_attractions())
    return jsonify(content_service.get_all_attractions())

@content_bp.route('/gallery', methods=['GET'])
def get_gallery():
    """API endpoint để lấy danh sách thư viện."""
    return jsonify(content_service.get_gallery_items())

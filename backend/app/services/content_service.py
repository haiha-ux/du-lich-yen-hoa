import json
import os

# Xác định đường dẫn tuyệt đối đến file content.json
# Điều này đảm bảo service có thể chạy từ bất kỳ đâu
_current_dir = os.path.dirname(os.path.abspath(__file__))
_data_file = os.path.join(_current_dir, '..', '..', 'data', 'content.json')

class ContentService:
    """
    Lớp dịch vụ để xử lý tất cả các logic liên quan đến nội dung.
    """

    def __init__(self, data_path=_data_file):
        """
        Khởi tạo service và tải dữ liệu từ file JSON.
        """
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Data file not found at {data_path}")
            self._data = {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {data_path}")
            self._data = {}

    def get_about_content(self):
        """
        Lấy nội dung giới thiệu.
        """
        return self._data.get('about', {})

    def get_full_content(self):
        """
        Lấy toàn bộ dữ liệu.
        """
        return self._data

    def get_all_attractions(self):
        """
        Lấy tất cả các điểm đến.
        """
        return self._data.get('attractions', [])

    def get_featured_attractions(self):
        """
        Lọc và lấy các điểm đến được đánh dấu là nổi bật (featured).
        """
        all_attractions = self.get_all_attractions()
        return [attr for attr in all_attractions if attr.get('featured', False)]

    def get_gallery_items(self):
        """
        Lấy tất cả các mục trong thư viện ảnh.
        """
        return self._data.get('gallery', [])

# Tạo một instance của service để có thể import và sử dụng ở nơi khác
content_service = ContentService()

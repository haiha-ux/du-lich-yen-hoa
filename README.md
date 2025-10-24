# Website Du Lịch Bản Yên Hòa

Đây là dự án website quảng bá du lịch cho Bản Yên Hòa, xã Mỹ Lý, tỉnh Nghệ An. Dự án được xây dựng theo kiến trúc 3 lớp tách biệt: Frontend, Backend, và API.

## Cấu trúc thư mục

```
/du_lich_yen_hoa
|-- frontend/       # Giao diện người dùng (HTML, CSS, JS)
|-- backend/        # Logic xử lý và quản lý dữ liệu (Python)
|-- api/            # Lớp giao tiếp giữa frontend và backend (Python Flask)
`-- README.md       # Hướng dẫn này
```

## Yêu cầu cài đặt

- Python 3.6+
- pip (trình quản lý gói cho Python)
- Trình duyệt web hiện đại (Chrome, Firefox, Edge)

## Hướng dẫn cài đặt và chạy dự án

### 1. Cài đặt thư viện Python

Mở terminal hoặc command prompt, di chuyển đến thư mục gốc `du_lich_yen_hoa` và chạy lệnh sau để cài đặt các thư viện cần thiết:

```bash
pip install Flask Flask-Cors
```

### 2. Chạy ứng dụng

Trong terminal, đảm bảo bạn đang ở thư mục gốc `du_lich_yen_hoa`, sau đó chạy lệnh:

```bash
python app.py
```

Server sẽ khởi động. Bây giờ, bạn chỉ cần mở trình duyệt và truy cập vào địa chỉ sau:

**http://127.0.0.1:5000**

Trang web sẽ được hiển thị và tất cả các dịch vụ (frontend, backend, API) đều đã sẵn sàng.

## Mô tả các thành phần

### Frontend

- **Ngôn ngữ**: HTML, CSS, JavaScript (không dùng framework).
- **Cấu trúc**:
    - `index.html`: Trang chủ.
    - `attractions.html`: Trang danh sách các điểm đến.
    - `gallery.html`: Trang thư viện ảnh.
    - `assets/`: Chứa các file CSS, JS, và hình ảnh.
    - `assets/js/api_handler.js`: Module chuyên xử lý việc gọi API.
    - `assets/js/main.js`: Logic chính để điều khiển hiển thị trên các trang.

### Backend

- **Ngôn ngữ**: Python.
- **Cấu trúc**:
    - `data/content.json`: Đóng vai trò là một "database" dạng file, chứa toàn bộ nội dung của website.
    - `app/services/content_service.py`: Lớp dịch vụ chứa logic để đọc và xử lý dữ liệu từ `content.json`.

### API

- **Framework**: Flask.
- **Chức năng**:
    - Cung cấp các endpoint (`/api/about`, `/api/attractions`, `/api/gallery`) để `frontend` lấy dữ liệu.
    - Phục vụ các file tĩnh (hình ảnh) từ thư mục `backend/data`.
    - Cho phép CORS để `frontend` có thể gọi API từ một domain khác (khi mở file HTML trực tiếp).

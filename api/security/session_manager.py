from flask import session
import uuid

SESSION_USER_ID_KEY = 'user_id'

def create_user_session():
    """
    Tạo một session mới cho người dùng nếu chưa tồn tại.

    Hàm này gán một định danh duy nhất (UUID) cho mỗi người dùng
    truy cập trang web lần đầu. Điều này hữu ích để theo dõi
    hành vi người dùng hoặc cho các tính năng nâng cao sau này
    mà không cần đăng nhập.
    """
    if SESSION_USER_ID_KEY not in session:
        session[SESSION_USER_ID_KEY] = str(uuid.uuid4())

def get_user_id():
    """
    Lấy ID người dùng từ session hiện tại.
    """
    return session.get(SESSION_USER_ID_KEY)

def clear_user_session():
    """
    Xóa session của người dùng (tương tự như logout).
    """
    session.pop(SESSION_USER_ID_KEY, None)

from typing import Optional

class Place:
    """
    Lớp đại diện cho một địa điểm du lịch (Attraction).

    Sử dụng lớp này giúp mã nguồn trở nên tường minh và dễ quản lý hơn
    so với việc sử dụng dictionary trực tiếp.
    """
    def __init__(self, id: int, name: str, summary: str, image_url: str, featured: bool = False):
        self.id = id
        self.name = name
        self.summary = summary
        self.image_url = image_url
        self.featured = featured

    def to_dict(self) -> dict:
        """
        Chuyển đổi đối tượng Place thành một dictionary để dễ dàng serialize thành JSON.
        """
        return {
            "id": self.id,
            "name": self.name,
            "summary": self.summary,
            "imageUrl": self.image_url,
            "featured": self.featured
        }

    @staticmethod
    def from_dict(data: dict) -> Optional['Place']:
        """
        Tạo một đối tượng Place từ một dictionary.
        Trả về None nếu dữ liệu đầu vào không hợp lệ.
        """
        try:
            return Place(
                id=data['id'],
                name=data['name'],
                summary=data['summary'],
                image_url=data['imageUrl'],
                featured=data.get('featured', False)
            )
        except KeyError:
            # Trả về None nếu thiếu trường thông tin quan trọng
            return None

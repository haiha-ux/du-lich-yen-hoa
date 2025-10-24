const API_BASE_URL = '/api'; // Đường dẫn tương đối, vì frontend và API giờ cùng một server

/**
 * Hàm fetch dữ liệu chung từ API
 * @param {string} endpoint - Đường dẫn API endpoint (ví dụ: '/attractions')
 * @returns {Promise<any>} - Dữ liệu trả về từ API
 */
async function fetchData(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Could not fetch data from ${endpoint}:`, error);
        return null; // Trả về null nếu có lỗi để xử lý ở nơi gọi
    }
}

/**
 * Lấy toàn bộ nội dung trang web
 * @returns {Promise<object|null>}
 */
function getContent() {
    return fetchData('/content');
}

/**
 * Lấy thông tin giới thiệu chung
 * @returns {Promise<object|null>}
 */
function getAboutContent() {
    return fetchData('/about');
}

/**
 * Lấy danh sách tất cả các điểm đến
 * @returns {Promise<Array|null>}
 */
function getAllAttractions() {
    return fetchData('/attractions');
}

/**
 * Lấy danh sách các điểm đến nổi bật (ví dụ: 3 điểm)
 * @returns {Promise<Array|null>}
 */
function getFeaturedAttractions() {
    return fetchData('/attractions?featured=true');
}

/**
 * Lấy danh sách hình ảnh/video trong thư viện
 * @returns {Promise<Array|null>}
 */
function getGalleryItems() {
    return fetchData('/gallery');
}

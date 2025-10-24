document.addEventListener('DOMContentLoaded', () => {
    // Lấy đường dẫn trang hiện tại để quyết định hàm nào cần chạy
    const path = window.location.pathname;

    if (path.endsWith('index.html') || path === '/') {
        loadHomePage();
    } else if (path.endsWith('attractions.html')) {
        loadAttractionsPage();
    } else if (path.endsWith('gallery.html')) {
        loadGalleryPage();
    }
});

/**
 * Tải dữ liệu cho trang chủ
 */
async function loadHomePage() {
    // Tải và hiển thị phần giới thiệu
    const contentData = await getContent(); // Giả sử có hàm getContent trả về toàn bộ JSON
    if (!contentData) return;

    const { about, sections, attractions } = contentData;

    const aboutTitle = document.getElementById('about-title');
    const aboutContent = document.getElementById('about-content');
    if (about && aboutTitle && aboutContent) {
        aboutTitle.textContent = about.title;
        aboutContent.textContent = about.text;
    }

    // Tải và hiển thị các sections
    const sectionsContainer = document.getElementById('content-sections');
    if (sections && sectionsContainer) {
        sectionsContainer.innerHTML = '';
        sections.forEach((section, index) => {
            const sectionElement = createContentSection(section, index);
            sectionsContainer.appendChild(sectionElement);
        });
    }

    // Tải và hiển thị các điểm đến nổi bật
    const featuredAttractions = attractions.filter(a => a.featured);
    const attractionsGrid = document.getElementById('attractions-grid');
    if (featuredAttractions && attractionsGrid) {
        attractionsGrid.innerHTML = '';
        featuredAttractions.forEach(attraction => {
            const card = createAttractionCard(attraction);
            attractionsGrid.appendChild(card);
        });
    }
}

/**
 * Tải dữ liệu cho trang điểm đến
 */
async function loadAttractionsPage() {
    const allAttractions = await getAllAttractions();
    const attractionsList = document.getElementById('attractions-list');
    if (allAttractions && attractionsList) {
        attractionsList.innerHTML = '';
        allAttractions.forEach(attraction => {
            const card = createAttractionCard(attraction);
            attractionsList.appendChild(card);
        });
    }
}

/**
 * Tải dữ liệu cho trang thư viện
 */
async function loadGalleryPage() {
    const galleryItems = await getGalleryItems();
    const galleryGrid = document.getElementById('gallery-grid');
    if (galleryItems && galleryGrid) {
        galleryGrid.innerHTML = '';
        galleryItems.forEach(item => {
            const galleryElement = document.createElement('div');
            galleryElement.className = 'gallery-item';
            
            const img = document.createElement('img');
            img.src = item.url;
            img.alt = item.alt;
            // Thêm sự kiện click để mở modal
            img.onclick = () => openModal(item.url, item.alt);

            galleryElement.appendChild(img);
            galleryGrid.appendChild(galleryElement);
        });

        // Thêm sự kiện cho nút đóng modal
        const modal = document.getElementById('image-modal');
        const closeButton = document.querySelector('.close-button');
        if (modal && closeButton) {
            closeButton.onclick = () => modal.style.display = "none";
        }
    }
}

/**
 * Mở modal hiển thị ảnh lớn
 * @param {string} src - Đường dẫn ảnh
 * @param {string} alt - Chú thích ảnh
 */
function openModal(src, alt) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');
    const captionText = document.getElementById('caption');
    
    if (modal && modalImg && captionText) {
        modal.style.display = "block";
        modalImg.src = src;
        captionText.innerHTML = alt;
    }
}

/**
 * Helper function: Tạo một card HTML cho điểm đến
 * @param {object} attraction - Dữ liệu của một điểm đến
 * @returns {HTMLElement} - Phần tử HTML của card
 */
function createAttractionCard(attraction) {
    const card = document.createElement('div');
    card.className = 'attraction-card';

    const isAttractionsPage = window.location.pathname.endsWith('attractions.html');
    
    let detailsHtml = `<p>${attraction.summary}</p>`;
    if (isAttractionsPage && attraction.description) {
        detailsHtml += `<p class="attraction-description">${attraction.description}</p>`;
    }

    card.innerHTML = `
        <img src="${attraction.imageUrl}" alt="${attraction.name}">
        <div class="attraction-card-content">
            <h3>${attraction.name}</h3>
            ${detailsHtml}
        </div>
    `;
    return card;
}

/**
 * Helper function: Tạo một section nội dung cho trang chủ
 * @param {object} section - Dữ liệu của một section
 * @param {number} index - Chỉ số của section (để xen kẽ layout)
 * @returns {HTMLElement} - Phần tử HTML của section
 */
function createContentSection(section, index) {
    const sectionElement = document.createElement('div');
    sectionElement.className = 'content-section';
    // Xen kẽ layout cho các section chẵn/lẻ
    if (index % 2 !== 0) {
        sectionElement.classList.add('reverse');
    }

    sectionElement.innerHTML = `
        <div class="section-image">
            <img src="${section.imageUrl}" alt="${section.title}">
        </div>
        <div class="section-text">
            <h3>${section.title}</h3>
            <p>${section.content}</p>
        </div>
    `;
    return sectionElement;
}

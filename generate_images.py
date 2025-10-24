import os
import shutil
from ai_thuc_chien_wrapper import AIThucChienAPI

# --- CONFIGURATION ---
API_KEY = "sk-mC3HR1XKLMrP__q7lxFrVA"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(SCRIPT_DIR, "backend", "data", "images")

# --- INITIALIZATION ---
api = AIThucChienAPI(api_key=API_KEY)

# --- HELPER FUNCTIONS ---
def setup_directories():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    print(f"Thư mục '{IMAGE_DIR}' đã sẵn sàng.")

def generate_and_save_image(prompt: str, filename: str, aspect_ratio: str = "16:9"):
    output_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(output_path):
        print(f"✅ Ảnh '{filename}' đã tồn tại, bỏ qua.")
        return

    print(f"🎨 Đang tạo ảnh cho: {filename}...")
    try:
        images = api.generate_image(
            prompt=prompt,
            n=1,
            aspect_ratio=aspect_ratio,
            model="imagen-4"
        )
        if images:
            api.save_image(images[0], output_path)
        else:
            print(f"Lỗi: Không tạo được ảnh cho '{filename}'")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi tạo ảnh '{filename}': {e}")

# --- MAIN LOGIC ---
def main():
    setup_directories()

    print("\nBắt đầu quá trình cuối cùng để tạo các ảnh còn thiếu...")

    final_missing_prompts = {
        "suoi_moc.jpg": ("A clear, tranquil stream in a lush Vietnamese forest. Sunlight filtering through the trees. Photorealistic.", "4:3"),
        "gallery_4.jpg": ("A beautiful arrangement of Vietnamese highland food on a banana leaf, featuring grilled fish and colorful sticky rice. Top-down view, vibrant colors.", "4:3")
    }

    for filename, (prompt, aspect_ratio) in final_missing_prompts.items():
        generate_and_save_image(prompt, filename, aspect_ratio)

    print("\n✅ Quá trình tạo ảnh cuối cùng đã hoàn tất!")

if __name__ == "__main__":
    main()

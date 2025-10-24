"""
AI Thực Chiến API Wrapper
=========================


Wrapper class hoàn chỉnh cho AI Thực Chiến API Gateway
Tích hợp tất cả tricks và best practices từ documentation


Author: AI Thực Chiến Competition
Version: 1.0.0
"""


import requests
import base64
import time
import random
import json
from typing import List, Dict, Optional, Union, Tuple
from pathlib import Path
import io




class AIThucChienAPI:
    """
    Wrapper class chính cho AI Thực Chiến API


    Usage:
        api = AIThucChienAPI(api_key="your_api_key")
        response = api.generate_text("Hello world")
    """


    def __init__(self, api_key: str, base_url: str = "https://api.thucchien.ai"):
        """
        Khởi tạo API client


        Args:
            api_key: API key từ AI Thực Chiến
            base_url: Base URL của API (default: https://api.thucchien.ai)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.gemini_headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }


    # =============================================
    # PHẦN 1: CÁC HÀM CƠ BẢN (Basic Functions)
    # =============================================


    def generate_text(
        self,
        prompt: str,
        model: str = "gemini-2.5-pro",
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """
        Sinh văn bản từ prompt


        Args:
            prompt: Nội dung prompt
            model: Tên model (gemini-2.5-pro, gemini-2.5-flash)
            temperature: Độ ngẫu nhiên (0-2)
            max_tokens: Số tokens tối đa


        Returns:
            Dict chứa response từ API
        """
        url = f"{self.base_url}/chat/completions"


        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }


        if max_tokens:
            data["max_tokens"] = max_tokens


        data.update(kwargs)


        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()


    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gemini-2.5-pro",
        temperature: float = 1.0,
        **kwargs
    ) -> Dict:
        """
        Tạo chat completion với history messages


        Args:
            messages: List các messages theo format OpenAI
            model: Tên model
            temperature: Độ ngẫu nhiên


        Returns:
            Dict chứa response
        """
        url = f"{self.base_url}/chat/completions"


        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        data.update(kwargs)


        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()


    def generate_image(
        self,
        prompt: str,
        model: str = "imagen-4",
        n: int = 1,
        aspect_ratio: str = "1:1",
        **kwargs
    ) -> List[str]:
        """
        Sinh hình ảnh từ prompt (trả về list base64 data URLs)


        Args:
            prompt: Mô tả hình ảnh
            model: Tên model (imagen-4)
            n: Số lượng ảnh cần tạo (1-4)
            aspect_ratio: Tỷ lệ khung hình (1:1, 3:4, 4:3, 16:9, 9:16)


        Returns:
            List các data URL của ảnh (data:image/png;base64,...)
        """
        # Thêm random seed để tránh cache (TRICK từ docs)
        prompt_with_seed = f"{prompt} {random.randint(1, 10000)}"


        url = f"{self.base_url}/images/generations"


        data = {
            "model": model,
            "prompt": prompt_with_seed,
            "n": n,
            "aspect_ratio": aspect_ratio
        }
        data.update(kwargs)


        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()


        result = response.json()
        images = []
        for item in result.get('data', []):
            b64_data = item.get('b64_json')
            if b64_data:
                # Return as data URL format
                images.append(f"data:image/png;base64,{b64_data}")


        return images


    def generate_image_chat(
        self,
        prompt: str,
        model: str = "gemini-2.5-flash-image-preview",
        messages: Optional[List[Dict]] = None
    ) -> str:
        """
        Sinh hình ảnh qua chat endpoint (multimodal)
        Hỗ trợ consistent character generation


        Args:
            prompt: Mô tả hình ảnh
            model: Model multimodal
            messages: History messages để maintain consistency


        Returns:
            Data URL của ảnh (data:image/png;base64,...)
        """
        url = f"{self.base_url}/chat/completions"


        if messages is None:
            messages = []


        messages.append({"role": "user", "content": prompt})


        data = {
            "model": model,
            "messages": messages,
            "modalities": ["image"]
        }


        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()


        result = response.json()
        image_url = result['choices'][0]['message']['images'][0]['image_url']['url']


        return image_url


    def text_to_speech(
        self,
        text: str,
        model: str = "gemini-2.5-flash-preview-tts",
        voice: str = "Zephyr"
    ) -> bytes:
        """
        Chuyển văn bản thành giọng nói


        Args:
            text: Văn bản cần chuyển
            model: Model TTS
            voice: Giọng nói (Zephyr, Puck, Charon, Kore, ...)


        Returns:
            Bytes của file âm thanh
        """
        url = f"{self.base_url}/audio/speech"


        data = {
            "model": model,
            "input": text,
            "voice": voice
        }


        response = requests.post(url, headers=self.headers, json=data, stream=True)
        response.raise_for_status()


        return response.content


    def text_to_speech_gemini(
        self,
        text: str,
        model: str = "gemini-2.5-flash-preview-tts",
        multi_speaker: bool = False,
        speaker_configs: Optional[List[Dict]] = None
    ) -> bytes:
        """
        Chuyển văn bản thành giọng nói với Gemini API (hỗ trợ multi-speaker)


        Args:
            text: Văn bản cần chuyển
            model: Model TTS
            multi_speaker: Có phải multi-speaker không
            speaker_configs: Danh sách config cho từng speaker
                            Format: [{"speaker": "John", "voice": "Puck"}, ...]


        Returns:
            Bytes của file âm thanh
        """
        url = f"{self.base_url}/gemini/v1beta/models/{model}:generateContent"


        data = {
            "contents": [{
                "parts": [{"text": text}]
            }],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {}
            }
        }


        if multi_speaker and speaker_configs:
            # Multi-speaker configuration
            speaker_voice_configs = []
            for config in speaker_configs:
                speaker_voice_configs.append({
                    "speaker": config["speaker"],
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": config["voice"]
                        }
                    }
                })


            data["generationConfig"]["speechConfig"]["multiSpeakerVoiceConfig"] = {
                "speakerVoiceConfigs": speaker_voice_configs
            }
        else:
            # Single speaker configuration
            voice = speaker_configs[0]["voice"] if speaker_configs else "Kore"
            data["generationConfig"]["speechConfig"]["voiceConfig"] = {
                "prebuiltVoiceConfig": {
                    "voiceName": voice
                }
            }


        response = requests.post(url, headers=self.gemini_headers, json=data)
        response.raise_for_status()


        result = response.json()


        # Extract audio data from response
        audio_b64 = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
        return base64.b64decode(audio_b64)


    def check_spending(self) -> Dict:
        """
        Kiểm tra chi tiêu API key


        Returns:
            Dict chứa thông tin chi tiêu
        """
        url = f"{self.base_url}/key/info"


        response = requests.get(url, headers=self.headers)
        response.raise_for_status()


        return response.json()


    # =============================================
    # PHẦN 2: VIDEO GENERATION (Async 3-step process)
    # =============================================


    def start_video_generation(
        self,
        prompt: str,
        model: str = "veo-3.0-generate-001",
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        image_base64: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Bước 1: Bắt đầu tạo video (async)


        Args:
            prompt: Mô tả video
            model: Model video (veo-3.0-generate-001, veo-3.0-fast-generate-001, veo-2.0-generate-001)
            aspect_ratio: Tỷ lệ (16:9 hoặc 9:16)
            resolution: Độ phân giải (720p hoặc 1080p)
            image_base64: Ảnh đầu vào (base64) cho image-to-video


        Returns:
            operation_name để tracking
        """
        url = f"{self.base_url}/gemini/v1beta/models/{model}:predictLongRunning"


        instance = {"prompt": prompt}


        if image_base64:
            instance["image"] = {
                "bytesBase64Encoded": image_base64,
                "mimeType": "image/png"
            }


        data = {
            "instances": [instance],
            "parameters": {
                "aspectRatio": aspect_ratio,
                "resolution": resolution
            }
        }


        # Add extra parameters
        data["parameters"].update(kwargs)


        response = requests.post(url, headers=self.gemini_headers, json=data)
        response.raise_for_status()


        result = response.json()
        return result.get("name")


    def check_video_status(self, operation_name: str) -> Tuple[bool, Optional[str]]:
        """
        Bước 2: Kiểm tra trạng thái video


        Args:
            operation_name: Name từ bước 1


        Returns:
            (is_done, video_uri)
        """
        url = f"{self.base_url}/gemini/v1beta/{operation_name}"


        response = requests.get(url, headers=self.gemini_headers)
        response.raise_for_status()


        result = response.json()
        is_done = result.get("done", False)


        video_uri = None
        if is_done and "response" in result:
            try:
                video_uri = result["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
            except (KeyError, IndexError):
                pass


        return is_done, video_uri


    def download_video(self, video_uri: str) -> bytes:
        """
        Bước 3: Tải video về


        Args:
            video_uri: URI từ bước 2


        Returns:
            Bytes của video
        """
        # Extract video_id from URI
        # URI format: https://generativelanguage.googleapis.com/v1beta/files/{video_id}:download?alt=media
        video_id = video_uri.split('/files/')[1].split(':')[0]


        url = f"{self.base_url}/gemini/download/v1beta/files/{video_id}:download?alt=media"


        response = requests.get(url, headers=self.gemini_headers, stream=True)
        response.raise_for_status()


        return response.content


    # =============================================
    # PHẦN 3: CÁC HÀM NÂNG CAO (Advanced Functions with Tricks)
    # =============================================


    def generate_video_complete(
        self,
        prompt: str,
        model: str = "veo-3.0-generate-001",
        max_wait_time: int = 600,
        poll_interval: int = 10,
        **kwargs
    ) -> bytes:
        """
        Tạo video hoàn chỉnh (auto polling)


        Args:
            prompt: Mô tả video
            model: Model video
            max_wait_time: Thời gian chờ tối đa (giây)
            poll_interval: Khoảng thời gian giữa các lần check (giây)


        Returns:
            Bytes của video
        """
        print(f"🎬 Bắt đầu tạo video: {prompt[:50]}...")


        # Bước 1: Start
        operation_name = self.start_video_generation(prompt, model, **kwargs)
        print(f"✅ Đã bắt đầu: {operation_name}")


        # Bước 2: Poll until done
        start_time = time.time()
        current_interval = poll_interval


        while time.time() - start_time < max_wait_time:
            print(f"⏳ Đang kiểm tra... ({int(time.time() - start_time)}s)")


            is_done, video_uri = self.check_video_status(operation_name)


            if is_done and video_uri:
                print("🎉 Video đã hoàn thành!")
                # Bước 3: Download
                video_bytes = self.download_video(video_uri)
                print(f"📥 Đã tải xong: {len(video_bytes)} bytes")
                return video_bytes


            time.sleep(current_interval)
            # Exponential backoff
            current_interval = min(current_interval * 1.2, 30)


        raise TimeoutError(f"Timeout after {max_wait_time} seconds")


    def create_consistent_character_images(
        self,
        character_description: str,
        scenes: List[str],
        model: str = "gemini-2.5-flash-image-preview"
    ) -> List[str]:
        """
        TRICK: Tạo nhiều ảnh với nhân vật nhất quán
        Phương pháp: Ghép character description vào mỗi scene prompt


        Args:
            character_description: Mô tả chi tiết nhân vật
            scenes: List các scene khác nhau
            model: Model multimodal


        Returns:
            List data URLs của các ảnh
        """
        images = []


        # Ảnh đầu tiên: mô tả đầy đủ
        print(f"🎨 Tạo ảnh tham chiếu: {character_description[:50]}...")
        first_image = self.generate_image_chat(character_description, model)
        images.append(first_image)


        # Các ảnh tiếp theo: Ghép character description + scene description
        for i, scene in enumerate(scenes):
            print(f"🎨 Tạo ảnh {i+2}/{len(scenes)+1}: {scene[:50]}...")


            # TRICK: Ghép character vào scene để giữ nhất quán
            combined_prompt = f"{character_description}, {scene}"


            image = self.generate_image_chat(combined_prompt, model)
            images.append(image)


        print(f"✅ Hoàn thành {len(images)} ảnh với cùng nhân vật!")
        return images


    def create_vietnamese_text_image(
        self,
        background_prompt: str,
        vietnamese_text: str,
        text_color: str = "yellow",
        model: str = "gemini-2.5-flash-image-preview"
    ) -> bytes:
        """
        TRICK: Tạo ảnh có chữ tiếng Việt không bị lỗi font
        1. Tạo ảnh nền không có chữ
        2. Tạo ảnh chữ riêng
        3. Dùng AI merge 2 ảnh


        Args:
            background_prompt: Mô tả ảnh nền
            vietnamese_text: Chữ tiếng Việt cần thêm
            text_color: Màu chữ
            model: Model multimodal


        Returns:
            Bytes của ảnh hoàn chỉnh
        """
        # Bước 1: Tạo ảnh nền không có chữ
        print("🎨 Bước 1: Tạo ảnh nền...")
        background_prompt_no_text = f"{background_prompt}. Do not include any text. Leave a clear, empty space for the title text."
        background_img = self.generate_image_chat(background_prompt_no_text, model)


        # Bước 2: Người dùng tự tạo ảnh chữ bằng tool (Canva, Photoshop...)
        # Ở đây chỉ hướng dẫn
        print(f"📝 Bước 2: Tạo ảnh chữ '{vietnamese_text}' bằng Canva/Photoshop")
        print("   - Nền trắng")
        print("   - Font đẹp")
        print("   - Lưu thành PNG/JPG")
        print("   - Chuyển sang base64 và truyền vào merge_vietnamese_text_to_image()")


        return background_img


    def merge_vietnamese_text_to_image(
        self,
        background_image_base64: str,
        text_image_base64: str,
        placement_instruction: str = "Place it in a visually fitting position",
        model: str = "gemini-2.5-flash-image-preview"
    ) -> bytes:
        """
        TRICK: Merge chữ tiếng Việt vào ảnh nền bằng AI


        Args:
            background_image_base64: Base64 của ảnh nền
            text_image_base64: Base64 của ảnh chữ
            placement_instruction: Hướng dẫn đặt chữ
            model: Model multimodal


        Returns:
            Bytes của ảnh đã merge
        """
        url = f"{self.base_url}/gemini/v1beta/models/{model}:generateContent"


        data = {
            "contents": [{
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": background_image_base64
                        }
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": text_image_base64
                        }
                    },
                    {
                        "text": f"Add the text from the second image onto the first image. {placement_instruction}"
                    }
                ]
            }],
            "generationConfig": {
                "imageConfig": {
                    "aspectRatio": "1:1"
                }
            }
        }


        response = requests.post(url, headers=self.gemini_headers, json=data)
        response.raise_for_status()


        result = response.json()
        image_data = result['candidates'][0]['content']['parts'][0]['inlineData']['data']


        return base64.b64decode(image_data)


    def create_comic_consistent(
        self,
        title: str,
        character_description: str,
        panels: List[Dict[str, str]],
        model: str = "gemini-2.5-flash-image-preview"
    ) -> List[bytes]:
        """
        Tạo truyện tranh với nhân vật nhất quán


        Args:
            title: Tiêu đề truyện
            character_description: Mô tả nhân vật chi tiết
            panels: List các panel, mỗi panel là dict {"scene": "...", "dialogue": "..."}
            model: Model multimodal


        Returns:
            List bytes của các trang truyện
        """
        print(f"📖 Tạo truyện tranh: {title}")


        # Tạo cover page
        cover_prompt = f"Comic book cover titled '{title}'. {character_description}. Semi-realistic manga style, A4 vertical."
        print("🎨 Tạo trang bìa...")
        cover_img = self.generate_image_chat(cover_prompt, model)


        # Tạo các panel với nhân vật nhất quán
        panel_scenes = [p["scene"] for p in panels]
        panel_images = self.create_consistent_character_images(
            character_description,
            panel_scenes,
            model
        )


        print(f"✅ Hoàn thành truyện tranh {len(panel_images) + 1} trang!")
        return [cover_img] + panel_images


    def create_news_video_with_mc(
        self,
        news_content: str,
        mc_description: str = "A professional Vietnamese female news anchor, 30s, wearing formal attire",
        duration: int = 80,
        model: str = "veo-3.0-generate-001"
    ) -> bytes:
        """
        TRICK: Tạo video bản tin có MC ảo
        1. Tạo ảnh MC nhất quán
        2. Tạo script đọc tin
        3. Tạo TTS cho MC
        4. Tạo video từ ảnh MC + prompt
        5. User tự ghép video + audio bằng tool


        Args:
            news_content: Nội dung tin tức
            mc_description: Mô tả MC
            duration: Thời lượng video
            model: Model video


        Returns:
            Bytes của video MC (chưa có audio)
        """
        print("📺 Tạo video bản tin với MC ảo...")


        # Bước 1: Tạo ảnh MC
        print("🎨 Tạo hình ảnh MC...")
        mc_image = self.generate_image_chat(mc_description)
        mc_image_base64 = base64.b64encode(mc_image).decode('utf-8')


        # Bước 2: Tạo script
        print("📝 Tạo script...")
        script_prompt = f"Viết script bản tin truyền hình chuyên nghiệp về: {news_content}. Thời lượng {duration} giây. Văn phong trang trọng, dễ hiểu."
        script_response = self.generate_text(script_prompt)
        script = script_response['choices'][0]['message']['content']


        # Bước 3: Tạo TTS
        print("🎙️ Tạo giọng đọc...")
        audio = self.text_to_speech(script, voice="Kore")  # Giọng nữ chuyên nghiệp


        # Lưu audio để user merge sau
        with open("mc_voice.mp3", "wb") as f:
            f.write(audio)
        print("💾 Đã lưu mc_voice.mp3")


        # Bước 4: Tạo video MC
        print("🎬 Tạo video MC...")
        video_prompt = f"A professional news anchor is presenting the news on television. {mc_description}. She is speaking confidently to the camera with professional hand gestures. Studio lighting, TV broadcast quality."


        video = self.generate_video_complete(
            video_prompt,
            model=model,
            image_base64=mc_image_base64
        )


        print("✅ Hoàn thành! Dùng Premiere/FFmpeg để ghép video + mc_voice.mp3")
        return video


    def analyze_and_summarize_web_content(
        self,
        topic: str,
        web_sources: List[str],
        model: str = "gemini-2.5-pro"
    ) -> str:
        """
        Phân tích và tổng hợp nội dung từ web
        (User cần crawl data trước, hàm này chỉ summarize)


        Args:
            topic: Chủ đề cần phân tích
            web_sources: List nội dung đã crawl từ web
            model: Model LLM


        Returns:
            Bản tổng hợp
        """
        combined_content = "\n\n---\n\n".join(web_sources)


        prompt = f"""
        Phân tích và tổng hợp thông tin về chủ đề: {topic}


        Dữ liệu từ các nguồn:
        {combined_content}


        Yêu cầu:
        1. Tổng hợp các thông tin chính
        2. Phân tích các điểm nổi bật
        3. Đưa ra kết luận


        Trình bày theo format markdown.
        """


        response = self.generate_text(prompt, model=model)
        return response['choices'][0]['message']['content']


    # =============================================
    # PHẦN 4: UTILITY FUNCTIONS
    # =============================================


    def save_image(self, image_data: Union[bytes, str], filename: str):
        """
        Lưu ảnh ra file


        Args:
            image_data: Bytes hoặc data URL (data:image/png;base64,...)
            filename: Tên file để lưu
        """
        if isinstance(image_data, str):
            # Convert data URL to bytes
            if ',' in image_data:
                _, encoded = image_data.split(',', 1)
            else:
                encoded = image_data
            image_bytes = base64.b64decode(encoded)
        else:
            image_bytes = image_data


        with open(filename, 'wb') as f:
            f.write(image_bytes)
        print(f"💾 Đã lưu: {filename}")


    def save_audio(self, audio_bytes: bytes, filename: str):
        """Lưu audio ra file"""
        with open(filename, 'wb') as f:
            f.write(audio_bytes)
        print(f"💾 Đã lưu: {filename}")


    def save_video(self, video_bytes: bytes, filename: str):
        """Lưu video ra file"""
        with open(filename, 'wb') as f:
            f.write(video_bytes)
        print(f"💾 Đã lưu: {filename}")


    def image_to_base64(self, image_path: str) -> str:
        """Chuyển ảnh sang base64"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')


    def base64_to_image(self, b64_string: str, filename: str):
        """Chuyển base64 sang ảnh"""
        image_bytes = base64.b64decode(b64_string)
        self.save_image(image_bytes, filename)




# =============================================
# EXAMPLE USAGE
# =============================================


if __name__ == "__main__":
    # Khởi tạo API
    api = AIThucChienAPI(api_key="your_api_key_here")


    # Example 1: Text generation
    print("\n=== Example 1: Text Generation ===")
    response = api.generate_text("Giải thích về AI trong 50 từ")
    print(response['choices'][0]['message']['content'])


    # Example 2: Image generation
    print("\n=== Example 2: Image Generation ===")
    images = api.generate_image("A beautiful sunset over the ocean", n=2)
    for i, img in enumerate(images):
        api.save_image(img, f"sunset_{i+1}.png")


    # Example 3: Consistent character comic
    print("\n=== Example 3: Comic with Consistent Character ===")
    comic_pages = api.create_comic_consistent(
        title="Cuộc phiêu lưu của Kenji",
        character_description="A young Japanese detective boy named Kenji, 10 years old, messy black hair, wearing round red glasses and a beige trench coat, anime style",
        panels=[
            {"scene": "He is reading a book in a library", "dialogue": "Hmm, interesting..."},
            {"scene": "He is chasing someone on a busy Tokyo street", "dialogue": "Stop right there!"},
        ]
    )


    # Example 4: Video generation
    print("\n=== Example 4: Video Generation ===")
    video = api.generate_video_complete(
        "A hummingbird flying in slow motion through a garden"
    )
    api.save_video(video, "hummingbird.mp4")


    # Example 5: Check spending
    print("\n=== Example 5: Check Spending ===")
    spending = api.check_spending()
    print(f"Đã chi tiêu: ${spending['info']['spend']}")
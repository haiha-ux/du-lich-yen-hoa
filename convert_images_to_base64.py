import json
import base64
import os

def get_image_mime_type(filepath):
    """Determine the MIME type of an image based on its extension."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.jpg' or ext == '.jpeg':
        return 'image/jpeg'
    elif ext == '.png':
        return 'image/png'
    elif ext == '.gif':
        return 'image/gif'
    else:
        return 'application/octet-stream' # Fallback

def file_to_base64(filepath):
    """Reads a file and converts it to a Base64 data URI."""
    try:
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            mime_type = get_image_mime_type(filepath)
            return f"data:{mime_type};base64,{encoded_string}"
    except FileNotFoundError:
        print(f"Warning: File not found at {filepath}. Skipping.")
        return None

def process_json_images(json_path, base_image_path):
    """
    Reads a JSON file, finds image URLs, converts them to Base64,
    and overwrites the JSON file with the updated data.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Process sections
    if 'sections' in data:
        for item in data['sections']:
            if 'imageUrl' in item and not item['imageUrl'].startswith('data:'):
                image_path = os.path.join(base_image_path, item['imageUrl'])
                base64_string = file_to_base64(image_path)
                if base64_string:
                    item['imageUrl'] = base64_string

    # Process attractions
    if 'attractions' in data:
        for item in data['attractions']:
            if 'imageUrl' in item and not item['imageUrl'].startswith('data:'):
                image_path = os.path.join(base_image_path, item['imageUrl'])
                base64_string = file_to_base64(image_path)
                if base64_string:
                    item['imageUrl'] = base64_string

    # Process gallery
    if 'gallery' in data:
        for item in data['gallery']:
            if 'url' in item and not item['url'].startswith('data:'):
                image_path = os.path.join(base_image_path, item['url'])
                base64_string = file_to_base64(image_path)
                if base64_string:
                    item['url'] = base64_string
    
    # Overwrite the original JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully updated {json_path} with Base64 image data.")

if __name__ == '__main__':
    json_file_path = os.path.join('backend', 'data', 'content.json')
    image_base_dir = os.path.join('backend', 'data')
    process_json_images(json_file_path, image_base_dir)

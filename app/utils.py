from flask import abort
import os, json, glob

MEDIA_DIR = "D:\Python Projects\PiMedia\media"

def get_media_data(category: str, id: str) -> dict:
    media_path = os.path.join(MEDIA_DIR, category, id, "info.json")

    if not os.path.exists(media_path):
        abort(404)

    # Open and read info.json
    with open(media_path, 'r') as file:
        data = json.load(file)
    data["id"] = id
    data["category"] = category
    return data

def get_media_data_by_category(category: str) -> list[dict]:
    if category not in ['movies', 'shows']:
        abort(404)

    result = []
    media_path = os.path.join(MEDIA_DIR, category)
    for id in os.listdir(media_path):
        data = get_media_data(category, id)
        result.append(data)
    return result

def validate_media_path(category: str, id: str) -> str:
    if category not in ['movies', 'shows']:
        abort(404)
    
    path = os.path.join(MEDIA_DIR, category, id)
    if not os.path.exists(path):
        abort(404)
    
    return path

def get_episodes(category: str, id: str) -> list[str]:
    media_path = validate_media_path(category, id)
    return [os.path.basename(mp4_file) for mp4_file in glob.glob(os.path.join(media_path, '*.mp4'))]

def check_media_file_exists(media_path: str, filename: str) -> str:
    file_path = os.path.join(media_path, filename)
    if not os.path.exists(file_path):
        abort(404)
    return file_path

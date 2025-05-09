from googleapiclient.discovery import build
import yt_dlp
import secrets
import os
import time
import json
import uuid
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Tải thông tin từ file .env
load_dotenv()

# Key admin và user
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
USER_API_KEY = os.getenv("USER_API_KEY")
TRIAL_API_KEY = os.getenv("TRIAL_API_KEY")
PERMANENT_API_KEY = os.getenv("PERMANENT_API_KEY")
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Đường dẫn tới file lưu các key
KEYS_FILE_PATH = 'keys.json'

# Lấy mã thiết bị duy nhất (MAC address)
def get_device_id():
    return str(uuid.getnode())

# Hàm tìm kiếm video Shorts từ YouTube API
def search_shorts(api_key, query, max_results=10):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=max_results,
        type="video",
        videoDuration="short",
        videoLicense="creativeCommon",
        videoDefinition="any"
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        videos.append((title, f"https://www.youtube.com/watch?v={video_id}"))

    return videos

# Hàm tải video
def download_videos(video_list, download_dir):
    ydl_opts = {
        'format': 'best[height<=1080]',
        'outtmpl': f'{download_dir}/%(title).80s.%(ext)s',
        'quiet': True,
    }

    for title, url in video_list:
        try:
            print(f"\U0001F4A1 Đang tải: {title}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"\u26A0\uFE0F Lỗi khi tải video {title}: {e}")

# Hiển thị thông tin tác giả
def show_author_info():
    print(r"""
REM .-------------------------------------------------------------------.
REM |      ________  ___  ___  ________  _____ ______                   |
REM |     |\   __  \|\  \|\  \|\   __  \|\   _ \  _   \                 |
REM |     \ \  \|\  \ \  \\\  \ \  \|\  \ \  \\\__\ \  \                |
REM |      \ \   ____\ \   __  \ \   __  \ \  \\|__| \  \               |
REM |       \ \  \___|\ \  \ \  \ \  \ \  \ \  \    \ \  \              |
REM |        \ \__\    \ \__\ \__\ \__\ \__\ \__\    \ \__\             |
REM |      ___\|__|  ___\|__|\|__|\|__|\|__|\|__|____ \|__|_____        |
REM |     |\   __  \|\  \|\  \    |\  \  /  /|\  ___ \|\___   ___\      |
REM |     \ \  \|\  \ \  \\\  \   \ \  \/  / | \   __/\|___ \  \_|      |
REM |      \ \  \\\  \ \  \\\  \   \ \    / / \ \  \_|/__  \ \  \       |
REM |       \ \  \\\  \ \  \\\  \   \/  /  /   \ \  \_|\ \  \ \  \      |
REM |        \ \_____  \ \_______\__/  / /      \ \_______\  \ \__\     |
REM |         \|___| \__\|_______|\___/ /        \|_______|   \|__|     |
REM |               \|__|        \|___|/                                |
REM '-------------------------------------------------------------------'
                      TOOL BY: PHAM QUYET
    """)
    print("\U0001F4CD From: Bắc Kạn, Việt Nam")
    print("\U0001F4E7 Contact: phamquyet3377@gmail.com")
    print("\U0001F919 Zalo: 0789257816 Phạm Quyết")
    print("=" * 60 + "\n")

# Kiểm tra dùng thử hết hạn (theo device_id lưu trong keys.json)
def is_trial_expired(trial_key):
    device_id = get_device_id()

    if os.path.exists(KEYS_FILE_PATH):
        with open(KEYS_FILE_PATH, 'r') as f:
            data = json.load(f)
    else:
        return False

    trial_data = data.get("trial_keys", {}).get(trial_key, {})
    start_time_str = trial_data.get("devices", {}).get(device_id)

    if not start_time_str:
        return False

    start_time = datetime.fromisoformat(start_time_str)
    return datetime.now() > start_time + timedelta(hours=1)

# Lưu thời gian bắt đầu dùng thử vào keys.json
def start_trial(trial_key):
    device_id = get_device_id()
    now = datetime.now().isoformat()

    if os.path.exists(KEYS_FILE_PATH):
        with open(KEYS_FILE_PATH, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    if "trial_keys" not in data:
        data["trial_keys"] = {}

    if trial_key not in data["trial_keys"]:
        data["trial_keys"][trial_key] = {"devices": {}}

    data["trial_keys"][trial_key]["devices"][device_id] = now

    with open(KEYS_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

# Tạo key mới cho admin
def generate_new_key():
    new_key = secrets.token_urlsafe(16)
    print(f"\u2705 Key mới được tạo: {new_key}")

    if os.path.exists(KEYS_FILE_PATH):
        with open(KEYS_FILE_PATH, 'r') as f:
            keys_data = json.load(f)
    else:
        keys_data = {}

    keys_data[new_key] = {"role": "user"}

    with open(KEYS_FILE_PATH, 'w') as f:
        json.dump(keys_data, f, indent=4)

    print(f"\u2705 Key mới đã được lưu vào {KEYS_FILE_PATH}")

# Xác thực API key và phân quyền
def get_api_key():
    user_input = input("Nhập API key: ").strip()

    if user_input == ADMIN_API_KEY:
        print("\u2705 Quyền Admin - Có thể tạo và quản lý key.")
        return "admin"
    elif user_input == USER_API_KEY:
        print("\u2705 Quyền User - Chỉ có thể tìm kiếm và tải video.")
        return "user"
    elif user_input == TRIAL_API_KEY:
        if is_trial_expired(user_input):
            print("\u26A0\uFE0F Thời gian dùng thử đã hết! Vui lòng mua key vĩnh viễn.")
            exit()
        else:
            print("\u2705 Dùng thử còn hiệu lực!")
            start_trial(user_input)
            return "trial"
    elif user_input == PERMANENT_API_KEY:
        print("\u2705 Sử dụng key vĩnh viễn!")
        return "permanent"
    else:
        if os.path.exists(KEYS_FILE_PATH):
            with open(KEYS_FILE_PATH, 'r') as f:
                keys_data = json.load(f)
                if user_input in keys_data:
                    role = keys_data[user_input].get("role", "user")
                    print(f"\u2705 Key hợp lệ từ file - Quyền: {role}")
                    return role
        print("\u26A0\uFE0F Key không hợp lệ!")
        exit()

# Quay lại menu chính
def go_back():
    input("\U0001F519 Nhấn Enter để quay lại...")

# Main chương trình
if __name__ == "__main__":
    show_author_info()
    user_role = get_api_key()

    if user_role == "admin":
        print("Admin có thể tạo key mới và quản lý thử nghiệm.")
        generate_new_key()
        go_back()

    while True:
        query = input("\U0001F50D Nhập từ khóa tìm kiếm (hoặc nhấn '`' để thoát): ").strip()
        if query.lower() == '`':
            print("\u26A0\uFE0F Đã thoát khỏi chương trình.")
            break

        while True:
            try:
                max_videos = int(input("\U0001F4E6 Nhập số lượng video muốn tải: "))
                if max_videos > 0:
                    break
                else:
                    print("\u26A0\uFE0F Phải lớn hơn 0.")
            except ValueError:
                print("\u26A0\uFE0F Vui lòng nhập số nguyên.")

        while True:
            download_dir = input("\U0001F4C1 Nhập đường dẫn thư mục để lưu video: ").strip()
            if os.path.exists(download_dir):
                break
            else:
                print("\u26A0\uFE0F Thư mục không tồn tại. Vui lòng kiểm tra lại.")

        videos = search_shorts(API_KEY, query, max_videos)
        print(f"\u2705 Tìm thấy {len(videos)} video hợp lệ.")
        download_videos(videos, download_dir)
        print("\u2705 Tải video thành công!")
        go_back()
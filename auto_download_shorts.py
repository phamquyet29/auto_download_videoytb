from googleapiclient.discovery import build
import yt_dlp
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY") 

def search_shorts(api_key, query, max_results=10):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=max_results,
        type="video",
        videoDuration="short",            # < 4 phút
        videoLicense="creativeCommon",   # Không bản quyền
        videoDefinition="any"
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        videos.append((title, f"https://www.youtube.com/watch?v={video_id}"))

    return videos

def download_videos(video_list, download_dir):
    ydl_opts = {
        'format': 'best[height<=1080]',
        'outtmpl': f'{download_dir}/%(title).80s.%(ext)s',
        'quiet': True,
    }

    for title, url in video_list:
        try:
            print(f"🔽 Đang tải: {title}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"⚠️ Lỗi khi tải video {title}: {e}")
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

    print("📍 From: Bắc Kạn, Việt Nam")
    print("📧 Contact: phamquyet3377@gmail.com")
    print("🤙 Zalo: 0789257816 Phạm Quyết")
    print("=" * 60 + "\n")
if __name__ == "__main__":
    show_author_info()
    # Nhập từ khóa
    query = input("🔍 Nhập từ khóa tìm kiếm: ").strip()
    
    # Nhập số lượng video
    while True:
        try:
            max_videos = int(input("📦 Nhập số lượng video muốn tải: "))
            if max_videos > 0:
                break
            else:
                print("⚠️ Phải lớn hơn 0.")
        except ValueError:
            print("⚠️ Vui lòng nhập số nguyên.")

    # Nhập thư mục lưu
    while True:
        download_dir = input("📁 Nhập đường dẫn thư mục để lưu video: ").strip()
        if os.path.exists(download_dir):
            break
        else:
            print("⚠️ Thư mục không tồn tại. Vui lòng kiểm tra lại.")

    # Tìm và tải video
    videos = search_shorts(API_KEY, query, max_videos)
    print(f"✅ Tìm thấy {len(videos)} video hợp lệ.")
    download_videos(videos, download_dir)

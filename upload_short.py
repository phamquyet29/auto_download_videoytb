import os
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ⚙️ Cấu hình
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRET_FILE = 'client_secret.json'
VIDEO_DIR = r"E:\video\videoshotsyt"
CATEGORY_ID = "10"  # "Music" (chọn tùy nội dung)
PRIVACY = "public"
WAIT_TIME_SECONDS = 300  # 5 phút

def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=8080)
    return build('youtube', 'v3', credentials=creds)

def seo_title(filename):
    base = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ")
    title = f"🎵 {base.title()} | #Shorts #funny #entertainment"
    return title[:100]  # YouTube giới hạn 100 ký tự

def seo_description(filename):
    base = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ")
    return (
        f"Relax and enjoy the vibe! 🌿\n\n"
        f"🎧 Title: {base.title()}\n"
        f"🔥 Watch entertainment videos on our channel!\n"
        f"\n"
        f"#shorts #funny #entertainment #humorous\n"
        f"\n"
        f"Subscribe 👉 https://www.youtube.com/@PleasureEntertainment-1"
    )[:5000]  # YouTube cho phép tối đa 5000 ký tự

def upload_video(youtube, video_path):
    filename = os.path.basename(video_path)

    request_body = {
        'snippet': {
            'title': seo_title(filename),
            'description': seo_description(filename),
            'tags': [
                'shorts', 'entertainment', 'humorous', 'lofi', 'study music',
                'chill vibes', 'instrumental', 'focus'
            ],
            'categoryId': CATEGORY_ID
        },
        'status': {
            'privacyStatus': PRIVACY,
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(video_path, resumable=True, mimetype='video/*')

    print(f"⬆️ Đang upload: {filename} ...")
    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )
    response = request.execute()
    print(f"✅ Đã upload: https://youtu.be/{response['id']}\n")

if __name__ == "__main__":
    if not os.path.exists(CLIENT_SECRET_FILE):
        print(f"⚠️ Không tìm thấy file {CLIENT_SECRET_FILE}. Hãy tải từ Google Cloud Console.")
        exit()

    youtube = authenticate_youtube()

    videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]
    if not videos:
        print("❌ Không tìm thấy video .mp4 nào trong thư mục.")
        exit()

    print(f"🔍 Tìm thấy {len(videos)} video trong thư mục: {VIDEO_DIR}")

    for index, video in enumerate(videos):
        video_path = os.path.join(VIDEO_DIR, video)
        try:
            upload_video(youtube, video_path)
        except Exception as e:
            print(f"⚠️ Lỗi khi upload {video}: {e}")

        if index < len(videos) - 1:
            print(f"⏳ Đợi {WAIT_TIME_SECONDS // 60} phút trước video tiếp theo...\n")
            time.sleep(WAIT_TIME_SECONDS)

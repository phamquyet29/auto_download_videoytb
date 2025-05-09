Hướng dẫn sử dụng Tool Tìm và Tải Video Shorts từ YouTube
Chào mừng bạn đến với tool Tìm và Tải Video Shorts từ YouTube! Tool này giúp bạn tìm kiếm và tải các video Shorts trên YouTube một cách dễ dàng.

Yêu cầu hệ thống
Python phiên bản 3.7 trở lên

Các thư viện Python (có thể cài đặt qua requirements.txt)

Cài đặt và sử dụng
Bước 1: Cài đặt Python
Đảm bảo rằng bạn đã cài đặt Python phiên bản 3.7 trở lên. Bạn có thể tải Python tại python.org.

Bước 2: Cài đặt các thư viện cần thiết
Sau khi cài đặt Python, mở terminal/command prompt và chạy lệnh sau để cài đặt các thư viện cần thiết:

bash
Sao chép
Chỉnh sửa
pip install -r requirements.txt
Bước 3: Cấu hình API key
Tạo một file .env trong thư mục chứa script.

Điền các thông tin API key vào file .env. Ví dụ:

env
Sao chép
Chỉnh sửa
ADMIN_API_KEY=abc123
USER_API_KEY=xyz456
TRIAL_API_KEY=trial789
PERMANENT_API_KEY=perm000
YOUTUBE_API_KEY=AIza...
Nếu bạn không có API key, bạn có thể tạo chúng từ Google Cloud Console cho YouTube API.

Bước 4: Chạy tool
Mở terminal/command prompt, di chuyển đến thư mục chứa file shorts_downloader.py và chạy lệnh sau:

bash
Sao chép
Chỉnh sửa
python shorts_downloader.py
Tool sẽ yêu cầu bạn nhập API key. Nếu bạn nhập đúng key, bạn sẽ có quyền truy cập vào các tính năng của tool.

Bước 5: Tìm và tải video Shorts
Nhập từ khóa tìm kiếm để tìm video Shorts.

Chọn số lượng video bạn muốn tải.

Nhập đường dẫn thư mục lưu video.

Tool sẽ tự động tải các video Shorts về thư mục bạn đã chọn.

Các tính năng
Tìm kiếm video Shorts: Cho phép tìm kiếm video Shorts theo từ khóa bạn nhập vào.

Tải video: Tải các video Shorts về máy tính.

Quản lý key người dùng: Có thể thêm key người dùng vào file keys.json để quản lý các quyền truy cập.

Thông tin thêm
Phiên bản thử nghiệm: Bạn có thể sử dụng tool miễn phí trong 1 giờ nếu sử dụng key dùng thử. Sau khi hết hạn, bạn sẽ cần mua key vĩnh viễn để tiếp tục sử dụng.

Liên hệ:

Email: phamquyet3377@gmail.com

Zalo: 0789257816 Phạm Quyết

Địa chỉ: Bắc Kạn, Việt Nam

Lưu ý
Đảm bảo rằng bạn có kết nối Internet khi chạy tool.

Nếu gặp vấn đề về API key hoặc tải video, hãy kiểm tra lại cấu hình trong file .env và thử lại.

import os
problem_folder="problems"
submission_folder="submissions"
time_limit=2
# Cấu hình thêm cho V1.1 C++
build_folder = "build"  # Nơi chứa các file .exe sau khi biên dịch
# --- TÍNH NĂNG MỚI V1.2: QUẢN LÝ NGƯỜI DÙNG ---
USERS = {
    "teacher1": {"password": "123", "role": "admin", "name": "Thầy Trung"},
    "hocsinhA": {"password": "abc", "role": "student", "name": "Nguyễn Hồng Huy"},
    "hocsinhB": {"password": "abc", "role": "student", "name": "Nguyễn Nhật Quốc"}
}
# --- TÍNH NĂNG MỚI V1.3: LƯU LỊCH SỬ CHẤM ---
history_file = "history.csv"

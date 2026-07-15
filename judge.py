# judge.py
import subprocess
import time
import os
import config

def compile_cpp(submission_path):
    """Biên dịch file C++ sang file thực thi (.exe). Trả về (Thành công, Đường dẫn file exe/Lỗi)"""
    os.makedirs(config.build_folder, exist_ok=True)
    
    # Lấy tên file không bao gồm đuôi (Ví dụ: baituanduy.cpp -> baituanduy)
    file_name = os.path.splitext(os.path.basename(submission_path))[0]
    
    # Đường dẫn file thực thi sau khi biên dịch
    if os.name == 'nt': # Nếu là Windows
        exe_path = os.path.join(config.build_folder, f"{file_name}.exe")
    else: # Nếu là Linux/macOS
        exe_path = os.path.join(config.build_folder, f"{file_name}.out")
        
    # Lệnh biên dịch C++ chuẩn: g++ submission.cpp -o build/filename.exe
    compile_cmd = ["g++", submission_path, "-o", exe_path]
    
    try:
        result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True, exe_path
        else:
            # Trả về lỗi biên dịch nếu g++ báo lỗi
            return False, result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "Quá thời gian biên dịch (Hơn 10 giây)."
    except FileNotFoundError:
        return False, "Không tìm thấy trình biên dịch 'g++' trên hệ thống. Vui lòng cài đặt hệ điều hành GCC/MinGW."

def run_single_test(submission_path, input_file_path, expected_output_path, exe_path=None):
    """Chạy một test case đơn lẻ (Hỗ trợ cả Python và C++)"""
    # Đọc dữ liệu test case
    with open(input_file_path, 'r', encoding='utf-8') as f:
        input_data = f.read()
    with open(expected_output_path, 'r', encoding='utf-8') as f:
        expected_output = f.read().strip()

    # Xác định lệnh chạy dựa trên loại ngôn ngữ
    if submission_path.endswith('.py'):
        cmd = ["python", submission_path]
    elif submission_path.endswith('.cpp'):
        if not exe_path:
            return "Compile Error", 0.0, "File chưa được biên dịch."
        cmd = [exe_path]
    else:
        return "System Error", 0.0, "Ngôn ngữ không được hỗ trợ."

    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=config.time_limit
        )
        execution_time = time.time() - start_time

        if result.returncode != 0:
            return "Runtime Error", execution_time, result.stderr.strip()

        user_output = result.stdout.strip()
        if user_output == expected_output:
            return "Correct", execution_time, "Khớp kết quả"
        else:
            return "Wrong Answer", execution_time, f"Nhận được: '{user_output[:20]}' nhưng mong đợi: '{expected_output[:20]}'"

    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        return "Time Limit Exceeded", execution_time, f"Vượt quá {config.time_limit}s"
    except Exception as e:
        return "System Error", 0.0, str(e)

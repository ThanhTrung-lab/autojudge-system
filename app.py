#Cập nhật mới nhé
import streamlit as st
import os
import pandas as pd
import zipfile
import shutil  # Thư viện hỗ trợ dọn dẹp thư mục cũ
from datetime import datetime
import config
from testcase import get_problem_list, validate_problem, get_test_cases, get_problem_description
from judge import run_single_test, compile_cpp

# --- ĐÃ NÂNG CẤP BẬC CAO: ÉP GIẢI NÉN KHI SỐ LƯỢNG TEST CASE TRONG FILE ZIP THAY ĐỔI ---
if os.path.exists("problems.zip"):
    hash_marker = "problems_extracted.txt"
    current_zip_time = str(os.path.getmtime("problems.zip"))
    
    need_extract = False
    
    # Kiểm tra điều kiện thời gian sửa đổi file zip
    if not os.path.exists(hash_marker) or not os.path.exists("problems"):
        need_extract = True
    else:
        with open(hash_marker, "r") as f:
            last_zip_time = f.read().strip()
        if last_zip_time != current_zip_time:
            need_extract = True
            
    # Chốt chặn phụ: Nếu file zip mới có số lượng file khác với số lượng test case cũ, ép giải nén luôn!
    if not need_extract and os.path.exists("problems"):
        try:
            with zipfile.ZipFile("problems.zip", 'r') as zip_ref:
                # Đếm tổng số file thực tế hiện tại trong thư mục problems (loại trừ thư mục rỗng)
                total_current_files = sum([len(files) for r, d, files in os.walk("problems")])
                # Đếm tổng số file thực tế trong file ZIP mới
                total_zip_files = len([f for f in zip_ref.namelist() if not f.endswith('/')])
                
                if total_current_files != total_zip_files:
                    need_extract = True
        except Exception:
            need_extract = True

    if need_extract:
        if os.path.exists("problems"):
            shutil.rmtree("problems")
            
        with zipfile.ZipFile("problems.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
            
        # Ghi lại dấu vết thời gian của file ZIP vừa giải nén thành công
        with open(hash_marker, "w") as f:
            f.write(current_zip_time)

# --- 1. ĐỔI TÊN HỆ THỐNG TRÊN TAB TRÌNH DUYỆT ---
st.set_page_config(page_title="T_Code V1.3", layout="wide")

# --- HÀM HELPER: LƯU KẾT QUẢ VÀO FILE CSV ---
def save_to_history(username, problem, score, correct, total, lang):
    new_data = pd.DataFrame([{
        "Tài khoản": username,
        "Bài làm": problem,
        "Điểm số": f"{score:.1f}%",
        "Kết quả": f"{correct}/{total}",
        "Ngôn ngữ": lang,
        "Thời gian chấm": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }])
    if os.path.exists(config.history_file):
        new_data.to_csv(config.history_file, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        new_data.to_csv(config.history_file, mode='w', header=True, index=False, encoding='utf-8-sig')

# --- KHỞI TẠO SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_info = {}

# --- GIAO DIỆN MÀN HÌNH ĐĂNG NHẬP (ĐÃ CẬP NHẬT TÊN MỚI) ---
if not st.session_state.logged_in:
    st.title("🔐 Đăng nhập hệ thống T_Code")
    col1, col2 = st.columns([1, 2])
    with col1:
        username = st.text_input("Tài khoản")
        password = st.text_input("Mật khẩu", type="password")
        btn_login = st.button("Đăng nhập", use_container_width=True)
        if btn_login:
            if username in config.USERS and config.USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_info = config.USERS[username]
                st.rerun()
            else:
                st.error("❌ Tài khoản hoặc mật khẩu không chính xác!")
    st.stop()

user_info = st.session_state.user_info

# Thanh Sidebar hiển thị thông tin học sinh/giáo viên
st.sidebar.markdown(f"### 👤 Xin chào, **{user_info['name']}**")
st.sidebar.info(f"Vai trò: `{user_info['role'].upper()}`")
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_info = {}
    st.rerun()
st.sidebar.write("---")

# ==========================================
# PHẦN GIAO DIỆN CHÍNH (ADMIN / STUDENT)
# ==========================================
if user_info["role"] == "admin":
    st.title("📋 Bảng quản lý của Giáo viên - T_Code")
    st.write("---")
    st.subheader("📊 Lịch sử chấm bài toàn hệ thống")
    if os.path.exists(config.history_file):
        df_history = pd.read_csv(config.history_file)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("Chưa có lịch sử chấm bài nào được lưu.")
else:
    # --- ĐỔI TÊN HỆ THỐNG TRÊN GIAO DIỆN CHÍNH CỦA HỌC SINH ---
    st.title("🖥️ Hệ thống chấm bài tự động - T_Code")
    st.write("---")

    st.sidebar.header("📁 Cấu hình chấm bài")
    problem_list = get_problem_list()
    if len(problem_list) == 0:
        st.sidebar.error("❌ Không tìm thấy đề bài nào (Hãy kiểm tra lại file ZIP).")
        st.stop()

    selected_problem = st.sidebar.selectbox("🎯 Chọn đề bài để chấm", problem_list)
    problem_path = os.path.join("problems", selected_problem)

    ok, message = validate_problem(problem_path)
    if not ok:
        st.sidebar.error(f"❌ {message}")
        st.stop()
    else:
        st.sidebar.success("✅ Cấu trúc đề hợp lệ.")

    test_cases = get_test_cases(problem_path)
    st.sidebar.info(f"📊 Tổng số test case: {len(test_cases)}")

    st.subheader(f"📝 Đề bài: {selected_problem}")
    problem_desc = get_problem_description(problem_path)
    st.markdown(
        f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 5px solid #007bff; margin-bottom: 20px;">
            {problem_desc}
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.write("---")

    st.subheader("📤 Nộp bài giải")
    uploaded_file = st.file_uploader(
        "Kéo thả file Python (.py) hoặc C++ (.cpp) của bạn vào đây", 
        type=["py", "cpp"],
        key=f"uploader_{selected_problem}"
    )

    if uploaded_file is not None:
        os.makedirs(config.submission_folder, exist_ok=True)
        file_ext = os.path.splitext(uploaded_file.name)[1]
        lang_type = "Python" if file_ext == ".py" else "C++"
        
        # --- THAY ĐỔI ĐỂ TÊN FILE NỘP BÀI MANG DẤU ẤN T_CODE (TÙY CHỌN) ---
        custom_filename = f"TCode_{st.session_state.username}_{selected_problem}{file_ext}"
        submission_path = os.path.join(config.submission_folder, custom_filename)
        
        with open(submission_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.success(f"📩 Đã nhận bài giải của bạn!")
        
        if st.button("🚀 Bắt đầu chấm bài"):
            exe_path = None
            if custom_filename.endswith('.cpp'):
                st.write("### ⚙️ Đang tiến hành biên dịch C++...")
                success, compile_message = compile_cpp(submission_path)
                if not success:
                    st.error("❌ Lỗi biên dịch (Compile Error)!")
                    st.code(compile_message, language="cpp")
                    st.stop()
                else:
                    st.success("✅ Biên dịch thành công!")
                    exe_path = compile_message
            
            st.write("### ⏳ Đang chạy các test case...")
            progress_bar = st.progress(0)
            results = []
            correct_count = 0
            
            for idx, (in_file, out_file) in enumerate(test_cases):
                in_path = os.path.join(problem_path, in_file)
                out_path = os.path.join(problem_path, out_file)
                
                status, exec_time, detail = run_single_test(submission_path, in_path, out_path, exe_path)
                if status == "Correct":
                    correct_count += 1
                    
                results.append({
                    "Test Case": in_file,
                    "Trạng thái": status,
                    "Thời gian (s)": round(exec_time, 3),
                    "Chi tiết": detail
                })
                progress_bar.progress((idx + 1) / len(test_cases))
                
            st.success("🎉 Đã chấm xong!")
            score_percentage = (correct_count / len(test_cases)) * 100
            
            save_to_history(st.session_state.username, selected_problem, score_percentage, correct_count, len(test_cases), lang_type)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Điểm số", f"{score_percentage:.1f}%")
            col2.metric("Số test đúng", f"{correct_count} / {len(test_cases)}")
            col3.metric("Kết quả chung", "PASSED" if correct_count == len(test_cases) else "FAILED")
            
            st.write("### 📋 Bảng kết quả chi tiết")
            df = pd.DataFrame(results)
            
            def color_status(val):
                if val == "Correct": return "background-color: #d4edda; color: #155724;"
                elif val == "Wrong Answer": return "background-color: #f8d7da; color: #721c24;"
                elif val == "Time Limit Exceeded": return "background-color: #fff3cd; color: #856404;"
                return "background-color: #e2e3e5; color: #383d41;"
                
            st.dataframe(df.style.map(color_status, subset=['Trạng thái']), use_container_width=True)

    st.write("---")
    st.subheader("📜 Lịch sử các lần nộp bài của bạn")
    if os.path.exists(config.history_file):
        df_all_history = pd.read_csv(config.history_file)
        df_user_history = df_all_history[df_all_history["Tài khoản"] == st.session_state.username]
        if not df_user_history.empty:
            st.dataframe(df_user_history.iloc[::-1], use_container_width=True)
        else:
            st.info("Bạn chưa nộp bài lần nào.")
    else:
        st.info("Hệ thống chưa ghi nhận lịch sử chấm bài nào.")
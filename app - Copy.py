# app.py
import streamlit as st
import os
import zipfile
# --- MẸO TỰ ĐỘNG GIẢI NÉN THƯ MỤC PROBLEMS KHI DEPLOY INTERNET ---
if os.path.exists("problems.zip") and not os.path.exists("problems"):
    with zipfile.ZipFile("problems.zip", 'r') as zip_ref:
        zip_ref.extractall(".")
import pandas as pd
from datetime import datetime
import config
from testcase import get_problem_list, validate_problem, get_test_cases, get_problem_description
from judge import run_single_test, compile_cpp

st.set_page_config(page_title="AutoJudge V1.3", layout="wide")

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
    
    # Nếu file đã tồn tại thì append vào, nếu chưa thì tạo mới kèm header
    if os.path.exists(config.history_file):
        new_data.to_csv(config.history_file, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        new_data.to_csv(config.history_file, mode='w', header=True, index=False, encoding='utf-8-sig')

# --- KHỞI TẠO SESSION STATE ĐỂ LƯU TRẠNG THÁI ĐĂNG NHẬP ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_info = {}

# --- GIAO DIỆN MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.title("🔐 Đăng nhập hệ thống AutoJudge")
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

# Thanh Sidebar chung
st.sidebar.markdown(f"### 👤 Xin chào, **{user_info['name']}**")
st.sidebar.info(f"Vai trò: `{user_info['role'].upper()}`")
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_info = {}
    st.rerun()
st.sidebar.write("---")

# ==========================
# PHẦN 1: GIAO DIỆN GIÁO VIÊN (ADMIN)
# ==========================
if user_info["role"] == "admin":
    st.title("📋 Bảng quản lý của Giáo viên")
    st.write("---")
    
    # Hiển thị Lịch sử chấm bài của TOÀN BỘ học sinh
    st.subheader("📊 Lịch sử chấm bài toàn hệ thống")
    if os.path.exists(config.history_file):
        df_history = pd.read_csv(config.history_file)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("Chưa có lịch sử chấm bài nào được lưu.")
        
    st.write("---")
    st.subheader("📁 Danh sách file bài nộp chi tiết")
    sub_dir = config.submission_folder
    if os.path.exists(sub_dir) and len(os.listdir(sub_dir)) > 0:
        files = os.listdir(sub_dir)
        sub_data = []
        for f in files:
            path = os.path.join(sub_dir, f)
            sub_data.append({
                "Tên file bài nộp": f,
                "Kích thước (Bytes)": os.path.getsize(path),
                "Thời gian nộp": pd.to_datetime(os.path.getmtime(path), unit='s').strftime('%d/%m/%Y %H:%M:%S')
            })
        st.dataframe(pd.DataFrame(sub_data), use_container_width=True)
    else:
        st.info("Hiện tại chưa có học sinh nào nộp bài.")

# ==========================
# PHẦN 2: GIAO DIỆN HỌC SINH (STUDENT)
# ==========================
else:
    st.title("🖥️ Hệ thống chấm bài tự động - AutoJudge")
    st.write("---")

    st.sidebar.header("📁 Cấu hình chấm bài")
    problem_list = get_problem_list()
    if len(problem_list) == 0:
        st.sidebar.error("❌ Không tìm thấy đề bài nào.")
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

    # Hiển thị Đề bài
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

    # Khu vực Nộp bài giải
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
        custom_filename = f"{st.session_state.username}_{selected_problem}{file_ext}"
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
            
            # Tính toán điểm số
            score_percentage = (correct_count / len(test_cases)) * 100
            
            # --- TÍNH NĂNG MỚI: TỰ ĐỘNG LƯU KẾT QUẢ VÀO CSV ---
            save_to_history(
                st.session_state.username, 
                selected_problem, 
                score_percentage, 
                correct_count, 
                len(test_cases), 
                lang_type
            )
            
            # Thống kê trên giao diện
            col1, col2, col3 = st.columns(3)
            col1.metric("Điểm số", f"{score_percentage:.1f}%")
            col2.metric("Số test đúng", f"{correct_count} / {len(test_cases)}")
            col3.metric("Kết quả chung", "PASSED" if correct_count == len(test_cases) else "FAILED")
            
            # Bảng chi tiết lượt chấm hiện tại
            st.write("### 📋 Bảng kết quả chi tiết")
            df = pd.DataFrame(results)
            
            def color_status(val):
                if val == "Correct": return "background-color: #d4edda; color: #155724;"
                elif val == "Wrong Answer": return "background-color: #f8d7da; color: #721c24;"
                elif val == "Time Limit Exceeded": return "background-color: #fff3cd; color: #856404;"
                elif val == "Compile Error": return "background-color: #f8d7da; color: #721c24; font-weight: bold;"
                return "background-color: #e2e3e5; color: #383d41;"
                
            st.dataframe(df.style.applymap(color_status, subset=['Trạng thái']), use_container_width=True)

    # --- TÍNH NĂNG MỚI: HIỂN THỊ LỊCH SỬ CHẤM CỦA RIÊNG HỌC SINH ĐANG ĐĂNG NHẬP ---
    st.write("---")
    st.subheader("📜 Lịch sử các lần nộp bài của bạn")
    if os.path.exists(config.history_file):
        df_all_history = pd.read_csv(config.history_file)
        # Lọc chỉ lấy các dòng thuộc về học sinh hiện tại
        df_user_history = df_all_history[df_all_history["Tài khoản"] == st.session_state.username]
        
        if not df_user_history.empty:
            # Sắp xếp lịch sử mới nhất lên đầu
            df_user_history = df_user_history.iloc[::-1]
            st.dataframe(df_user_history, use_container_width=True)
        else:
            st.info("Bạn chưa nộp bài lần nào.")
    else:
        st.info("Hệ thống chưa ghi nhận lịch sử chấm bài nào.")
        
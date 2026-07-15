import os
def get_problem_list():
    if not os.path.exists("problems"):
        return []
    folders=[]
    for item in os.listdir("problems"):
        path=os.path.join("problems", item)
        if os.path.isdir(path):
            folders.append(item)
    folders.sort()
    return folders
def validate_problem(problem_path):

    files = os.listdir(problem_path)
    input_files = sorted([f for f in files if f.startswith("input")])
    output_files = sorted([f for f in files if f.startswith("output")])
    if len(input_files) == 0:
        return False, "Không có file Input nào."
    if len(output_files) == 0:
        return False, "Không có file Output nào."
    if len(input_files) != len(output_files):
        return False, f"Số lượng file không khớp (Có {len(input_files)} input nhưng có {len(output_files)} output)."
    
    return True, "Cấu trúc đề hợp lệ."
def get_test_cases(problem_path):
    """Trả về danh sách các bộ test dạng tuple: (file_input, file_output)"""
    files = os.listdir(problem_path)
    input_files = sorted([f for f in files if f.startswith("input")])
    output_files = sorted([f for f in files if f.startswith("output")])
    return list(zip(input_files, output_files))

def get_problem_description(problem_path):
    """Đọc nội dung file đề bài (ưu tiên debai.md, nếu không có thì tìm debai.txt)"""
    md_path = os.path.join(problem_path, "debai.md")
    txt_path = os.path.join(problem_path, "debai.txt")
    
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            return f.read()
    elif os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
 
    return "⚠️ *Bài này hiện chưa có nội dung đề bài cụ thể.*"  

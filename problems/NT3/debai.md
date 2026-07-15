Bài 3. Truy vấn nguyên tố
Hệ thống quản lý dữ liệu quốc gia cần kiểm tra tính xác thực của các mã định danh. Một trong những tiêu chuẩn để đánh giá mã số an toàn là kiểm tra xem mã số đó có phải là số nguyên tố hay không. Vì số lượng mã số cần kiểm tra trong một ngày là rất lớn, hệ thống đòi hỏi một chương trình có khả năng phản hồi kết quả cực nhanh.
Yêu cầu: Cho số nguyên dương N và Q truy vấn. Với mỗi truy vấn, cho một số nguyên dương x (x≤N), hãy cho biết x có phải là số nguyên tố hay không.
Dữ liệu vào (Từ file PRIME_QRY.INP)
- Dòng đầu tiên chứa hai số nguyên dương N và Q (1≤N,Q≤10^6).
- Q dòng tiếp theo, mỗi dòng chứa một số nguyên dương x cần kiểm tra (1≤x≤N).
Kết quả (Ghi ra file PRIME_QRY.OUT)
- Với mỗi truy vấn, in ra YES nếu x là số nguyên tố, ngược lại in ra NO.


Ví dụ

PRIME_QRY.INP

10 3
2
4
7

PRIME_COUNT.OUT

YES
NO
YES
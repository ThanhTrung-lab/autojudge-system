NT11. Ước nguyên tố lớn nhất
Với mỗi số nguyên dương n > 1, ta gọi LPF(n) là ước số nguyên tố lớn nhất của n.
Ví dụ:
- LPF(6) = 3 (vì các ước nguyên tố là 2 và 3).
- LPF(20) = 5 (vì 20 = 2^2 × 5).
- LPF(13) = 13 (vì 13 là số nguyên tố).
Yêu cầu: Cho Q truy vấn, mỗi truy vấn là một số nguyên dương x. Hãy tìm LPF(x) cho mỗi truy vấn đó.
Dữ liệu vào (Từ file MAXPRIME.INP)
- Dòng đầu tiên chứa số nguyên dương Q (1 ≤ Q ≤ 10^5).
- Q dòng tiếp theo, mỗi dòng chứa một số nguyên dương x (2 ≤ x ≤ 10^6).
3. Kết quả (Ghi ra file MAXPRIME.OUT)
Với mỗi truy vấn, in ra giá trị LPF(x) trên một dòng.


Ví dụ

MAXPRIME.INP

4

10

12

31

49


MAXPRIME.OUT

5

3

31

7
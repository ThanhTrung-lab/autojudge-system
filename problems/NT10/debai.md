NT10. Cặp nguyên tố có khoảng cách k
Trong toán học, các cặp số nguyên tố có khoảng cách cố định luôn là đề tài nghiên cứu hấp dẫn.
- Khi k=2, các cặp (p, p+2) được gọi là Số nguyên tố sinh đôi (Twin Primes).
- Khi k=4, các cặp (p, p+4) được gọi là Số nguyên tố họ hàng (Cousin Primes).
- Khi k=6, các cặp (p, p+6) được gọi là Số nguyên tố quyến rũ (Sexy Primes).
Yêu cầu: Cho số nguyên dương N và số nguyên dương k. Hãy đếm xem có bao nhiêu cặp số nguyên tố (p, q) thỏa mãn đồng thời các điều kiện sau:
1.	p và q đều là số nguyên tố.
2.	q - p = k.
3.	q ≤ N.
Dữ liệu vào (Từ file PRIMEK.INP)
Một dòng duy nhất chứa hai số nguyên dương N và k (1 ≤ k < N ≤ 10^6).
Kết quả (Ghi ra file PRIMEK.OUT)
Ghi một số nguyên duy nhất là số lượng cặp số nguyên tố tìm được.


Ví dụ

PRIMEK.INP

10 2

20 4

20 6


PRIMEK.OUT

2

3

4
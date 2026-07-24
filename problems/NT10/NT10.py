# NT10. Cặp nguyên tố có khoảng cách k
def Era(n):
    if n<2:
        return False
    f=[True ]*(n+1)
    f[0]=f[1]=False
    for i in range(4,n+1,2):
        f[i]=False
    p=3
    while p*p<=n:
        if f[p]:
            for i in range(p*p,n+1,2*p):
                f[i]=False
        p+=2
    return f
def xuly(n,k):
    if n<=k:
        return 0
    f=Era(n)
    cnt=0
    for p in range(2,n-k+1):
        if f[p] and f[p+k]:
            cnt+=1
    return cnt
'''n=20
k=4
print(xuly(n,k))'''

n,k=map(int,input().split())
kq=xuly(n,k)
print(kq)
'''with open('output5.txt',mode='w',encoding='utf-8') as fo:
    fo.write(str(kq))'''
    
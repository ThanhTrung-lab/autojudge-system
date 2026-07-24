import sys
def Era(n):
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
    return [i for i in range(n+1) if f[i]]
def doc_ghi():
    n=int(input())
    kq=Era(n)
    sys.stdout.write(str(len(kq)))
doc_ghi()
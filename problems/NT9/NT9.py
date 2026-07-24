#Bài 9 Bán số nguyên tố
def Era(n):
    if n<2:
        return False
    f=[True]*(n+1)
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
def xuly(n):
    if n<4:
        return 0
    f=Era(n)
    l=0
    r=len(f)-1
    cnt=0
    while l<=r:
        while l<=r and f[l]*f[r]>n:
            r-=1
        if l<=r:
            cnt+=(r-l+1)
            l+=1
    return cnt
        
n=int(input())
print(xuly(n))

'''n=99999
with open("output5.txt",mode='w',encoding="utf-8") as fo:
    kq=xuly(n)
    fo.write(str(kq))'''

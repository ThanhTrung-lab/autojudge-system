def Era(n):
    f=[True ]*(n+1)
    f[0]=f[1]=False
    for i in range(4,n+1,2):
        f[i]=False
    p=3
    while p*p<=n:
        if f[p]:
            for j in range(p*p,n+1,2*p):
                f[j]=False
        p+=2
    return f
def xuly(n):
    if n<6:
        return 0
    f=Era(n)
    v=[0]*(n+1)
    for i in range(2,n//2+1):
        if f[i]:
            for j in range(i,n+1,i):
                v[j]+=1
    cnt=0
    for x in v:
        if x==2:
            cnt+=1
    return cnt
def doc_ghi():
    import sys
    n=int(sys.stdin.read())
    ans=xuly(n)
    sys.stdout.write(str(ans))
doc_ghi()
    
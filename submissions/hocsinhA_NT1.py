def sang_NT(n):
    f=[True]*(n+1)
    f[0]=f[1]=False
    for i in range(4,n+1,2):
        f[i]=False
    p=3
    while p*p<=n:
        if f[p]:
            for i in range(p*p,n+1,p):
                f[i]=False
        p+=1
    res=[i for i in range(2,n+1) if f[i]==True]
    return res
n=int(input())
kq=sang_NT(n)
print(*kq)
        
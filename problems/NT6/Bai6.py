def SPF(n):
    f=[i for i in range(n+1)]
    for i in range(4,n+1,2):
        f[i]=2
    p=3
    while p*p<=n:
        if f[p]==p:
            for i in range(p*p,n+1,2*p):
                if f[i]==i:
                    f[i]=p
        p+=2
    return f[1:]
n=int(input())
kq=SPF(n)
print(*kq)

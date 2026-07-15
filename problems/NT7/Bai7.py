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
    return f
def xuly(q):
    f=SPF(max(q))
    kq=[]
    for x in q:
        res=[]
        while x>1:
            res.append(f[x])
            x//=f[x]
        kq.append(' '.join(map(str,res)))
    print('\n'.join(kq))
q=[12,31,100]
xuly(q)
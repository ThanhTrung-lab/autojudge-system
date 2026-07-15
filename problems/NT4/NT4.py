import sys
def Era(n):
    n=max(n,1)
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
    return f
def xuly():
    try:
        with open("input5.txt",mode="r") as fi:
            data=fi.read().split()
    except FileNotFoundError:
        return
    if not data:
        return
    n=int(data[0])
    q=int(data[1])
    max_r=0
    query=[]
    idx=2
    for _ in range(q):
        x=int(data[idx])
        y=int(data[idx+1])
        idx+=2
        L=max(1,x)
        R=max(1,y)
        query.append((L,R))
        max_r=max(max_r,R)
    f=Era(max_r)
    v=[0]*len(f)
    for i in range(2,len(f)):
        v[i]=v[i-1]+(1 if f[i] else 0)
    res=[]
    for L, R in query:
        if L>R:
            res.append('0')
        else:
            ans=v[R]-v[L-1]
            res.append(str(ans))
    with open('output5.txt',mode='w') as fo:
        fo.write("\n".join(res)+"\n")
xuly()

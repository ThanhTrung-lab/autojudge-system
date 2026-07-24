def spf(n):
    f=[i for i in range(n+1)]
    for i in range(4,n+1,2):
        f[i]=2
    p=3
    while p*p<=n:
        if f[p]==p:
            for j in range(p*p,n+1,2*p):
                if f[j]==j:
                    f[j]=p
        p+=2
    return f
def xuly(n):
    if n<4:
        return 0
    f=spf(n)
    ans=0
    for x in range(4,n+1):
        cnt=0
        while x>1:
            cnt+=1
            x//=f[x]
        if cnt==2:
            ans+=1
    return ans
n=int(input())
print(xuly(n))
    
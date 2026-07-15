def Era(n):
    if n<=1:
        return [False]*(n+1)
    f=bytearray([1])*(n+1)
    f[0]=f[1]=0
    for i in range(4,n+1,2):
        f[i]=0
    p=3
    while p*p<=n:
        if f[p]:
            for i in range(p*p,n+1,2*p):
                f[i]=0
        p+=2
    return f
def xuly(n):
    if n<=3:
        return 0
    f=Era(n)
    if n%2!=0:
        if f[n-2]:
            return 1
        else:
            return 0
    cnt=0
    for i in range(2,n//2+1):
        if f[i] and f[n-i]:
            cnt+=1
    return cnt
n=int(input())
print(xuly(n))
    
        
    
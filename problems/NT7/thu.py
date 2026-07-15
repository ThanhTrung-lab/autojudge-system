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
    return f
def xuly(a):
    f=Era(max(a))
    output=[]
    for x in a:
        if x<=3:
            output.append("-1")
            continue
        if x%2!=0:
            if f[x-2]:
                output.append(f"{2} {x-2}")
            else:
                output.append("-1")
            continue
        for i in range(2,x//2+1):
            if f[i] and f[x-i]:
                #res.append(i)
                #res.append(x-i)
                output.append(' '.join(map(str,[i,x-i])))
                break
    print(' '.join(output))
    print(output)
a=[2,4,10,17]
xuly(a)
            
        
        
    
def Sang_NT(n):
    if n<=1:
        return []
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
def xuly(a):
    #g=open('output5.txt',mode='w')
    b=[x for x in a if x>0]
    max_b=max(b) if b else 1
    f=Sang_NT(max_b)
    for x in a:
        if x<=1:
            print("NO")
        elif x<=max_b:
            if f[x]:
                print("YES")
            else:
                print("NO")
    #g.close()

'''def docdl():
    f=open('input5.txt',mode='r')
    n,x=map(int,f.readline().split())
    a=list(map(int,f.read().split()))
    f.close()
    return n,x,a
n,x,a=docdl()'''
n,x=map(int,input().split())
a=list(map(int,input().split()))
xuly(a)
            
        
    
    
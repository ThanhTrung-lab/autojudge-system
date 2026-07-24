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
    return kq
    '''print('\n'.join(kq))
q=[12,31,100]
xuly(q)'''

'''def doc_ghi():
    with open('input5.txt','r') as fi:
        data=fi.read().split()
        q=int(data[0])
        a=list(map(int,data[1:q+1]))
    with open('output5.txt','w') as fo:
        kq=xuly(a)
        fo.write('\n'.join(kq))
doc_ghi()'''
import sys
def doc_ghi():
    data=sys.stdin.read().split()
    if not data:
        return
    q=int(data[0])
    a=list(map(int,data[1:q+1]))
    kq=xuly(a)
    sys.stdout.write('\n'.join(kq))
doc_ghi()
    
    
    
    
    


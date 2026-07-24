import sys
def lpf(n):
    f=[0]*(n+1)
    for i in range(2,n+1):
        if f[i]==0:
            for j in range(i,n+1,i):
                f[j]=i
    return f
def xuly(q,a):
    if q<1 or not a:
        return []
    f=lpf(max(a))
    res=[]
    for x in a:
        if x<=1:
            res.append(x)
        else:
            res.append(f[x])
    return res
def doc_ghi():
    data=sys.stdin.read().split()
    if not data:
        return 
    q=int(data[0])
    a=list(map(int,data[1:q+1]))
    kq=xuly(q,a)
    sys.stdout.write('\n'.join(map(str,kq))+'\n')
doc_ghi()

'''with open('input1.txt','r') as fi:
    input=list(map(int,fi.read().split()))
    q=input[0]
    a=input[1:q+1]
kq=xuly(q,a)
print(kq)
with open('output.txt','w') as fo:
    fo.write('\n'.join(map(str,kq)))'''
'''q=6
a=[10,12,31,49,1,-2]
print(xuly(q,a))'''

    
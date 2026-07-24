#Bài 8. Số có đúng 2 ước nguyên tố
def Song_to(n):
    if n<6:
        return 0
    
    v=[0]*(n+1)
    for i in range(2,n+1):
        if v[i]==0:
            for j in range(i,n+1,i):
                v[j]+=1
    res=[]
    for i in range(len(v)):
        if v[i]==2:
            res.append(i)
    return res

n=int(input())
kq=Song_to(n)
print(len(kq))
#print(*kq)

        
    
import random
q=10**5
a=[q]
for _ in range(q):
    a.append(random.randint(2,1000000))
with open('input5.txt','w') as fo:
    fo.write('\n'.join(map(str,a)))
    
    
import random
n=100000
a=[n]
for _ in range(n):
    a.append(random.randint(1,1000000))
with open('input5.txt','w') as fo:
    fo.write('\n'.join(map(str,a)))
    
    
import random
q=4
a=[]
for _ in range(q):
    a.append(random.randint(2,100))
with open('input.txt','w') as fo:
    fo.write('\n'.join(map(str,a)))
    
    
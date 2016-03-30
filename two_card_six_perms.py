

lis = []
for i in range(6):
    for j in range(6):
        lis.append(sorted([i+1, j+1]))

lis=sorted(lis)

lis2 =[]
for i in lis:
    if i not in lis2:
        lis2.append(i)
    #print(i[0],i[1])

lis2=sorted(lis2)

for i in lis2:
    print(i[0],i[1])

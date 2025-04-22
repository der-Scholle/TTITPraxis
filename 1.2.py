a = [2,5,2,1,2]
t = 5
r = []
a.sort()

for i in range(len(a)):
    if a[i] > t: continue
    if a[i] == t:
        if [a[i]] not in r: r.append([a[i]])
        continue
    for j in range(i+1, len(a)):
        if a[i]+a[j] > t: continue
        if a[i]+a[j] == t:
            c = sorted([a[i],a[j]])
            if c not in r: r.append(c)
            continue
        for k in range(j+1, len(a)):
            if a[i]+a[j]+a[k] > t: continue
            if a[i]+a[j]+a[k] == t:
                c = sorted([a[i],a[j],a[k]])
                if c not in r: r.append(c)

print(r)

a = [10,1,2,7,6,1,5]
t = 8
r = []
a.sort()

for i in range(len(a)):
    if a[i] > t: continue
    if a[i] == t:
        if [a[i]] not in r: r.append([a[i]])
        continue
    for j in range(i+1, len(a)):
        if a[i]+a[j] > t: continue
        if a[i]+a[j] == t:
            c = sorted([a[i],a[j]])
            if c not in r: r.append(c)
            continue
        for k in range(j+1, len(a)):
            if a[i]+a[j]+a[k] > t: continue
            if a[i]+a[j]+a[k] == t:
                c = sorted([a[i],a[j],a[k]])
                if c not in r: r.append(c)

print(r)
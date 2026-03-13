s = int(input())
g = int(input())

for i in range(g):
        s += s*s*(s-1)**g
        print(s*s*(s-1)**g)
print(s)
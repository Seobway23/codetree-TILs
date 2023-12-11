n, m = input().split() # n 비트, m 밑
m = int(m)

sum = 0
t = 0
for i in range(len(n) - 1, -1, -1):
    num = int(i)
    sum +=  int(n[num]) * (m ** t)
    t += 1
    # print(num, t, sum)

print(sum)
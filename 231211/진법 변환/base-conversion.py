n, m = input().split()

# string이 나오면 숫자로 바꾸기
if m.isdigit():
    m = int(m)
else:
    m = ord(m) - 55

#메인 로직
N, sum, up = len(n), 0, 0
for i in range(N-1, -1, -1):
    bit = int(n[i])
    sum += bit * ( m ** up) 
    up += 1
    # print(sum, up, bit)

print(sum)
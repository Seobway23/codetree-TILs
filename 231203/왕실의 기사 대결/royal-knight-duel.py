'''
L X L 체스판 대결 준비
체스판의 왼쪽 상단 1,1 시작
빈칸, 함정, 벽(밖도 벽으로 간주)

왕실의 기사들은 자신의 마력으로 상대방 밀침
초기 위치 r, c

r,c 를 좌측 상단으로 하며 h x w 크기의 직사각형 형태 띔

# 기사 이동
왕 명령 -> 상하좌우 중 한 칸 이동 가능
기사 이동하면 연쇄적으로 한 칸 밀려나게 됨
하지만, 밀리는 중에 벽이 있으면 못 움직임 (산타랑 다름)
체스판에서 사라진 기사 -> 명령 X

# 대결 대미지 
밀치면 밀친 만큼 피해
대미지 = 함정수( h x w 안)
if 기사 체력 - 대미지 < 0:
    기사 사라짐

명령 받은 기사는 피해 X
밀렸더라도, 밀쳐진 위치에 함정이 없으면 피해 X 

'''

# import sys
# sys.stdin = open("input.txt")

from collections import deque

# 전역 변수들을 정의
MAX_N = 31
MAX_L = 41
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

info = [[0 for _ in range(MAX_L)] for _ in range(MAX_L)]
bef_k = [0 for _ in range(MAX_N)]
r = [0 for _ in range(MAX_N)]
c = [0 for _ in range(MAX_N)]
h = [0 for _ in range(MAX_N)]
w = [0 for _ in range(MAX_N)]
k = [0 for _ in range(MAX_N)]
nr = [0 for _ in range(MAX_N)]
nc = [0 for _ in range(MAX_N)]
dmg = [0 for _ in range(MAX_N)]
is_moved = [False for _ in range(MAX_N)]


# 움직임을 시도
def try_movement(idx, dir):
    q = deque()
    is_pos = True

    # 초기화 작업
    for i in range(1, n + 1):
        dmg[i] = 0
        is_moved[i] = False
        nr[i] = r[i]
        nc[i] = c[i]

    q.append(idx)
    is_moved[idx] = True

    while q:
        x = q.popleft()

        nr[x] += dx[dir]
        nc[x] += dy[dir]

        # 경계를 벗어나는지 체크
        if nr[x] < 1 or nc[x] < 1 or nr[x] + h[x] - 1 > l or nc[x] + w[x] - 1 > l:
            return False

        # 대상 조각이 다른 조각이나 장애물과 충돌하는지 검사
        for i in range(nr[x], nr[x] + h[x]):
            for j in range(nc[x], nc[x] + w[x]):
                if info[i][j] == 1:
                    dmg[x] += 1
                if info[i][j] == 2:
                    return False

        # 다른 조각과 충돌하는 경우, 해당 조각도 같이 이동
        for i in range(1, n + 1):
            if is_moved[i] or k[i] <= 0:
                continue
            if r[i] > nr[x] + h[x] - 1 or nr[x] > r[i] + h[i] - 1:
                continue
            if c[i] > nc[x] + w[x] - 1 or nc[x] > c[i] + w[i] - 1:
                continue

            is_moved[i] = True
            q.append(i)

    # 모든 기사들이 이동할 수 있는지 확인
    for i in range(1, n + 1):
        if is_moved[i] and (nr[i] < 1 or nc[i] < 1 or nr[i] + h[i] - 1 > l or nc[i] + w[i] - 1 > l):
            return False
    # ,애초에 얘가 필요 없음 

    dmg[idx] = 0
    return True


# 특정 조각을 지정된 방향으로 이동시키는 함수
def move_piece(idx, move_dir):
    if k[idx] <= 0:
        return

    # 이동이 가능한 경우, 실제 위치와 체력을 업데이트
    if try_movement(idx, move_dir):
        for i in range(1, n + 1):
            r[i] = nr[i]
            c[i] = nc[i]
            k[i] -= dmg[i]


# 입력값
l, n, q = map(int, input().split())
for i in range(1, l + 1):
    info[i][1:] = map(int, input().split())
for i in range(1, n + 1):
    r[i], c[i], h[i], w[i], k[i] = map(int, input().split())
    bef_k[i] = k[i]

for _ in range(q):
    idx, d = map(int, input().split())
    move_piece(idx, d)

# 결과를 계산하고 출력
ans = sum([bef_k[i] - k[i] for i in range(1, n + 1) if k[i] > 0])
print(ans)
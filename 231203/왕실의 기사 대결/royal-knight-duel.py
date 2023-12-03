from collections import deque

# 전역 변수 관리
MAX_N = 31
MAX_L = 41
dx, dy = [-1,0,1,0], [0,1,0,-1]

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

# 움직임 시도
# 움직여지면 true, 아니면 false

def try_movement(idx, dir):
    # 큐로 관리
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

    # 큐
    while q:
        x = q.popleft()
        nr[x] += dx[dir]
        nc[x] += dy[dir]

        # 경계 체크
        if nr[x] <1 or nc[x] < 1 or nr[x] + h[x] - 1 > l or nc[x] + w[x] -1 > l:
            return False
        
        # 벽, 장애물 충돌 검사
        for i in range(nr[x], nr[x] + h[x]):
            for j in range(nc[x], nc[x] + w[x]):
                if info[i][j] == 1:
                    dmg[x] += 1
                elif info[i][j] == 2:
                    return False
        
        # 다른 조각 충돌, 해당 조각 같이 이동
        for i in range(1, n + 1):
            # 움직였거나, 체력이 없을 때
            if is_moved[i] or k[i] <= 0:
                continue
            # 범위 벗어나면 continue
            if r[i] > nr[x] + h[x] -1 or nr[x] >r[i] + h[i] - 1:
                continue
            if c[i] > nc[x] + w[x] -1 or nc[x] > c[i] + w[i] -1:
                continue
            
            is_moved[i] = True
            q.append(i)
    
    dmg[idx] = 0
    return True


# 지정된 방향으로 이동시킴
def move_piece(idx, move_dir):
    if k[idx] <= 0:
        return
    
    # 이동 가능한 경우, 실제 위치와 체력 업데이트
    if try_movement(idx, move_dir):
        for i in range(1, n+ 1):
            r[i] = nr[i]
            c[i] = nc[i]
            k[i] -= dmg[i]
    return


l, n, q = map(int, input().split())

# 인포 배열 업데이트
for i in range(1,l + 1):
    info[i][1:] = map(int, input().split())

# 각 기사들 위치,체력 업데이트
for i in range(1, n + 1):
    r[i], c[i], h[i], w[i], k[i] = map(int, input().split())
    bef_k[i] =k[i]

# 명령 실행
for _ in range(q):
    idx, d = map( int, input().split())
    move_piece(idx, d)

# 결과 출력
ans = sum([bef_k[i] - k[i] for i in range(1, n + 1) if k[i] > 0])
print(ans)
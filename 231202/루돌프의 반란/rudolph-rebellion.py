# # 전역 변수 초기화
# n, m, p, c, d = None, None, None, None, None
# rudolf, points, pos, board, is_live, stun, di, dj = None, None, None, None, None, None, None, None

def initialize_game():
    # 게임 시작 시 필요한 변수를 초기화하는 함수
    global n, m, p, c, d, rudolf, points, pos, board, is_live, stun, di, dj
    n, m, p, c, d = map(int, input().split())  # 게임판 크기, 턴 수, 산타 수, 루돌프의 힘, 산타의 힘을 입력받음
    rudolf = tuple(map(int, input().split()))  # 루돌프의 초기 위치

    # 각 산타의 점수, 위치, 생존 여부 등을 저장하는 배열 초기화
    points = [0 for _ in range(p + 1)]
    pos = [(0, 0) for _ in range(p + 1)]
    board = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    is_live = [False for _ in range(p + 1)]
    stun = [0 for _ in range(p + 1)]

    # 이동 방향 벡터 (상, 우, 하, 좌)
    di = [-1, 0, 1, 0]
    dj = [0, 1, 0, -1]

    # 게임판에 루돌프와 산타의 위치 설정
    board[rudolf[0]][rudolf[1]] = -1
    for _ in range(p):
        id, i, j = tuple(map(int, input().split()))
        pos[id] = (i, j)
        board[pos[id][0]][pos[id][1]] = id
        is_live[id] = True

def is_inrange(i, j):
    # 주어진 좌표가 게임판 내에 있는지 확인하는 함수
    return 1 <= i <= n and 1 <= j <= n

def move_rudolf():
    # 루돌프의 움직임을 처리하는 함수
    global rudolf
    closestI, closestJ, closestIdx = 10000, 10000, 0

    # 루돌프와 가장 가까운 산타를 찾음
    for idx in range(1, p + 1):
        if not is_live[idx]:
            continue

        # 가장 가까운 산타까지의 거리와 좌표를 저장
        currentBest = ((closestI - rudolf[0]) ** 2 + (closestJ - rudolf[1]) ** 2, (-closestI, -closestJ))
        currentValue = ((pos[idx][0] - rudolf[0]) ** 2 + (pos[idx][1] - rudolf[1]) ** 2, (-pos[idx][0], -pos[idx][1]))

        if currentValue < currentBest:
            closestI, closestJ = pos[idx]
            closestIdx = idx

    # 루돌프를 가장 가까운 산타 방향으로 이동
    if closestIdx:
        prevRudolf = rudolf
        moveI, moveJ = 0, 0
        if closestI > rudolf[0]:
            moveI = 1
        elif closestI < rudolf[0]:
            moveI = -1
        if closestJ > rudolf[1]:
            moveJ = 1
        elif closestJ < rudolf[1]:
            moveJ = -1

        rudolf = (rudolf[0] + moveI, rudolf[1] + moveJ)
        board[prevRudolf[0]][prevRudolf[1]] = 0
        board[rudolf[0]][rudolf[1]] = -1

        # 루돌프 이동 후 발생한 충돌 처리
        handle_collision(closestI, closestJ, moveI, moveJ, closestIdx)

def handle_collision(i, j, moveI, moveJ, idx):
    # 루돌프가 산타와 충돌했을 때 처리하는 함수
    if rudolf[0] == i and rudolf[1] == j:
        # 충돌 후 산타가 밀려날 최종 위치 계산
        firstI = i + moveI * c
        firstJ = j + moveJ * c
        lastI, lastJ = firstI, firstJ

        # 충돌한 산타 기절 처리
        stun[idx] = t + 1

        # 밀려난 산타가 다른 산타에게 영향을 줄 경우 처리
        while is_inrange(lastI, lastJ) and board[lastI][lastJ] > 0:
            lastI += moveI
            lastJ += moveJ

        # 연쇄적 밀쳐내기 처리
        while not (lastI == firstI and lastJ == firstJ):
            beforeI = lastI - moveI
            beforeJ = lastJ - moveJ

            if not is_inrange(beforeI, beforeJ):
                break

            cur_idx = board[beforeI][beforeJ]
            if not is_inrange(lastI, lastJ):
                is_live[cur_idx] = False
            else:
                board[lastI][lastJ] = board[beforeI][beforeJ]
                pos[cur_idx] = (lastI, lastJ)

            lastI, lastJ = beforeI, beforeJ

        # 산타의 점수 및 위치 업데이트
        points[idx] += c
        pos[idx] = (firstI, firstJ)
        if is_inrange(firstI, firstJ):
            board[firstI][firstJ] = idx
        else:
            is_live[idx] = False

def move_santas():
    # 모든 산타들의 움직임을 처리하는 함수
    for i in range(1, p+1):
        if is_live[i] and stun[i] < t:
            move_santa(i)

def move_santa(i):
    # 개별 산타의 움직임을 처리하는 함수
    minDist = (pos[i][0] - rudolf[0])**2 + (pos[i][1] - rudolf[1])**2
    moveDir = -1

    for dir in range(4):
        ni = pos[i][0] + di[dir]
        nj = pos[i][1] + dj[dir]

        if not is_inrange(ni, nj) or board[ni][nj] > 0:
            continue

        dist = (ni - rudolf[0])**2 + (nj - rudolf[1])**2
        if dist < minDist:
            minDist = dist
            moveDir = dir

    if moveDir != -1:
        ni = pos[i][0] + di[moveDir]
        nj = pos[i][1] + dj[moveDir]
        handle_santa_collision(i, ni, nj, moveDir)

def handle_santa_collision(i, ni, nj, moveDir):
    # 산타가 루돌프와 충돌했을 때 처리하는 함수
    if ni == rudolf[0] and nj == rudolf[1]:
        stun[i] = t + 1
        moveI = -di[moveDir]
        moveJ = -dj[moveDir]
        firstI = ni + moveI * d
        firstJ = nj + moveJ * d
        lastI, lastJ = firstI, firstJ

        if d == 1:
            points[i] += d
        else:
            while is_inrange(lastI, lastJ) and board[lastI][lastJ] > 0:
                lastI += moveI
                lastJ += moveJ

            while lastI != firstI or lastJ != firstJ:
                beforeI = lastI - moveI
                beforeJ = lastJ - moveJ

                if not is_inrange(beforeI, beforeJ):
                    break

                cur_idx = board[beforeI][beforeJ]
                if not is_inrange(lastI, lastJ):
                    is_live[cur_idx] = False
                else:
                    board[lastI][lastJ] = board[beforeI][beforeJ]
                    pos[cur_idx] = (lastI, lastJ)

                lastI, lastJ = beforeI, beforeJ

            points[i] += d
            board[pos[i][0]][pos[i][1]] = 0
            pos[i] = (firstI, firstJ)
            if is_inrange(firstI, firstJ):
                board[firstI][firstJ] = i
            else:
                is_live[i] = False
    else:
        board[pos[i][0]][pos[i][1]] = 0
        pos[i] = (ni, nj)
        board[ni][nj] = i

def update_scores():
    # 매 턴마다 산타들의 점수를 업데이트하는 함수
    for i in range(1, p+1):
        if is_live[i]:
            points[i] += 1

def print_final_scores():
    # 게임이 끝난 후 최종 점수를 출력하는 함수
    for i in range(1, p + 1):
        print(points[i], end=" ")

# 게임 초기화 및 메인 루프
initialize_game()
for t in range(1, m + 1):
    move_rudolf()
    move_santas()
    update_scores()

# 결과 출력
print_final_scores()
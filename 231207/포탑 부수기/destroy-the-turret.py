# import sys
# sys.stdin = open("input.txt")
# from pprint import pprint

from collections import deque


def attack_check():
    ai, aj = 0, 0
    power = 5001

    for i in range(n):
        for j in range(m):
            if arr[i][j] == 0: continue
            if arr[i][j] < power:
                power = arr[i][j]
                ai, aj = i, j
            elif arr[i][j] == power:
                if attack_time[i][j] > attack_time[ai][aj]:
                    ai, aj = i, j
                elif attack_time[i][j] == attack_time[ai][aj]:
                    if i + j > ai + aj:
                        ai, aj = i, j
                    elif i + j == ai + aj:
                        if j > aj:
                            aj = j
    return ai, aj


def target_check(ai, aj):
    ti, tj = 0, 0
    power = -1
    for i in range(n):
        for j in range(m):
            if arr[i][j] == 0: continue
            if i == ai and j == aj: continue
            if arr[i][j] > power:
                power = arr[i][j]
                ti, tj = i, j
            elif arr[i][j] == power:
                if attack_time[i][j] < attack_time[ti][tj]:
                    ti, tj = i, j
                elif attack_time[i][j] == attack_time[ti][tj]:
                    if i + j < ti + tj:
                        ti, tj = i, j
                    elif i + j == ti + tj:
                        if j < tj:
                            ti, tj  = i, j
    return ti, tj


def laser(ai, aj, ti, tj):
    q = deque()
    q.append((ai, aj, []))
    visited = [[False] * m for _ in range(n)]
    visited[ai][aj] = True

    while q:
        i, j, route = q.popleft()
        for k in range(4):
            ni, nj = (i + di[k]) % n, (j + dj[k]) % m
            if visited[ni][nj]: continue
            if arr[ni][nj] == 0: continue

            # 타겟인 경우
            if (ni, nj) == (ti, tj):
                arr[ni][nj] -= point

                for ri, rj in route:
                    arr[ri][rj] -= half_point
                    attack[ri][rj] = True
                return True

            # 경로 체크
            tmp_route = route[:] # deepcopy
            tmp_route.append((ni, nj))
            visited[ni][nj] = True
            q.append((ni, nj, tmp_route))

    # 도달 X 라면
    return False


def boom(ai, aj, ti, tj):
    arr[ti][tj] -= point
    ddi, ddj = di + [1, 1, -1, -1], dj + [-1, 1, -1, 1]
    for k in range(8):
        ni, nj = (ti + ddi[k]) % n, (tj + ddj[k]) % m
        if ni == ai and nj == aj: continue
        arr[ni][nj] -= half_point
        attack[ni][nj] = True
    return


def break_check():
    for i in range(n):
        for j in range(m):
            if arr[i][j] < 0:
                arr[i][j] = 0
    return


def max_check():
    return max([max(line) for line in arr])


def turret_check():
    turret = []
    turret_cnt = 0
    for i in range(n):
        for j in range(m):
            if arr[i][j] == 0: continue
            turret_cnt += 1
            if attack[i][j]: continue
            turret.append((i, j))

    if turret_cnt == 1:
        print(max_check())
        # 코드 끝내기
        exit(0)
    for i, j in turret:
        arr[i][j] += 1

    return


di, dj = [0, 1, 0, -1], [1, 0, -1, 0]
n, m, k = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]
attack_time = [[0] * m for _ in range(n)]  # 공격 시점 배열

for time in range(1, k + 1):
    # 공격 배열
    attack = [[False] * m for _ in range(n)]

    # 공격자 선정
    ai, aj = attack_check()
    arr[ai][aj] += n + m
    point = arr[ai][aj]
    half_point = point // 2
    attack[ai][aj] = True
    attack_time[ai][aj] = time

    # 공격, 부서짐
    ti, tj = target_check(ai, aj)
    attack[ti][tj] = True

    if not laser(ai, aj, ti, tj):
        boom(ai, aj, ti, tj)

    # 포탑 부서짐
    break_check()

    # 정비
    turret_check()


print(max_check())
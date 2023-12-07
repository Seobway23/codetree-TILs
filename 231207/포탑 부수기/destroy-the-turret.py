# import sys
# sys.stdin = open("input.txt")
# from pprint import pprint

from collections import deque

n, m, k = map(int, input().split()) # n 행, m 열, k 턴
arr = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
turn_arr = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

for i in range(1, n + 1):
    arr[i][1:] = list(map(int, input().split()))


def select_tow():
    global atk_tow, tgk_tow
    # 포탑 리스트, 포탑 이라면 추가, key 값으로 sort 할 것
    tow_lst = []

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if arr[i][j] > 0:
                # 0 공격력, 1 최근 공격 포탑, 2 i + j, 3 i, 4 j

                tow_lst.append([arr[i][j], turn_arr[i][j], i + j, i, j])

    # 가장 약한 포탑 선정
    # 0 낮음, 1 높음, 2 높음, 4 높음
    # x[0] , -x[1], -x[2], -x[4]
    tow_lst.sort(key=lambda x: (x[0], -x[1], -x[2], -x[4]))
    atk_tow = tow_lst[0]

    # 가장 강한 포탑 선정
    # 0 높음, 1 낮음, 2 낮음, 4 낮음
    tow_lst.sort(key=lambda x: (-x[0], x[1], x[2], x[4]))
    tgk_tow = tow_lst[0]
    return


def laser():
    global atk_tow, tgk_tow
    atk, atk_turn, atk_ij, ai, aj = atk_tow
    tgk, tgk_turn, tgk_ij, ti, tj = tgk_tow

    q = deque()
    q.append([ai, aj, []])
    visited = [[False] * (m + 1) for _ in range(n + 1)]
    visited[ai][aj] = True

    while q:
        ci, cj, route = q.popleft()

        # 우 하 좌 상
        dir = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        # 좌 상 하 우
        for k in range(len(dir)):
            # 범위내 ㅇㅇ 맞음
            ni, nj = (ci + dir[k][0]) % n, (cj + dir[k][1]) % n
            ni = n if ni == 0 else ni
            nj = m if nj == 0 else nj

            if visited[ni][nj]: continue
            if arr[ni][nj] == 0: continue

            if (ni, nj) == (ti, tj):
                route.append([ni, nj])
                return route

            tmp_route = route[:]
            tmp_route.append([ni, nj])
            visited[ni][nj] = True
            q.append([ni, nj, tmp_route])
    return False


def tower_atk():
    global atk_tow, tgk_tow

    atk, atk_turn, atk_ij, ai, aj = atk_tow
    tgk, tgk_turn, tgk_ij, ti, tj = tgk_tow

    # 공격 tow turn 에 갱신
    turn_arr[ai][aj] = turn
    arr[ai][aj] += n + m
    atk += n + m

    # repair 에 적용할 공격 받은 리스트
    atk_lst = [[ai, aj], [ti, tj]]

    # 공격 턴
    laser_lst = laser()

    if laser_lst != False:
        # print("레이저다")
        # print("공격자:", (ai, aj), ", 공격 받는자:", (ti, tj))
        # print(laser_lst)
        for ci, cj in laser_lst:
            # 타겟 이라면
            if (ci, cj) == (ti, tj):
                cur_atk = arr[ti][tj] - atk
                arr[ci][cj] = cur_atk if cur_atk > 0 else 0

            # 그냥 포탑 이라면
            else:
                cur_atk = arr[ci][cj] - (atk // 2)
                arr[ci][cj] = cur_atk if cur_atk > 0 else 0
                atk_lst.append([ci, cj])

    else:
        # print("포탑 공격")
        # print("공격자:", (ai, aj), ", 공격 받는자:", (ti, tj))
        # print()

        for di in range(-1, 2):
            for dj in range(-1, 2):
                ni, nj = (ti + di) % n, (tj + dj) % m
                ni = n if ni == 0 else ni
                nj = m if nj == 0 else nj
                # print(ni, nj)

                # 타겟 이라면
                if (ni, nj) == (ti, tj):
                    cur_atk = arr[ti][tj] - atk
                    arr[ni][nj] = cur_atk if cur_atk > 0 else 0

                # 타겟이 아니라면
                else:
                    cur_atk = arr[ni][nj] - (atk // 2)
                    arr[ni][nj] = cur_atk if cur_atk > 0 else 0
                    atk_lst.append([ni, nj])


    # Repair
    # print(atk_lst)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if arr[i][j] > 0:
                if [i, j] in atk_lst:
                    pass
                else:
                    arr[i][j] += 1

    return


def print_strong():
    ans_lst = []
    for i in range(n + 1):
        for j in range(m + 1):
            if arr[i][j] > 0:
                ans_lst.append([arr[i][j], turn_arr, i + j, i, j])
    # 0 높음, 1 낮음, 2 낮음, 4 낮음
    ans_lst.sort(key=lambda x: (-x[0], x[1], x[2], x[4]))
    print(ans_lst[0][0])
    return


for turn in range(1, k + 1):
    laser_lst = []
    atk_tow, tgk_tow = [], []
    select_tow()
    tower_atk()

print_strong()


'''
turn x[1] 값 갱신 해야 함
'''
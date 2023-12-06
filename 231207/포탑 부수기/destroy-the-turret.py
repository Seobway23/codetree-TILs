# import sys
from collections import deque
# from pprint import pprint
# sys.stdin = open("input.txt")

'''
4≤N,M≤10
1≤K≤1,000
0≤공격력≤5,000
'''


def target():
    global key_lst, turn_arr
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # 포탑 이라면
            if arr[i][j] > 0:
                # key => 공격력, 최근 공격, 행과 열 합, 행, 열
                push_lst = [0, 2, 0, 0, 0]

                # 공격력
                push_lst[0] = arr[i][j]

                # 최근 공격
                push_lst[1] = turn_arr[i][j]

                # 행 + 렬
                push_lst[2] = i + j

                # 행 열
                push_lst[3] = i
                push_lst[4] = j
                key_lst.append(push_lst)

    key_lst.sort(key=lambda x: (x[0], -x[1], -x[2], -x[4]))
    # print(turn, "번째, 턴")
    return


def attack():
    global key_lst, last_atk

    # print( turn, "어택전 arr")
    # pprint(arr)
    # print()

    # key => 0공격력, 1최근 공격, 2행과 열 합, 3행, 4열
    # 공격 하는 타워
    atk_tow = key_lst[0]
    turn_arr[atk_tow[3]][atk_tow[4]] = turn + 1
    # 공격 당하는 타워
    key_lst.sort(key=lambda x: (-x[0], x[1], x[2], x[4]))
    target_tow = key_lst[0]
    # print("공격받는자 리스트")
    # pprint( key_lst)
    # print("공격 타워:", atk_tow, ", 공격 받는 타워:", target_tow)

    # 공격력 m + n 만큼 증가
    atk_tow[0] += n + m
    arr[atk_tow[3]][atk_tow[4]] += n + m
    # print("공격력:", atk_tow[0], arr[atk_tow[3]][atk_tow[4]])

    # print("공격자:", atk_tow[3],atk_tow[4])
    # print("공격 받는 위치:", target_tow[3], target_tow[4])

    laser_lst = laser(atk_tow, target_tow)
    if laser_lst:
        # print("레이저다")
        # print(laser_lst)
        # 주변 타워 -atk//2

        for ci, cj in laser_lst:
            # print(ci, cj)
            arr[ci][cj] -= atk_tow[0] // 2
            # print(atk_tow[0] // 2, arr[ci][cj])

            # last_atk 추가
            last_atk.append([ci, cj])

            if arr[ci][cj] < 0:
                arr[ci][cj] = 0

        # 타겟 타워 - atk
        arr[target_tow[3]][target_tow[4]] -= atk_tow[0]
        if arr[target_tow[3]][target_tow[4]] < 0:
            arr[target_tow[3]][target_tow[4]] = 0

    # 포탄 공격
    else:
        # print("포탑이다!")
        # target_tow 는 atk_tow[0] 만큼 공격 받음
        # 주변 8방향은 atk_tow // 2
        for i in range(-1, 2):
            for j in range(-1, 2):
                ni, nj = (target_tow[3] + i), (target_tow[4] + j)
                ni = ni -m if ni> m else ni
                nj = nj - n if nj > n else nj
                # print((i, j), "m:", m,  "ni: ", ni, " ,nj: ", nj)

                if arr[ni][nj] != 0:
                    # target 일 때,
                    if (ni,nj) == (target_tow[3], target_tow[4]):
                        arr[ni][nj] -= atk_tow[0]

                    # 아닐 때,
                    else:
                        # print()
                        arr[ni][nj] -= atk_tow[0] // 2

                    # last_atk 추가
                    last_atk.append([ni, nj])

                    # 0보다 작으면 0으로 갱신
                    if arr[ni][nj] < 0:
                        arr[ni][nj] = 0

    # repair 전 last_atk 에 atk_tow, target_tow 추가
    if [atk_tow[3], atk_tow[4]] not in last_atk:
        last_atk.append([atk_tow[3], atk_tow[4]])
    if [target_tow[3], target_tow[4]] not in last_atk:
        last_atk.append([target_tow[3], target_tow[4]])

    # repair
    for i in range(1, n + 1):
        for j in range(1, m +1):
            if arr[i][j] !=0 and [i, j] not in last_atk:
                # 공격 가담 X -> 공격력 + 1
                arr[i][j] += 1
    # last_atk 갱신
    last_atk = []
    return


def max_atk():
    global turn_arr

    ans_lst = []
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if arr[i][j] > 0:
                ans_lst.append([arr[i][j],turn_arr[i][j], i+j, i, j])

    ans_lst.sort(key=lambda x: (-x[0], -x[1], -x[2], -x[4]))
    return ans_lst[0][0]


def laser(atk_tow, target_tow):
    # 우,하,좌,상
    laser_lst = []
    q = deque()
    q.append([atk_tow[3], atk_tow[4]])

    while q:
        ti, tj = q.pop()
        flag = 0
        for di, dj in ((0, 1), (1, 0), (0,-1), (-1,0)):

            if flag == 1:
                break

            ni, nj = (ti + di) % n, (tj + dj) % m
            # print(ni, nj)
            # print(laser_lst)
            if arr[ni][nj] > 0:
                if [ni, nj] not in laser_lst:
                    if [ni, nj] == [target_tow[3], target_tow[4]]:
                        laser_lst.append([ni, nj])
                        return laser_lst

                    q.append([ni, nj])
                    laser_lst.append([ni, nj])
                    flag = 1
    return laser_lst
####


# n 행, m 열, k 턴
n, m, k = map(int, input().split())
arr = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
turn_arr = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
last_atk = []


for i in range(1,n+1):
    arr[i][1:] = list(map(int, input().split()))
# pprint(arr)

for turn in range(k):
    # key => 공격력, 최근 공격, 행과 열 합, 행, 열
    key_lst = []
    target()
    attack()

print(max_atk())
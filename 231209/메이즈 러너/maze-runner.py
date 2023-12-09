from copy import deepcopy


# 상 하 좌 우
di, dj = [-1, 1, 0, 0], [0, 0, -1, 1]


def move_people():
    global exits, move
    # 종료 조건은 move 에서

    # 먼저 무브 판단
    ei, ej = exits
    for i in range(1, m + 1):
        if pi[i] == -1:
            continue

        ci, cj = pi[i], pj[i]

        # 상하 먼저 탐색
        mi, mj = 0, 0
        if ci < ei:
            mi += 1
        elif ci > ei:
            mi -= 1

        else:
            if cj > ej:
                mj -= 1

            elif cj < ej:
                mj += 1

        # 움직임 시작
        # print("exit:",(ei, ej), "cur:", (ci, cj), "move:",  (mi, mj))
        ni, nj = ci + mi, cj + mj
        if arr[ni][nj] == 0 or arr[ni][nj] == -1:
            people_num = arr[ci][cj]

            if ni == ei and nj == ej:
                # print("도착")
                ni, nj, people_num = -1, -1, -1

            # 갱신 위치
            arr[ni][nj] = people_num
            pi[i], pj[i] = ni, nj
            move += 1

            # 현재 위치 0으로 만들기
            arr[ci][cj] = 0
    # print("무브진행")
    # pprint(arr)
    # print("move:", move)
    # print()
    return


def select_rec():
    global exits
    ei, ej = exits
    # 정사각형 만들어야 함
    # size 는 격자 갯수
    # print("n:", n)
    for size in range(2, n + 1):
        # print("size:", size)
        for i in range(n - size + 1):
            for j in range(n - size + 1):
                cnt = 0

                # 사람 있으면 cnt +=  1
                for k in range(1, m + 1):
                    if i <= pi[k] < i + size and j <= pj[k] < j + size:
                        # print("사람 있음")
                        cnt += 1
                        break

                # exit 있으면 cnt +=  1
                if i <= ei < i + size and j <= ej < j + size:
                    # print("exit 있음")
                    cnt += 1

                if cnt == 2:
                    # print("사각형 찾음")
                    # print("size: ", size, " ,i:", i, " ,j:", j)
                    return i, j, size
    # 설마
    return -1, -1, -1


def rotate_miro(si, sj, size):
    global arr, pr, pc, exits
    # print("si:", si, "sj:", sj, "size:", size)
    copy_arr = deepcopy(arr)
    for ci in range(size):
        for cj in range(size):
            # 시계 방향 회전
            ri, rj = si + cj, size -1 + sj - ci
            # print((ci, cj), "->", (ri, rj))
            copy_arr[ri][rj] = arr[ci + si][cj + sj]

    # print("turn:", turn)
    # print("움직이기 전")
    # pprint(arr)
    # print()

    for i in range(si + size):
        for j in range(sj + size):
            # 벽이면 -1
            if 10 > copy_arr[i][j] > 0:
                copy_arr[i][j] -= 1

            # 사람이면, 위치 옮기기
            if copy_arr[i][j] > 10:
                p_idx = copy_arr[i][j] - 10
                pi[p_idx], pj[p_idx] = i, j

            if copy_arr[i][j] == -1:
                exits = i, j

    # print("움직인 후")
    # pprint(copy_arr)
    # print()
    return copy_arr


# n: 미로 크기, m: 참가자 수, k: 게임 시간
n, m, k = map(int, input().split())
# exit, pi, pj, move 미로 배열 필요
arr = [list(map(int, input().split())) for _ in range(n)]

move = 0
pi = [0 for _ in range(m + 1)]
pj = [0 for _ in range(m + 1)]

for i in range(1, m + 1):
    peopleI, peopleJ = map(int, input().split())
    pi[i], pj[i] = peopleI - 1, peopleJ - 1
    arr[peopleI-1][peopleJ-1] = i + 10

# exits
exits = list(map(int, input().split()))
exits[0] -= 1
exits[1] -= 1
arr[exits[0]][exits[1]] = -1

for turn in range(k):
    move_people()
    si, sj, size = select_rec()
    arr = rotate_miro(si, sj, size)
    # pprint(arr)
    # 전부 빠져나왔다면
    if sum(pi) == (-1)*m:
        break

print(move)
exits = exits[0] + 1, exits[1] + 1
print(*exits)
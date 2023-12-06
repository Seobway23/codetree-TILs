def move_people():
    global m, exit, pr, pc, move_cnt
    # 사람 마다 전부 이동
    for i in range(1, m + 1):
        if pr[i] == -1:
            continue

        # print("i:", i, ", 사람 위치:", (pr[i], pc[i]), ", exit:", exit)
        # 상, 하 먼저 판단
        if pr[i] != exit[0]:
            nr, nc = pr[i], pc[i]
            if exit[0] < pr[i]:
                nr -= 1
            else:
                nr += 1

            # print("i:", i, ", 사람 위치:", (pr[i], pc[i]), "움직인 위치:", (nr, nc),", exit:", exit)

            if is_in_range(nr, nc) and arr[nr][nc] < 1:
                people_value = arr[pr[i]][pc[i]]

                # 처음 위치 초기화
                arr[pr[i]][pc[i]] = 0
                move_cnt += 1
                # 움직인 위치 갱신
                if arr[nr][nc] == -1:  # 도착지라면
                    pr[i], pc[i] = -1, -1

                else:  # 움직일 수 있는 길이라면
                    arr[nr][nc] = people_value
                    pr[i], pc[i] = nr, nc

                continue

        # 좌 우 판단
        if pc[i] != exit[1]:
            nr, nc = pr[i], pc[i]
            # 좌, 우 판단
            if exit[1] < pc[i]:
                nc -= 1
            elif exit[1] > pc[i]:
                nc += 1

            if is_in_range(nr, nc) and arr[nr][nc] < 1:
                people_value = arr[pr[i]][pc[i]]

                # 처음 위치 초기화
                arr[pr[i]][pc[i]] = 0
                move_cnt += 1
                # 움직인 위치 갱신
                if arr[nr][nc] == -1:  # 도착지라면
                    pr[i], pc[i] = -1, -1

                else:  # 움직일 수 있는 길이라면
                    arr[nr][nc] = people_value
                    pr[i], pc[i] = nr, nc
                    continue

    return


def find_square():
    ir, ic, length = 0, 0, 0
    for length in range(1, n):  # r2 - r1
        # print("사각형 길이:", length)
        # 정사각형 좌상단 (r1, c1)
        for r1 in range(1, n + 1 - length):
            for c1 in range(1, n + 1 - length):
                # 정사각형 우하단 (r2,c2)
                r2, c2 = r1 + length, c1 + length

                exit_flag, people_flag = False, False

                for i in range(r1, r2 + 1):
                    for j in range(c1, c2 + 1):

                        if arr[i][j] > 10:
                            people_flag = True
                        elif arr[i][j] == -1:
                            exit_flag = True

                        if people_flag and exit_flag:
                            # print(length + 1, "길이", (r1, c1), (r2, c2))
                            return r1, c1, length + 1
    return


def rotate_square():
    global ir, ic, length, exit
    arr_copy = [[0 for _ in range(n)] for _ in range(n)]

    # 90도 시계방향 회전  # 현재 방향에서 하면 안되고 -ir, -ic 한 다음에 그다음에 ir, ic 더하기
    for i in range(ir, ir + length):  # length 는 +1 더해서 오기 때문에 그냥 length 쓴다
        for j in range(ic, ic + length):
            oi, oj = i - ir, j - ic
            new_i, new_j = oj, length - oi - 1
            arr_copy[new_i + ir][new_j + ic] = arr[i][j]  # j, n - i

    # 갱신
    for i in range(ir, ir + length):  # length 는 +1 더해서 오기 때문에 그냥 length 쓴다
        for j in range(ic, ic + length):
            arr[i][j] = arr_copy[i][j]
            # 벽 -1
            if 0 < arr[i][j] < 10:
                arr[i][j] -= 1

            # 사람 위치 갱신
            elif arr[i][j] > 10:
                idx = arr[i][j] - 10
                pr[idx], pc[idx] = i, j

            if arr[i][j] == -1:
                # print("오애 안되는데")
                exit = [i, j]
                # print("exit:", exit)

    # print("갱신후")
    # for i in range(n + 1):
    #     print(arr[i])

    return


# 세부 function
####
def is_in_range(i, j):
    global n
    return 1 <= i <= n and 1 <= j <= n


####

# input 받기
n, m, k = map(int, input().split())
arr = [[0 for _ in range(n + 1)] for _ in range(n + 1)]  # 1,1 시작
for i in range(1, n + 1):
    arr[i][1:] = list(map(int, input().split()))

# 자료 구조
pr = [0] * (m + 1)
pc = [0] * (m + 1)
move_cnt = 0
exit = [0, 0]

# 사람 input 받기
for i in range(1, m + 1):
    r, c = map(int, input().split())
    # 사람 리스트에 표시
    pr[i], pc[i] = r, c

    # 배열에 표시, i + 10
    arr[r][c] = i + 10

# exit input 받기
exit = list(map(int, input().split()))
arr[exit[0]][exit[1]] = -1

# 메인 로직
for h in range(k):
    # 모두 탈출했다면, 즉시 종료
    if sum(pr) == -1 * (m):
        break

    # 사람 이동
    move_people()
    # print("move")
    # for i in range(n + 1):
    #     print(arr[i])

    ir, ic, length = find_square()  # length 는 변 길이 (0, 0, 0 일 경우 3)
    # print("ir:", ir, "ic:", ic, "length:", length)
    rotate_square()

# 답 출력
print(move_cnt)
print(*exit)
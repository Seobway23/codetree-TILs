from copy import deepcopy

def plus_sushi():
    global lst, sushi, people

    time, loc, name = int(lst[1]), int(lst[2]), lst[3]
    
    if name in sushi:
        sushi[name].append([time, loc])
    
    else:
        sushi[name] = [[time, loc]]
    
    update(time)
    return

def plus_people():
    global lst, sushi, people

    time, loc, name, eat = int(lst[1]), int(lst[2]), lst[3], int(lst[4])
    people[name] = [eat, loc]
    update(time)
    return

def print_ans():
    global lst, L, sushi, people
    time = int(lst[1])
    update(time)

    # 각 갯수 cnt
    people_cnt = len(people)
    sushi_cnt = 0
    for ss in sushi:
        sushi_cnt += len(sushi[ss])
    
    print(people_cnt, sushi_cnt)
    return

def update(time):
    global L, sushi, people
    temp = deepcopy(sushi)

    for index in sushi: # sushi [0]: time, [1]: location
        for i in range(len(sushi[index])-1, -1, -1):
            flag = 0
            dif = time - sushi[index][i][0]

            start, end = sushi[index][i][1], sushi[index][i][1] + dif

            if index in people: # 만약 사람이 있으면 먹었는지 확인
            
                if dif >= L:
                    del temp[index][i] # 스시 삭제
                    if len(temp[index]) == 0: # 만약 전부 다 먹으면 
                        del temp[index] # 이름-스시 전부 삭제
                    people[index][0] -= 1 # 사람 eat -1
                    if people[index][0] == 0: #만약 사람이 전부 먹었다면
                        del people[index] # 사람 삭제
                    flag = 1

                else: # dif < L 이라면
                    if end < start:
                        if start <= people[index][1] + L <= end + L :
                            del temp[index][i] # 스시 삭제
                            if len(temp[index]) == 0: # 만약 전부 다 먹으면 
                                del temp[index] # 이름-스시 전부 삭제
                            people[index][0] -= 1 # 사람 eat -1
                            if people[index][0] == 0: #만약 사람이 전부 먹었다면
                                del people[index] # 사람 삭제
                            flag = 1
                    else:
                        # 정방향 범위내
                        if start <= people[index][1] <= end:
                            del temp[index][i] # 스시 삭제
                            if len(temp[index]) == 0: # 만약 전부 다 먹으면 
                                del temp[index] # 이름-스시 전부 삭제
                            people[index][0] -= 1 # 사람 eat -1
                            if people[index][0] == 0: #만약 사람이 전부 먹었다면
                                del people[index] # 사람 삭제
                            flag = 1
                    
            if flag == 0:
                # print("갱신해야돼:", time, index, temp[index][i])
                # print("갱신 대상:", temp)
                temp[index][i][0] = time # time 갱신
                temp[index][i][1] = ((temp[index][i][1] + dif) % L)

    sushi = temp
    return

# 자료구조 선언
sushi = dict() # [0]: time, [1]: location
people = dict() # [0]: eat, [1]: location


# 입력 선언
L, Q = map(int, input().split())
for _ in range(Q):
    lst = list(input().split())
    
    if lst[0] == "100":
        plus_sushi()

    elif lst[0] == "200":
        plus_people()
    
    elif lst[0] == "300":
        # print("sushi:", sushi)
        # print("people:", people)
        print_ans()
L, Q = map(int, input().split())
# 필요 자료 구조
sushi_lst = [] # 초밥 리스트
people_dict = dict() # 사람 cnt
people_index = dict() # 사람 자리

def circle(time):
    global L, sushi_lst

    # table 순회
    for i in range(len(sushi_lst)):

        flag = 0
        # 타임에 따라서 다르게 하기
        t, loc, name = sushi_lst[i]
        t, loc, time = int(t), int(loc), int(time)
        dif = time - t
        
        # 범위 내 있는지 확인
        people_list = people_dict.keys()

        if name in people_list:
            s, e = loc, ((loc + dif) % L)

            # 있는 지 확인
            if e < s:
                if s < people_index[name]  + L < e + L:
                    people_dict[name] -= 1
                    sushi_lst[i][2] = 1
                    
                    
                    
            else: 
                if s <= people_index[name] <= e:
                    people_dict[name] -= 1
                    sushi_lst[i][2] = 1

            # cnt가 0인지 확인
            if people_dict[name] == 0:
                del people_dict[name]
                del people_index[name]
                flag= 1
        # 갱신
        if flag == 0:
            sushi_lst[i][0] = time
            sushi_lst[i][1] = ((loc + dif) % L)


    # 초밥리스트 갱신
    temp_lst = []
    for j in range(len(sushi_lst)):
        # print(j, ":",sushi_lst[j][2])
        if sushi_lst[j][2] == 1:
            pass
        else:
            temp_lst.append(sushi_lst[j])

    sushi_lst = temp_lst
    # print("갱신된 suhsi:", sushi_lst)
    # print("현재 people:",people_dict)
    return



def plus_sushi(lst):
    time, loc, name = lst[1:]
    time, loc = int(time), int(loc)
    sushi_lst.append([time, loc, name])
    circle(time)
    return

def plus_people(lst):
    time, loc, name, cnt = lst[1:]
    time, loc, cnt = int(time), int(loc), int(cnt)
    people_dict[name] = cnt
    people_index[name] = loc
    circle(time)
    return

def print_sushi(lst):
    time = lst[1]
    circle(time)
    return



for i in range(Q):
    lst = list(input().split())
    if lst[0] == "100" :
        plus_sushi(lst)


    if lst[0] == "200":
        plus_people(lst)

    if lst[0] == "300":
        print_sushi(lst)
        print(len(people_dict), len(sushi_lst))
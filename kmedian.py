from optimal_solution import dis
import random

def kmedian(data_list, k, max_iter = 100):
    num = len(data_list)
    random_begin = [random.randint(0, num-1) for x in range(k)]
    cur_acc = cal_dis(data_list, random_begin)
    cur_state = random_begin
    flag = True
    cnt = 0
    while flag and cnt < max_iter:
        cnt += 1
        flag = False
        for i in range(num):
            for x in range(k):
                temp = cur_state
                temp[x] = i
                local_move_acc = cal_dis(data_list, temp)
                if local_move_acc >  cur_acc:
                    local_move_acc = cur_acc
                    cur_state = temp
                    flag = True
                if flag:
                    break
            if flag:
                break
    print "For %d center objective, 5-approx value is %d" % (k , local_move_acc)
    return local_move_acc

def cal_dis(client_list, center_list):
    assignment = dict()
    ans = 0
    for client in client_list:
        min = 10000000000000000
        for c in center_list:
            center = client_list[c]
            if (dis(client, center) < min):
                min = dis(center, client)
        ans = ans + min
    return ans
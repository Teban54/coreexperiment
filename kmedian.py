from optimal_solution import dis
import random
from utils import *

def kmedian(data_list, k, alpha=1, max_iter=100, groups_list=None, distances=None):
    if not distances:
        distances = calc_distances(data_list)
    num = len(data_list)
    random_begin = [random.randint(0, num-1) for x in range(k)]
    cur_acc = cal_dis(data_list, random_begin, distances)
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
                local_move_acc = cal_dis(data_list, temp, distances)
                if local_move_acc >  cur_acc:
                    local_move_acc = cur_acc
                    cur_state = temp
                    flag = True
                if flag:
                    break
            if flag:
                break
    print("For %d median objective, 5-approx value is %d" % (k , local_move_acc))
    if groups_list:
        return local_move_acc, calc_beta_groups(data_list, groups_list, cur_state, alpha)
    return local_move_acc, calc_beta(data_list, cur_state, k, alpha)

def cal_dis(client_list, center_list, distances):
    assignment = dict()
    ans = 0
    for client in client_list:
        min = 10000000000000000
        for c in center_list:
            center = client_list[c]
            if (distances[client][center] < min):
                min = distances[center][client]
        ans = ans + min
    return ans
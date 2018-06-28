from optimal_solution import dis
from kmedian import cal_dis
import random
from utils import *

def local_search_capture(data_list, k, alpha = 1, beta = 1, max_iter = 100):
    num = len(data_list)
    random_begin = [random.randint(0, num-1) for x in range(k)]
    flag = True
    temp = random_begin
    iter_cnt = 0
    while flag and iter_cnt < max_iter:
        iter_cnt += 1
        flag = False
        assignment = dict()
        for client in data_list:
            min = 10000000000000000
            for center in temp:
                if (dis(data_list[center], client) < min):
                    min = dis(data_list[center], client)
                    mincenter = center
            assignment[client] = mincenter
        client_num = dict()
        for center in temp:
            client_num[center] = 0
        for client in data_list:
            client_num[assignment[client]] += 1
        next_close_center = 0
        next_close_center_client = 100000
        next_close_center_index = 0

        for i in range(len(temp)):
            center = temp[i]
            if (client_num[center] < next_close_center_client):
                next_close_center_client = client_num[center]
                next_close_center = center
                next_close_center_index = i
        for i in range(len(data_list)):
            potential_center = data_list[i]
            cnt = 0
            for client in data_list:
                if beta * dis(client, data_list[assignment[client]]) > dis(client, potential_center):
                    cnt += 1
            if (cnt >= alpha * num / k):
                temp[next_close_center_index] = i
                flag = True
                break
    if iter_cnt == max_iter:
        print('Did not converge %d %d' % (alpha, beta))
    kcenterobj = calc_kcenter_objective(data_list, temp, k)
    kmedianobj = cal_dis(data_list, temp)
    print("For %d median objective, local search value is %d" % (k, kmedianobj))
    return kcenterobj, kmedianobj, calc_beta(data_list, temp, alpha)

def calc_kcenter_objective(data_list, cur_sol, k):
    assignment = dict()
    ans = 0
    for client in data_list:
        min = 10000000000000000
        for center in cur_sol:
            if (dis(data_list[center], client) < min):
                min = dis(data_list[center], client)
                mincenter = center
        if min > ans:
            ans = min
    print("For %d center objective, local search value is %d" % (k , ans))
    return ans




from optimal_solution import dis
import random
from utils import *

def kmedian_procedure(data_list, k, alpha=1, max_iter=100, groups_list=None, distances=None,
                      client_list=None, remaining_k=-1):
    """
    Performs the k-median approximation algorithm.
    :param data_list:
    :param k:
    :param alpha:
    :param max_iter:
    :param groups_list:
    :param distances:
    :param client_list: list of indexes of available facilities to choose
        default: 0, 1, ..., len(data_list)-1
    :param remaining_k: number of remaining centers to be opened
        default: k
    :return:
    """
    if not distances:
        distances = calc_distances(data_list)
    if not client_list:
        client_list = range(len(data_list))
    if remaining_k == -1:
        remaining_k = k
    num = len(data_list)
    random_begin = [client_list[random.randint(0, len(client_list)-1)] for x in range(remaining_k)]
    cur_acc = cal_dis(data_list, random_begin, distances)
    cur_state = random_begin
    flag = True
    cnt = 0
    while flag and cnt < max_iter:
        cnt += 1
        flag = False
        for i in client_list:
            for x in range(remaining_k):
                temp = cur_state
                temp[x] = i
                local_move_acc = cal_dis(data_list, temp, distances)
                if cur_acc > local_move_acc:
                    cur_acc = local_move_acc
                    cur_state = temp
                    flag = True
                if flag:
                    break
            if flag:
                break
    return cur_state, cur_acc


def kmedian(data_list, k, alpha=1, max_iter=100, groups_list=None, distances=None, print_log=True):
    if not distances:
        distances = calc_distances(data_list)
    facility_indexes, objective = kmedian_procedure(data_list, k, alpha, max_iter, groups_list, distances, range(len(data_list)), k)
    if print_log:
        print("For %d median objective, 5-approx value is %d" % (k , objective))
    if groups_list:
        return objective, calc_beta_groups(data_list, groups_list, facility_indexes, k, alpha)
    return objective, calc_beta(data_list, facility_indexes, k, alpha), facility_indexes


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
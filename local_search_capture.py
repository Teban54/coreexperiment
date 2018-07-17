from optimal_solution import dis
from kmedian import cal_dis
import random
from utils import *

def local_search_capture(data_list, k, alpha=1, beta=1, max_iter=100, distances=None):
    if not distances:
        distances = calc_distances(data_list)
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
                if (distances[data_list[center]][client] < min):
                    min = distances[data_list[center]][client]
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
                if beta * distances[client][data_list[assignment[client]]] > distances[client][potential_center]:
                    cnt += 1
            if (cnt >= alpha * num / k):
                temp[next_close_center_index] = i
                flag = True
                break
    if iter_cnt == max_iter:
        print('Did not converge %d %d' % (alpha, beta))
    kcenterobj = calc_kcenter_objective(data_list, temp, k, distances)
    kmedianobj = cal_dis(data_list, temp, distances)
    print("For %d median objective, local search value is %d" % (k, kmedianobj))
    return kcenterobj, kmedianobj, calc_beta(data_list, temp, k, alpha)

def calc_kcenter_objective(data_list, cur_sol, k, distances):
    assignment = dict()
    ans = 0
    for client in data_list:
        min = 10000000000000000
        for center in cur_sol:
            if (distances[data_list[center]][client] < min):
                min = distances[data_list[center]][client]
                mincenter = center
        if min > ans:
            ans = min
    print("For %d center objective, local search value is %d" % (k , ans))
    return ans


def local_search_capture_groups(data_list, groups_list, k, alpha=1, beta=1, max_iter=100, distances=None):
    """
    Currently, the next center to be closed is determined by the smallest totay number of captured clients that are
    in at least one protected group.

    :param groups_list: A list of sublists that store clients in protected groups, one for each group.
        e.g. [[man1, man2], [woman1, woman2, woman3]]
    """
    if not distances:
        distances = calc_distances(data_list)
    num = len(data_list)
    random_begin = [random.randint(0, num-1) for x in range(k)]

    protected_set = set()
    for group in groups_list:
        for client in group:
            protected_set.add(client)

    flag = True
    temp = random_begin
    iter_cnt = 0
    while flag and iter_cnt < max_iter:
        iter_cnt += 1
        flag = False
        assignment = dict()
        for client in protected_set:  # Disregards clients not in any protected group
            min = 10000000000000000
            for center in temp:
                if (distances[data_list[center]][client] < min):
                    min = distances[data_list[center]][client]
                    mincenter = center
            assignment[client] = mincenter
        client_num = dict()
        for center in temp:
            client_num[center] = 0
        for client in protected_set:  # Disregards clients not in any protected group
            client_num[assignment[client]] += 1

        # Determine next center to be closed
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
            replaced = False
            for group in groups_list:  # Count number of deviating clients in each group separately
                cnt = 0
                for client in group:
                    if beta * distances[client][data_list[assignment[client]]] > distances[client][potential_center]:
                        cnt += 1
                if (cnt >= alpha * num / k):
                    temp[next_close_center_index] = i
                    flag = True
                    replaced = True
                    break
            if replaced:
                break
    if iter_cnt == max_iter:  # TODO: Replace with return values
        print('Did not converge %d %d' % (alpha, beta))
    kcenterobj = calc_kcenter_objective(data_list, temp, k, distances)
    kmedianobj = cal_dis(data_list, temp, distances)
    print("For %d median objective, local search value is %d" % (k, kmedianobj))
    return kcenterobj, kmedianobj, calc_beta_groups(data_list, groups_list, temp, alpha)

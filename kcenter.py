from optimal_solution import dis
import random
from utils import *

def kcenter(data_list, k, alpha = 1, groups_list = None):
    num = len(data_list)
    assignment = dict()
    cur_sol = set([random.randint(0, num-1)])
    for cnt in range(k):
        furthest_center = 0
        furthest_center_distance = 0
        for c in range(len(data_list)):
            client = data_list[c]
            dis_cur_sol = 100000000000
            for c_alt in cur_sol:
                center = data_list[c_alt]
                if (dis(client, center) < dis_cur_sol):
                    dis_cur_sol = dis(client, center)
            if (dis_cur_sol > furthest_center_distance):
                furthest_center_distance = dis_cur_sol
                furthest_center = c
        cur_sol.add(furthest_center)


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
    print("For %d center objective, 2-approx value is %d" % (k , ans))
    if groups_list:
        return ans, calc_beta_groups(data_list, groups_list, list(cur_sol), alpha)
    return ans, calc_beta(data_list, list(cur_sol), k, alpha)


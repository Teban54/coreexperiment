from itertools import combinations
from data_parser import parse_data, random_sample
import math
import numpy as np

def optimal_solution(data_list, k):
    comb = combinations([x for x in range(len(data_list)-1)], k)
    opt = 0.0
    for sol in list(comb):
        acc = calculate_accuracy(data_list, sol, k)
        if acc > opt:
            opt = acc
    return opt

def dis(pt1, pt2):
    sum = 0
    for i in range(pt1.dim):
        a = int(pt1.data[i])
        b = int(pt2.data[i])
        sum = sum + (a - b) * (a - b)
    return math.sqrt(sum)

def calculate_accuracy(data_list, sol, k):
    assignment = dict()
    for client in data_list:
        min = 10000000000000000
        for center in sol:
            if (dis(data_list[center], client) < min):
                min = dis(data_list[center], client)
                mincenter = center
        assignment[client] = mincenter
    metric = np.zeros((k, len(data_list)))
    for client in data_list:
        metric[int(client.result), assignment[client]] = metric[int(client.result), assignment[client]] + 1
    matched = 0.0
    for i in range(k):
        max = 0
        for j in range(len(data_list)):
            if metric[i, j] > max:
                max = metric[i, j]
        matched = matched + max
    return matched/len(data_list)


if __name__ == '__main__':
    file_name = 'dataset_1'
    sample_num = 20
    parsed_data = parse_data(file_name)
    print 'Succeed'
    sampled_data = random_sample(parsed_data, sample_num)
    print optimal_solution(sampled_data, 2)


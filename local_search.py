from optimal_solution import calculate_accuracy
import random

def local_search(data_list, k):
    num = len(data_list)
    random_begin = [random.randint(1, num) for x in range(k)]
    cur_acc = calculate_accuracy(data_list, random_begin, k)
    cur_state = random_begin
    while True:
        for i in range(num):
            for x in range(k):
                temp = cur_state
                temp[x] = i
                local_move_acc = calculate_accuracy(data_list, temp, k)
                if local_move_acc > 1.05 * cur_acc:
                    local_move_acc = 1.05* cur_acc
                    cur_state = temp
        break
    return local_move_acc
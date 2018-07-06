from data_parser import parse_data, random_sample
from optimal_solution import optimal_solution
from local_search import local_search
from kcenter import kcenter
from kmedian import kmedian
from local_search_capture import *
from ball_growing import *
import numpy as np
import matplotlib.pyplot as plt
from utils import *

if __name__ == '__main__':
    file_name = 'dataset_1'
    sample_num = 100
    k = 5
    print('Working on %s, Randomly select %d samples, %d Centers' % (file_name, sample_num, k))
    parsed_data = parse_data(file_name)
    print('Succeed in Parsing Data')
    tot_exp = 30
    control_kcenter = np.zeros(tot_exp)
    control_kmedian = np.zeros(tot_exp)
    control_kcenter_betas = np.zeros(tot_exp)
    control_kmedian_betas = np.zeros(tot_exp)

    exp_kcenter = np.zeros(tot_exp)
    exp_kmedian = np.zeros(tot_exp)
    exp_betas = np.zeros(tot_exp)
    bg_kcenter = np.zeros(tot_exp)
    bg_kmedian = np.zeros(tot_exp)
    bg_betas = np.zeros(tot_exp)

    #for alpha in [0.8, 1.0, 1.2]:
    for alpha in [0.8, 1.0, 1.2]:
    #for alpha in [1.0]:
        #for beta in [0.8, 1.0, 1.2]:
        #for beta in [0.8, 1.0]:
        for beta in [1.0]:
            for i in range(tot_exp):
                print('Experiment %d' % (i))
                sampled_data = random_sample(parsed_data, sample_num)
                #print 'Optimal %d Median Accuracy: %f' % (k, optimal_solution(sampled_data, k))
                #print 'Local Search %d Median Accuracy: %f' % (k, local_search(sampled_data, k))
                control_kcenter[i], control_kcenter_betas[i] = kcenter(sampled_data, k, alpha)
                control_kmedian[i], control_kmedian_betas[i] = kmedian(sampled_data, k, alpha)
                exp_kcenter[i], exp_kmedian[i], exp_betas[i] = local_search_capture(sampled_data, k, alpha, beta)
                bg_kcenter[i], bg_kmedian[i], bg_betas[i] = ball_growing(sampled_data, k, alpha)
            x = range(tot_exp)
            fig = plt.figure(figsize=(12, 4.8))  # dpi=100
            #ax1 = fig.add_subplot(121)
            #ax2 = fig.add_subplot(122)
            ax1 = fig.add_subplot(131)
            ax2 = fig.add_subplot(132)
            ax3 = fig.add_subplot(133)

            ax1.plot(x, control_kcenter, color = 'green')
            ax1.plot(x, exp_kcenter, color = 'red')
            ax1.plot(x, bg_kcenter, color = 'black')
            ax2.plot(x, control_kmedian, color = 'blue')
            ax2.plot(x, exp_kmedian, color ='red')
            ax2.plot(x, bg_kmedian, color ='black')
            ax3.plot(x, control_kcenter_betas, color = 'green')
            ax3.plot(x, control_kmedian_betas, color = 'blue')
            ax3.plot(x, exp_betas, color ='red')
            ax3.plot(x, bg_betas, color ='black')
            plt.title('alpha=%.1f, beta=%.1f: k-center green, k-median blue, local search red, ball growing black' % (alpha, beta))
            plt.savefig('Ball growing, k=%d, alpha = %.1f, beta =%.1f.png' % (k, alpha, beta))

            """
            # Protected Groups
            criteria = [9, 8, 3]  # Gender, race, highest degree
            x = range(tot_exp)
            fig = plt.figure(figsize=(12, 4.8))  # dpi=100
            for crit_index in range(len(criteria)):
                grouped_exp_betas = np.zeros(tot_exp)
                grouped_control_kcenter_betas = np.zeros(tot_exp)
                grouped_control_kmedian_betas = np.zeros(tot_exp)
                ungrouped_exp_betas = np.zeros(tot_exp)
                ungrouped_control_kcenter_betas = np.zeros(tot_exp)
                ungrouped_control_kmedian_betas = np.zeros(tot_exp)
                crit = criteria[crit_index]
                for i in range(tot_exp):
                    print('Experiment %d' % (i))
                    sampled_data = random_sample(parsed_data, sample_num)
                    sampled_groups = generate_groups(sampled_data, crit)
                    xx, grouped_control_kcenter_betas[i] = kcenter(sampled_data, k, alpha, groups_list=sampled_groups)
                    xx, grouped_control_kmedian_betas[i] = kmedian(sampled_data, k, alpha, groups_list=sampled_groups)
                    xx, yy, grouped_exp_betas[i] = local_search_capture_groups(sampled_data, sampled_groups, k, alpha, beta)
                    xx, ungrouped_control_kcenter_betas[i] = kcenter(sampled_data, k, alpha)
                    xx, ungrouped_control_kmedian_betas[i] = kmedian(sampled_data, k, alpha)
                    xx, yy, ungrouped_exp_betas[i] = local_search_capture(sampled_data, k, alpha, beta)

                ax = fig.add_subplot(130 + crit_index + 1)
                ax.plot(x, ungrouped_control_kcenter_betas, color = 'green', dashes = [6, 2], label = 'k-center without groups')
                ax.plot(x, ungrouped_control_kmedian_betas, color = 'blue', dashes = [6, 2], label = 'k-median without groups')
                ax.plot(x, ungrouped_exp_betas, color ='red', dashes = [6, 2], label = 'local search without groups')
                ax.plot(x, grouped_control_kcenter_betas, color = 'green', label = 'k-center with groups')
                ax.plot(x, grouped_control_kmedian_betas, color = 'blue', label = 'k-median with groups')
                ax.plot(x, grouped_exp_betas, color ='red', label = 'local search with groups')

            plt.title('Gender Race Degree alpha=%.1f,beta=%.1f' % (alpha, beta))
            #plt.savefig('k=5, alpha = %.1f, beta =%.1f.png' % (alpha, beta))
            plt.savefig('k=5, alpha = %.1f, beta =%.1f, protected groups.png' % (alpha, beta))
            """


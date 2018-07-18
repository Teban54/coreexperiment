from data_parser import parse_data, random_sample
from optimal_solution import optimal_solution
from local_search import local_search
from kcenter import kcenter
from kmedian import kmedian
from local_search_capture import *
from ball_growing import *
from ball_growing_groups import *
import numpy as np
import matplotlib.pyplot as plt
from utils import *
import statistics

if __name__ == '__main__':
    file_name = 'dataset_1'
    sample_num = 200  # 100
    # k = 5
    min_k = 2
    max_k = 50
    k_step = 4 # 2
    # print('Working on %s, Randomly select %d samples, %d Centers' % (file_name, sample_num, k))
    print('Working on %s, Randomly select %d samples, k from %d to %d' % (file_name, sample_num, min_k, max_k))
    parsed_data = parse_data(file_name)
    print('Succeed in Parsing Data')
    tot_exp = 10 # 20
    criteria = [9, 8, 3]  # Gender, race, highest degree
    criteria_text = ['Gender', 'Race', 'Educational Status']

    #for alpha in [0.8, 1.0, 1.2]:
    #for alpha in [0.8, 1.0, 1.2]:
    for alpha in [1.0]:
        #for beta in [0.8, 1.0, 1.2]:
        #for beta in [0.8, 1.0]:
        for beta in [1.0]:
            k_values = range(min_k, max_k + 1, k_step)
            control_kcenter_avg, control_kcenter_betas_avg = [], []
            control_kcenter_grouped_betas_avg = []
            control_kmedian_avg, control_kmedian_betas_avg = [], []
            control_kmedian_grouped_betas_avg = []

            exp_kcenter_avg, exp_kmedian_avg, exp_betas_avg = [], [], []
            exp_grouped_betas_avg = []
            bg_kcenter_avg, bg_kmedian_avg, bg_betas_avg = [], [], []
            bg_grouped_betas_avg = []
            bg_km_kcenter_avg, bg_km_kmedian_avg, bg_km_betas_avg = [], [], []
            bg_km_grouped_betas_avg = []
            bg_bg_kcenter_avg, bg_bg_kmedian_avg, bg_bg_betas_avg = [], [], []
            bg_bg_grouped_betas_avg = []
            for crit_index in range(len(criteria)):
                control_kcenter_grouped_betas_avg.append([])
                control_kmedian_grouped_betas_avg.append([])
                exp_grouped_betas_avg.append([])
                bg_grouped_betas_avg.append([])
                bg_km_grouped_betas_avg.append([])
                bg_bg_grouped_betas_avg.append([])
            for k in k_values:
                print('k = %d' % k)
                control_kcenter, control_kcenter_betas = np.zeros(tot_exp), np.zeros(tot_exp)
                control_kcenter_grouped_betas = []  # [crit_index] stores results of all experiments on a specific criteria
                control_kmedian, control_kmedian_betas = np.zeros(tot_exp), np.zeros(tot_exp)
                control_kmedian_grouped_betas = []
                exp_kcenter, exp_kmedian, exp_betas = np.zeros(tot_exp), np.zeros(tot_exp), np.zeros(tot_exp)
                exp_grouped_betas = []
                bg_kcenter, bg_kmedian, bg_betas = np.zeros(tot_exp), np.zeros(tot_exp), np.zeros(tot_exp)
                bg_grouped_betas = []
                bg_km_kcenter, bg_km_kmedian, bg_km_betas = np.zeros(tot_exp), np.zeros(tot_exp), np.zeros(tot_exp)
                bg_km_grouped_betas = []
                bg_bg_kcenter, bg_bg_kmedian, bg_bg_betas = np.zeros(tot_exp), np.zeros(tot_exp), np.zeros(tot_exp)
                bg_bg_grouped_betas = []
                for crit_index in range(len(criteria)):
                    control_kcenter_grouped_betas.append([])
                    control_kmedian_grouped_betas.append([])
                    exp_grouped_betas.append([])
                    bg_grouped_betas.append([])
                    bg_km_grouped_betas.append([])
                    bg_bg_grouped_betas.append([])
                for i in range(tot_exp):
                    print('Experiment %d' % (i))
                    sampled_data = random_sample(parsed_data, sample_num)
                    sampled_groups = []
                    sampled_groups_index = []
                    for crit_index in range(len(criteria)):
                        crit = criteria[crit_index]
                        groups, groups_index = generate_groups(sampled_data, crit)
                        sampled_groups.append(groups)
                        sampled_groups_index.append(groups_index)
                    distances = calc_distances(sampled_data)

                    control_kcenter[i], control_kcenter_betas[i], kcenter_facils = kcenter(sampled_data, k, alpha, distances=distances)
                    control_kmedian[i], control_kmedian_betas[i], kmedian_facils = kmedian(sampled_data, k, alpha, distances=distances)
                    for crit_index in range(len(criteria)):
                        control_kcenter_grouped_betas[crit_index].append(
                            calc_beta_groups(sampled_data, sampled_groups[crit_index], kcenter_facils, k, alpha))
                        control_kmedian_grouped_betas[crit_index].append(
                            calc_beta_groups(sampled_data, sampled_groups[crit_index], kmedian_facils, k, alpha))

                    exp_kcenter[i], exp_kmedian[i], exp_betas[i] = local_search_capture(sampled_data, k, alpha, beta, distances=distances)
                    for crit_index in range(len(criteria)):
                        _, _, grouped_beta = local_search_capture_groups(
                            sampled_data, sampled_groups[crit_index], k, alpha, beta, distances=distances)
                        exp_grouped_betas[crit_index].append(grouped_beta)

                    bg_kcenter[i], bg_kmedian[i], bg_betas[i] = ball_growing(sampled_data, k, alpha, distances=distances)
                    for crit_index in range(len(criteria)):
                        _, _, grouped_beta = ball_growing_groups(
                            sampled_data, sampled_groups[crit_index], sampled_groups_index[crit_index], k, alpha, distances=distances)
                        bg_grouped_betas[crit_index].append(grouped_beta)
                    bg_km_kcenter[i], bg_km_kmedian[i], bg_km_betas[i] = ball_growing_k_median(sampled_data, k, alpha, distances=distances)
                    for crit_index in range(len(criteria)):
                        _, _, grouped_beta = ball_growing_k_median_groups(
                            sampled_data, sampled_groups[crit_index], sampled_groups_index[crit_index], k, alpha, distances=distances)
                        bg_km_grouped_betas[crit_index].append(grouped_beta)
                    bg_bg_kcenter[i], bg_bg_kmedian[i], bg_bg_betas[i] = ball_growing_repeated(sampled_data, k, alpha, distances=distances)
                    for crit_index in range(len(criteria)):
                        _, _, grouped_beta = ball_growing_repeated_groups(
                            sampled_data, sampled_groups[crit_index], sampled_groups_index[crit_index], k, alpha, distances=distances)
                        bg_bg_grouped_betas[crit_index].append(grouped_beta)

                control_kcenter_avg.append(statistics.mean(control_kcenter))
                control_kmedian_avg.append(statistics.mean(control_kmedian))
                control_kcenter_betas_avg.append(statistics.mean(control_kcenter_betas))
                control_kmedian_betas_avg.append(statistics.mean(control_kmedian_betas))
                exp_kcenter_avg.append(statistics.mean(exp_kcenter))
                exp_kmedian_avg.append(statistics.mean(exp_kmedian))
                exp_betas_avg.append(statistics.mean(exp_betas))
                bg_kcenter_avg.append(statistics.mean(bg_kcenter))
                bg_kmedian_avg.append(statistics.mean(bg_kmedian))
                bg_betas_avg.append(statistics.mean(bg_betas))
                bg_km_kcenter_avg.append(statistics.mean(bg_km_kcenter))
                bg_km_kmedian_avg.append(statistics.mean(bg_km_kmedian))
                bg_km_betas_avg.append(statistics.mean(bg_km_betas))
                bg_bg_kcenter_avg.append(statistics.mean(bg_bg_kcenter))
                bg_bg_kmedian_avg.append(statistics.mean(bg_bg_kmedian))
                bg_bg_betas_avg.append(statistics.mean(bg_bg_betas))
                for crit_index in range(len(criteria)):
                    control_kcenter_grouped_betas_avg[crit_index].append(statistics.mean(control_kcenter_grouped_betas[crit_index]))
                    control_kmedian_grouped_betas_avg[crit_index].append(statistics.mean(control_kmedian_grouped_betas[crit_index]))
                    exp_grouped_betas_avg[crit_index].append(statistics.mean(exp_grouped_betas[crit_index]))
                    bg_grouped_betas_avg[crit_index].append(statistics.mean(bg_grouped_betas[crit_index]))
                    bg_km_grouped_betas_avg[crit_index].append(statistics.mean(bg_km_grouped_betas[crit_index]))
                    bg_bg_grouped_betas_avg[crit_index].append(statistics.mean(bg_bg_grouped_betas[crit_index]))

            x = k_values
            fig = plt.figure(figsize=(12, 4.8))  # dpi=100

            # Protected groups
            for crit_index in range(len(criteria)):
                ax = fig.add_subplot(100 + len(criteria) * 10 + crit_index + 1)
                ax.set_title(criteria_text[crit_index])
                ax.set_xlabel('k')
                ax.set_ylabel('beta')
                ax.plot(x, control_kcenter_betas_avg, color='green', label='k-center, no groups')
                ax.plot(x, control_kmedian_betas_avg, color='blue', label='k-median, no groups')
                ax.plot(x, exp_betas_avg, color='red', label='local search, no groups')
                ax.plot(x, bg_betas_avg, color='black', label='ball growing, no groups')
                ax.plot(x, bg_km_betas_avg, color='navy', label='ball growing + k-median, no groups')
                ax.plot(x, bg_bg_betas_avg, color='gray', label='ball growing repeated, no groups')
                ax.plot(x, control_kcenter_grouped_betas_avg[crit_index], color='green', dashes = [4, 2], label='k-center, with groups')
                ax.plot(x, control_kmedian_grouped_betas_avg[crit_index], color='blue', dashes = [4, 2], label='k-median, with groups')
                ax.plot(x, exp_grouped_betas_avg[crit_index], color='red', dashes = [4, 2], label='local search, with groups')
                ax.plot(x, bg_grouped_betas_avg[crit_index], color='black', dashes = [4, 2], label='ball growing, with groups')
                ax.plot(x, bg_km_grouped_betas_avg[crit_index], color='navy', dashes = [4, 2], label='ball growing + k-median, with groups')
                ax.plot(x, bg_bg_grouped_betas_avg[crit_index], color='gray', dashes = [4, 2], label='ball growing repeated, with groups')
                if crit_index == len(criteria) - 1:
                    ax.legend(fontsize='xx-small')

            """
            # No protected groups
            ax1 = fig.add_subplot(131)
            ax1.set_title('k-center objective')
            ax1.set_xlabel('k')
            ax1.set_ylabel('obj')
            ax2 = fig.add_subplot(132)
            ax2.set_title('k-median objective')
            ax2.set_xlabel('k')
            ax2.set_ylabel('obj')
            ax3 = fig.add_subplot(133)
            ax3.set_title('beta fairness measure')
            ax3.set_xlabel('k')
            ax3.set_ylabel('beta')

            ax1.plot(x, control_kcenter_avg, color='green', label='k-center')
            ax1.plot(x, exp_kcenter_avg, color='red', label='local search')
            ax1.plot(x, bg_kcenter_avg, color='black', label='ball growing')
            ax1.plot(x, bg_km_kcenter_avg, color='navy', label='ball growing + k-median')
            ax1.plot(x, bg_bg_kcenter_avg, color='gray', label='ball growing repeated')
            ax2.plot(x, control_kmedian_avg, color='blue', label='k-median')
            ax2.plot(x, exp_kmedian_avg, color='red', label='local search')
            ax2.plot(x, bg_kmedian_avg, color='black', label='ball growing')
            ax2.plot(x, bg_km_kmedian_avg, color='navy', label='ball growing + k-median')
            ax2.plot(x, bg_bg_kmedian_avg, color='gray', label='ball growing repeated')
            ax3.plot(x, control_kcenter_betas_avg, color='green', label='k-center')
            ax3.plot(x, control_kmedian_betas_avg, color='blue', label='k-median')
            ax3.plot(x, exp_betas_avg, color='red', label='local search')
            ax3.plot(x, bg_betas_avg, color='black', label='ball growing')
            ax3.plot(x, bg_km_betas_avg, color='navy', label='ball growing + k-median')
            ax3.plot(x, bg_bg_betas_avg, color='gray', label='ball growing repeated')
            ax1.legend(fontsize='small')
            ax2.legend(fontsize='small')
            ax3.legend(fontsize='small')
            """

            plt.suptitle('alpha=%.1f, beta=%.1f' % (alpha, beta))
            # plt.savefig('Ball growing, k=%d, alpha = %.1f, beta =%.1f.png' % (k, alpha, beta))
            plt.savefig('alpha = %.1f, beta = %.1f.png' % (alpha, beta))

            """
            # Protected Groups (old)
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


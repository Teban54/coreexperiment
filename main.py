from data_parser import parse_data, random_sample
from optimal_solution import optimal_solution
from local_search import local_search
from kcenter import kcenter
from kmedian import kmedian
from local_search_capture import local_search_capture
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    file_name = 'dataset_1'
    sample_num = 100
    k = 2
    print 'Working on %s, Randomly select %d samples, %d Centers' % (file_name, sample_num, k)
    parsed_data = parse_data(file_name)
    print 'Succeed in Parsing Data'
    tot_exp = 30
    control_kcenter = np.zeros(tot_exp)
    control_kmedian = np.zeros(tot_exp)

    exp_kcenter = np.zeros(tot_exp)
    exp_kmedian = np.zeros(tot_exp)

    for alpha in [0.8, 1.0, 1.2]:
        for beta in [0.8, 1.0, 1.2]:
            for i in range(tot_exp):
                print 'Experiment %d' % (i)
                sampled_data = random_sample(parsed_data, sample_num)
                #print 'Optimal %d Median Accuracy: %f' % (k, optimal_solution(sampled_data, k))
                #print 'Local Search %d Median Accuracy: %f' % (k, local_search(sampled_data, k))
                control_kcenter[i] = kcenter(sampled_data, k)
                control_kmedian[i] = kmedian(sampled_data, k)
                exp_kcenter[i], exp_kmedian[i] = local_search_capture(sampled_data, k, alpha, beta)
            x = range(tot_exp)
            fig = plt.figure()
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.plot(x, control_kcenter, color = 'green')
            ax1.plot(x, exp_kcenter, color = 'red')
            ax2.plot(x, control_kmedian, color = 'green')
            ax2.plot(x, exp_kmedian, color ='red')
            plt.title('Center Median alpha=%.1f,beta=%.1f' % (alpha, beta))
            plt.savefig('alpha = %.1f, beta =%.1f.png' % (alpha, beta))




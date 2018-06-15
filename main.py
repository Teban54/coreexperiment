from data_parser import parse_data, random_sample
from optimal_solution import optimal_solution
from local_search import local_search
from kcenter import kcenter
from kmedian import kmedian
from local_search_capture import local_search_capture

if __name__ == '__main__':
    file_name = 'dataset_1'
    sample_num = 20
    k = 2
    print 'Working on %s, Randomly select %d samples, %d Centers' % (file_name, sample_num, k)
    parsed_data = parse_data(file_name)
    print 'Succeed in Parsing Data'
    sampled_data = random_sample(parsed_data, sample_num)
    #print 'Optimal %d Median Accuracy: %f' % (k, optimal_solution(sampled_data, k))
    #print 'Local Search %d Median Accuracy: %f' % (k, local_search(sampled_data, k))
    #kcenter(parsed_data, k)
    #kmedian(parsed_data, k)
    local_search_capture(parsed_data, k)




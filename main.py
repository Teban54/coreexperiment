from data_parser import parse_data, random_sample
from optimal_solution import optimal_solution
from local_search import local_search

if __name__ == '__main__':
    file_name = 'dataset_1'
    sample_num = 20
    k = 2
    print 'Working on %s, Randomly select %d samples, %d Median' % (file_name, sample_num, k)
    parsed_data = parse_data(file_name)
    print 'Succeed in Parsing Data'
    sampled_data = random_sample(parsed_data, sample_num)
    print 'Optimal %d Median Accuracy: %f' % (k, optimal_solution(sampled_data, 2))
    print 'Local Search %d Median Accuracy: %f' % (k, local_search(sampled_data, 2))


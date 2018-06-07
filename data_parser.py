import random

def represent_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class data_pt:
    def __init__(self, content, flag):
        if flag == 'raw':
            self.data = content[: -1]
            self.dim = len(content) - 1
            self.result = content[-1]
            self.raw_data = content

    def __str__(self):
        return ','.join(self.raw_data)


def error_check(data):
    for entry in data:
        if entry == '?':
            return False
    return True

def convert_to_num(line_data, convert_map):
    modified_data = list()
    for i in range(len(line_data)):
        if represent_int(line_data[i]):
            modified_data.append(line_data[i])
            continue
        if not line_data[i] in convert_map[i]:
            convert_map[i][line_data[i]] = str(len(convert_map[i]))
        modified_data.append(convert_map[i][line_data[i]])
    return modified_data

def parse_data(file_name):
    data_list = []
    convert_map = []
    with open(file_name) as f:
        content = f.readlines()
        for i in range(len(content[0].split(','))):
            convert_map.append(dict())
        for content_line in content:
            line_data = content_line.split(',')
            line_data = convert_to_num(line_data, convert_map)
            if error_check(line_data):
                data_list.append(data_pt(line_data, 'raw'))
    return data_list


def random_sample(parsed_data, num):
    s = set()
    data_list = []
    while (len(s) <= num):
        t = random.randint(0, len(parsed_data) - 1)
        if not t in s:
            s.add(parsed_data[t])
            data_list.append(parsed_data[t])
    return data_list



if __name__ == '__main__':
    file_name = 'dataset_1'
    sample_num = 10
    parsed_data = parse_data(file_name)
    print 'Succeed'
    sampled_data = random_sample(parsed_data, sample_num)
    for i in sampled_data:
        print i

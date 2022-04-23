from src.RBTree import RBTree
from timeit import default_timer

DATASET_PATH = 'C:\\Users\\dasha\\PycharmProjects\\red-black-tree\\dataset\\data'
examples = ['\\100.csv', '\\1000.csv', '\\10000.csv', '\\100000.csv', '\\1000000.csv']

for index, example in enumerate(examples):
    for _ in range(10):
        summ = 0
        with open(DATASET_PATH + '\\insert\\05' + example, 'r') as input_file:
            tree = RBTree()
            for line in input_file:
                key, value = line.split()
                start_time = default_timer()
                tree[key] = value
                summ += (default_timer() - start_time) * 10**3
        print(tree.size)
        with open(DATASET_PATH + '\\metric05.txt', 'a') as output_file:
            output_file.write(f'{summ}\n')

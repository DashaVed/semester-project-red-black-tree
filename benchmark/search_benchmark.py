from src.RBTree import RBTree
from timeit import default_timer

DATASET_PATH = 'C:\\Users\\dasha\\PycharmProjects\\red-black-tree\\dataset\\data'
examples = ['\\100.csv', '\\1000.csv', '\\10000.csv', '\\100000.csv', '\\1000000.csv']


def insert_node(example, tree):
    with open(DATASET_PATH + '\\get\\05' + example, 'r') as input_file:
        for line in input_file:
            key, value = line.split()
            tree[key] = value


if __name__ == "__main__":
    for example in examples:
        tree = RBTree()
        insert_node(example, tree)
        for i in range(10):
            summ = 0
            with open(DATASET_PATH + '\\get\\05' + example, 'r') as input_file:
                for line in input_file:
                    key, value = line.split()
                    start_time = default_timer()
                    node_value = tree[key]
                    summ += (default_timer() - start_time) * 10 ** 3
            print(tree.size)
            with open(DATASET_PATH + '\\search_metric05.txt', 'a') as output_file:
                output_file.write(f'{summ}\n')

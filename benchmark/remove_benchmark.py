import random
from src.RBTree import RBTree
from timeit import default_timer

DATASET_PATH = 'C:\\Users\\dasha\\PycharmProjects\\red-black-tree\\dataset\\data'
examples = ['\\100.csv', '\\1000.csv', '\\10000.csv', '\\100000.csv', '\\1000000.csv']



def insert_node(example, tree):
    with open(DATASET_PATH + '\\delete\\01' + example, 'r') as input_file:
        for line in input_file:
            key, value = line.split()
            tree[key] = value


if __name__ == "__main__":
    for example in examples:
        for i in range(10):
            summ = 0
            with open(DATASET_PATH + '\\delete\\01' + example, 'r') as input_file:
                lines = input_file.readlines()
                temporary_sum = 0
                for _ in range(5):
                    tree = RBTree()
                    insert_node(example, tree)
                    key, value = random.choice(lines).strip().split()
                    start_time = default_timer()
                    del(tree[key])
                    temporary_sum += (default_timer() - start_time) * 10 ** 3
                    tree[key] = value
                    summ += temporary_sum / 5
            print(tree.size)
            with open(DATASET_PATH + '\\remove_metric01.txt', 'a') as output_file:
                output_file.write(f'{summ}\n')

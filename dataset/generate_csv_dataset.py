import argparse
from random import randint

DEFAULT_DESCRIPTION = 'CSV dataset generator script demo.'
DEFAULT_SAMPLES = 100


def parse_args():
    """
    Парсинг аргументов командной строки (CLI).
    :return интерфейс для работы с аргументами.

    Больше информации на https://docs.python.org/3.7/howto/argparse.html
    """
    parser = argparse.ArgumentParser(description=DEFAULT_DESCRIPTION)

    parser.add_argument('output',
                        type=str,
                        help='output CSV file, e.g. data/output.csv')

    parser.add_argument('--samples',
                        type=int,
                        default=DEFAULT_SAMPLES,
                        help='number of samples to generate (default: {})'.format(DEFAULT_SAMPLES))

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    # валидация аргументов
    if args.samples < 0:
        raise ValueError('Number of samples must be greater than 0.')

    # запись данных в файл
    with open(args.output, 'w') as file:
        for _ in range(args.samples - 1):
            file.write('{0} {1}\n'.format(randint(1, args.samples//2), randint(1, 15)))
        file.write('{0} {1}\n'.format(randint(1, 15), randint(1, 15)))

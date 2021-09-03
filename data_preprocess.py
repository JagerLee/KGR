import pandas as pd
import os
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='data processing of knowledge graph tuples.')
    parser.add_argument('-t', '--test', dest='test_size', type=float, default=0.1,
                        help='Test size of knowledge graph tuples. Default: 0.1.')
    parser.add_argument('-v', '--val', dest='valid_size', type=float, default=0.1,
                        help='Valid size of knowledge graph tuples. Default: 0.1.')
    parser.add_argument('-i', '--input', dest='input_file', type=str,
                        help='Input knowledge graph tuples file path.')

    return parser.parse_args()


def train_test_split(df, valid_size=0.1, test_size=0.1, shuffle=True):
    if shuffle:
        df = df.sample(frac=1).reset_index(drop=True)
    valid_num = int(valid_size * df.shape[0])
    train_num = df.shape[0] - int(test_size * df.shape[0]) - valid_num

    train_df = df[:train_num]
    valid_df = df[train_num:train_num + valid_num]
    test_df = df[train_num + valid_num:]

    return train_df, valid_df, test_df


def data_preproccess():
    args = get_args()
    test_size = args.test_size
    valid_size = args.valid_size
    input_file = args.input_file
    df = pd.read_csv(input_file, header=0, encoding='utf-8')
    data_path = 'data/train'
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    train_path = os.path.join(data_path, 'train.txt')
    valid_path = os.path.join(data_path, 'valid.txt')
    test_path = os.path.join(data_path, 'test.txt')

    train_df, valid_df, test_df = train_test_split(df, valid_size, test_size)
    train_df.to_csv(train_path, sep='\t', header=None, index=False)
    valid_df.to_csv(valid_path, sep='\t', header=None, index=False)
    test_df.to_csv(test_path, sep='\t', header=None, index=False)


if __name__ == '__main__':
    data_preproccess()

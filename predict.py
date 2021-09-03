import os
import argparse
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(description='predict nodes from given node and relation.')
    parser.add_argument('-n', '--node', dest='node', type=str,
                        help='Input node file.')
    parser.add_argument('-r', '--relation', dest='rel', type=str,
                        help='Input relation file.')
    parser.add_argument('-k', '--topk', dest='k', type=int, default=10,
                        help='How many results are returned. Default: 10.')

    return parser.parse_args()


def load_nodes(nodes_file):
    df = pd.read_csv('data/train/entities.tsv', header=None, sep='\t', encoding='utf-8')
    df.loc[:, 1].to_csv(nodes_file, header=0, index=0, encoding='utf-8')


def predict():
    args = get_args()
    head_file = args.node
    rel_file = args.rel
    k = args.k
    if not os.path.exists('data/predict'):
        os.mkdir('data/predict')
    tail_file = 'data/predict/whole_nodes.list'
    load_nodes(tail_file)
    os.system('DGLBACKEND=pytorch dglke_predict --model_path ckpts/ComplEx_mydataset_0/ --format \'h_r_t\' --data_files'
              + ' ' + head_file + ' ' + rel_file + ' ' + tail_file + ' --topK ' + str(k) + ' --exec_mode \'batch_head\''
              ' --raw_data --entity_mfile data/train/entities.tsv --rel_mfile data/train/relations.tsv'
              )


if __name__ == '__main__':
    predict()

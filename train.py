import os
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='train dgl from knowledge graph.')
    parser.add_argument('-b', '--batch',  dest='batch_size', type=int, default=1024,
                        help='Batch size of training, multiple of 4. Default: 1024')
    parser.add_argument('-lr', '--lr', dest='lr', type=float, default=0.01,
                        help='Learning rate of training. Default: 0.01')
    parser.add_argument('-s', '--step', dest='max_step', type=int, default=40000,
                        help='Max steps of training(>= 10000). Default: 40000')

    return parser.parse_args()


def train():
    args = get_args()
    batch_size = args.batch_size
    lr = args.lr
    max_step = args.max_step
    if not os.path.exists('train_log'):
        os.mkdir('train_log')
    os.system('DGLBACKEND=pytorch nohup dglke_train --model_name ComplEx --dataset mydataset --data_path ./data/train/ '
              '--data_files train.txt valid.txt test.txt --format raw_udd_hrt --batch_size ' + str(batch_size) +
              ' --neg_sample_size ' + str(int(batch_size / 4)) + ' --hidden_dim 512 --gamma 50 --lr ' + str(lr) +
              ' --num_thread 4 --regularization_coef 2.00E-07 --batch_size_eval ' + str(batch_size) + ' --test -adv '
              '--mix_cpu_gpu --num_proc 2 --gpu 0 1 --max_step ' + str(max_step) + ' --neg_sample_size_eval ' +
              str(batch_size) + ' --log_interval ' + str(batch_size) + ' --async_update --rel_part --force_sync_'
              'interval 10000 > train_log/mydataset.log 2>&1 &'
              )


if __name__ == '__main__':
    train()

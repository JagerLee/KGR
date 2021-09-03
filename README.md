# KGR

## 环境需求

系统:linux
```
torch==1.6.0
dgl==0.4.3
dglke==0.1.2
```
注：dglke通过源码安装，否则0.1.2版本会报错

## 原始数据

- 知识图谱三元组 data/source_data/tuples.csv

id(a):头结点; type(b):关系链; id(b):尾结点
```
id(a),type(r),id(b)
931825,子类,2
31765,发生部位,2
35294,发生部位,2
66659,发生部位,2
99297,发生部位,2
69239,发生部位,2
92351,发生部位,2
...
```

## 数据预处理

- usage
```
python data_preprocess.py -h
```
```
data processing of knowledge graph tuples.

optional arguments:
  -h, --help            show this help message and exit
  -t TEST_SIZE, --test TEST_SIZE
                        test size of knowledge graph tuples. Default: 0.1.
  -v VALID_SIZE, --val VALID_SIZE
                        valid size of knowledge graph tuples. Default: 0.1.
  -i INPUT_FILE, --input INPUT_FILE
                        knowledge graph tuples file path.
```

- run
```
python data_preprocess.py -t 0.1 -v 0.1 -i data/source_data/tuples.csv
```

- result

训练集  data/train/train.txt

验证集  data/train/valid.txt

测试集  data/train/test.txt

节点编码  data/train/entities.tsv

链接编码  data/train/relations.tsv

## 训练

- usage 
```
python train.py -h
```
```
train dgl from knowledge graph.

optional arguments:
  -h, --help            show this help message and exit
  -b BATCH_SIZE, --batch BATCH_SIZE
                        Batch size of training, multiple of 4. Default: 1024
  -lr LR, --lr LR       Learning rate of training. Default: 0.01
  -s MAX_STEP, --step MAX_STEP
                        Max steps of training(>= 10000). Default: 40000
```

- run
```
python train.py -b 1024 -lr 0.01 -s 80000
```

- result

train
```
[proc 0][Train](79872/80000) average pos_loss: 0.17877843778114766
[proc 0][Train](79872/80000) average neg_loss: 0.26976426748296944
[proc 0][Train](79872/80000) average loss: 0.2242713526429725
[proc 0][Train](79872/80000) average regularization: 0.041346013596921694
[proc 0][Train] 1024 steps take 11.777 seconds
[proc 0]sample: 1.083, forward: 4.238, backward: 3.993, update: 2.457
proc 0 takes 869.088 seconds
training takes 874.0371513366699 seconds
Save model to ckpts/ComplEx_mydataset_0
```
test
```
-------------- Test result --------------
Test average MRR : 0.5189444347265852
Test average MR : 150.3310767776796
Test average HITS@1 : 0.46871126360268184
Test average HITS@3 : 0.5443966196179949
Test average HITS@10 : 0.6097203103705682
-----------------------------------------
testing takes 80.228 seconds
```

model

保存路径  ckpts/ComplEx_mydataset_0/

## 预测

- input

头节点  data/predict/node.list
```
0
5
100
```

关系链接  data/predict/rel.list
```
所在基因组
发生部位
```
注：输入文件为原始名称而非编码

- usage 
```
python predict.py -h
```
```
predict nodes from given node and relation.

optional arguments:
  -h, --help            show this help message and exit
  -n NODE, --node NODE  Input node file.
  -r REL, --relation REL
                        Input relation file.
  -k K, --topk K        How many results are returned. Default: 10.
```

- run
```
python predict.py -n data/predict/node.list -r data/predict/rel.list -k 5
```

- result

result.tsv
```
head	rel	tail	score
0	所在基因组	26425	-0.23086605966091156
0	所在基因组	727079	-0.5241658091545105
0	发生部位	575696	-0.5341730713844299
0	所在基因组	45640	-0.6790127158164978
0	发生部位	575698	-0.7586237788200378
5	所在基因组	727081	0.3719729781150818
5	所在基因组	26425	0.28864535689353943
5	所在基因组	45640	0.1332951784133911
5	所在基因组	727083	-0.18682646751403809
5	所在基因组	312573	-0.22891224920749664
10	发生部位	575697	2.772928237915039
10	发生部位	575696	2.7276782989501953
10	发生部位	195922	0.928019106388092
10	发生部位	205005	0.8934510350227356
10	发生部位	205152	0.8826712369918823
```

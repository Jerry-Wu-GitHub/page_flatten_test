# 任务书

这次任务是对上次任务的完善。

注：本仓库在你完成任务后会被删除，如有需要，请自己保存好。

## 准备

克隆本仓库：

```bash
git clone https://github.com/Jerry-Wu-GitHub/book_flatten.git
```

安装依赖：

```bash
cd book_flatten
pip install -r requirements.txt
```

## 任务一

提高准确度。

在 [`input`](input) 文件夹里有三组测试用例。对于每组测试用例：有4张左右的照片，拍的书本页面是一样的，但是角度不同。
- group1: 简单测试
- group2: 书页微微隆起
- group3: 书页边缘略有不全

理论上来说，每组内的4张图片经过 flatten 的结果应该是一样的，我用图片的 average hash 值（256位的0-1数组，即长度为32的字节串）的汉明距离来量化图片之间的相似度。这种哈希是一种局部敏感哈希（相似的图片的哈希结果也相似），且对图片的长宽比不敏感。具体的哈希细节你可以问问AI。

在 [`config.py`](config.py) 里定义了 `CHALLENGE_HASH_DIFF_THRESHOLD` 和 `BASE_HASH_DIFF_THRESHOLD` ，你的目标是：同一组内的图片两两之间的 average hash 的汉明距离占总比特数的比例不超过 `BASE_HASH_DIFF_THRESHOLD` 。如果能再好一点，不超过 `CHALLENGE_HASH_DIFF_THRESHOLD` 。

你的程序应该放在 [`book_flatten`](book_flatten) 文件夹内。然后，你可以运行 [`main.py`](main.py) ：

```bash
python main.py
```

就会输出测试结果：

```
CHALLENGE_HASH_DIFF_BYTES=20.48
BASE_HASH_DIFF_BYTES=38.4

==== Test group1 ====

处理图片 01.jpg ：耗时 0.33 秒
处理图片 02.jpg ：耗时 0.46 秒
处理图片 03.jpg ：耗时 0.34 秒
处理图片 04.jpg ：耗时 0.23 秒
平均耗时 0.34 秒
比较距离：01.jpg 与 02.jpg ：9
比较距离：01.jpg 与 03.jpg ：4
比较距离：01.jpg 与 04.jpg ：39
比较距离：02.jpg 与 03.jpg ：11
比较距离：02.jpg 与 04.jpg ：34
比较距离：03.jpg 与 04.jpg ：41

==== Test group2 ====

处理图片 01.jpg ：耗时 0.16 秒
处理图片 02.jpg ：耗时 0.16 秒
处理图片 03.jpg ：耗时 0.16 秒
处理图片 04.jpg ：耗时 0.15 秒
平均耗时 0.16 秒
比较距离：01.jpg 与 02.jpg ：25
比较距离：01.jpg 与 03.jpg ：21
比较距离：01.jpg 与 04.jpg ：29
比较距离：02.jpg 与 03.jpg ：38
比较距离：02.jpg 与 04.jpg ：48
比较距离：03.jpg 与 04.jpg ：38

==== Test group3 ====

处理图片 01.jpg ：耗时 0.22 秒
处理图片 02.jpg ：耗时 0.18 秒
处理图片 03.jpg ：耗时 0.17 秒
处理图片 04.jpg ：耗时 0.16 秒
平均耗时 0.18 秒
比较距离：01.jpg 与 02.jpg ：88
比较距离：01.jpg 与 03.jpg ：67
比较距离：01.jpg 与 04.jpg ：63
比较距离：02.jpg 与 03.jpg ：93
比较距离：02.jpg 与 04.jpg ：89
比较距离：03.jpg 与 04.jpg ：64
```

## 任务二

对于照片里识别不到页面，你的代码的原来的处理方式是返回原图，请你改成引发一个异常。

## 提交方式

更新你自己的仓库。
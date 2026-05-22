"""
评测程序。
"""

import os
import time

from image_hash import image_hash

from config import (
    HASH_METHOD, HASH_SIZE,
    AVG_TIME, MAX_TIME,
    CHALLENGE_HASH_DIFF_BYTES, BASE_HASH_DIFF_BYTES
)
from book_flatten.correct_paper import correct_paper


def hamming_distance_bytes(b1: bytes, b2: bytes) -> int:
    """
    计算两个字节串的汉明距离。
    """
    if len(b1) != len(b2):
        raise ValueError("两个字节串的长度必须相等")
    # sum()函数对生成器表达式求和
    # 对两个字节串的对应字节（整数形式）进行按位异或（^）
    # bin().count('1') 计算异或结果中二进制位为1的个数
    # 这样逐字节累加，得到总的比特差异数
    return sum(bin(b1[i] ^ b2[i]).count('1') for i in range(len(b1)))


def test_group(group_src: str, group_dst: str) -> None:
    """
    测试一组图片。
    """
    if not os.path.isdir(group_dst):
        os.mkdir(group_dst)

    image_hash_bytes: list[bytes] = []
    processing_time: list[float] = []

    filenames = []
    for filename in os.listdir(group_src):
        if not filename.endswith(".jpg"):
            continue
        filenames.append(filename)

        image_path = os.path.join(group_src, filename)
        with open(image_path, mode="rb") as file:
            image_bytes = file.read()

        # 处理图片
        print(f"处理图片 {filename} ：", end="")
        start_time = time.time()
        correct_image_bytes = correct_paper(image_bytes)
        end_time = time.time()

        # 判断单个用时
        time_consuming = end_time - start_time
        if time_consuming > MAX_TIME:
            print(f"耗时 \033[31m{time_consuming:.2f}\033[0m 秒")
        else:
            print(f"耗时 \033[32m{time_consuming:.2f}\033[0m 秒")
        processing_time.append(time_consuming)

        # 保存处理后的图片
        output_image_path = os.path.join(group_dst, filename)
        with open(output_image_path, mode="wb") as file:
            file.write(correct_image_bytes)

        # 计算局部敏感哈希
        image_hash_bytes.append(image_hash(
            correct_image_bytes,
            method=HASH_METHOD,
            hash_size=HASH_SIZE
        ))

    image_counts = len(filenames)

    # 判断平均用时
    avg_time_consuming = sum(processing_time, 0) / image_counts
    if avg_time_consuming > AVG_TIME:
        print(f"平均耗时 \033[31m{avg_time_consuming:.2f}\033[0m 秒")
    else:
        print(f"平均耗时 \033[32m{avg_time_consuming:.2f}\033[0m 秒")

    # 两两之间计算汉明距离
    for i in range(image_counts - 1):
        for j in range(i + 1, image_counts):
            print(f"比较距离：{filenames[i]} 与 {filenames[j]} ：", end="")
            dist = hamming_distance_bytes(image_hash_bytes[i], image_hash_bytes[j])
            if dist > BASE_HASH_DIFF_BYTES:
                print(f"\033[31m{dist}\033[0m")
            elif dist <= CHALLENGE_HASH_DIFF_BYTES:
                print(f"\033[32m{dist}\033[0m")
            else:
                print(dist)


def main(input_path: str = "input", output_path: str = "output"):
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    group_names = os.listdir(input_path)
    for group_name in group_names:
        print(f"\n==== Test {group_name} ====\n")
        group_src = os.path.join(input_path, group_name)
        group_dst = os.path.join(output_path, group_name)
        test_group(group_src, group_dst)


if __name__ == '__main__':
    main()

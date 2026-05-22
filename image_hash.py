import io
from typing import Literal

from PIL import Image
import imagehash


def hash_to_bytes(hash_obj: imagehash.ImageHash) -> bytes:
    """
    将 imagehash.ImageHash 对象转换为字节串。

    该函数提取哈希矩阵中的每一个二进制位（True/False），按行优先顺序每 8 位
    打包成一个字节，最终返回 bytes 对象。适用于存储或网络传输。

    参数
    ----------
    hash_obj : ImageHash
        imagehash 库中任意哈希方法返回的对象。

    返回
    -------
    bytes
        哈希位的字节表示，长度 = (hash_size * hash_size) / 8。
        例如 hash_size=8 (64 bits) 时返回 8 字节。

    示例
    -------
    >>> from PIL import Image
    >>> import imagehash
    >>> img = Image.open('example.jpg')
    >>> h = imagehash.average_hash(img)
    >>> b = hash_to_bytes(h)
    >>> print(len(b))  # 8
    """
    # 获取布尔型哈希矩阵
    hash_matrix = hash_obj.hash  # shape: (hash_size, hash_size)
    # 展平为一维布尔序列
    bits = hash_matrix.flatten()  # 长度为 n_bits

    # 将布尔序列转换为字节串
    # 每 8 个位组成一个字节，高位在前（与常见哈希字符串的十六进制表示一致）
    byte_list = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits) and bits[i + j]:
                byte |= (1 << (7 - j))  # 高位在前
        byte_list.append(byte)
    return bytes(byte_list)


def image_hash(
    data: bytes,
    method: Literal["average", "phash", "dhash", "whash"] = "average",
    hash_size: int = 16
) -> bytes:
    """
    根据输入的图片字节数据，计算指定方法的哈希值，并以字节串形式返回。

    该函数封装了 `imagehash` 库中常用的几种哈希算法，生成感知哈希后转换为字节串
    （每 8 位打包为一个字节）。可用于存储、传输或进一步处理。

    使用前请安装依赖：`pip install Pillow imagehash`

    参数
    ----------
    data : bytes
        图片文件的原始字节数据（例如从 `open('file.jpg', 'rb').read()` 获得）。
    method : str, optional
        哈希方法名称，支持：
        - "average" : 平均哈希 (aHash)，速度最快，对细节变化敏感度低。
        - "phash"   : 感知哈希 (pHash)，对缩放、旋转等变换鲁棒性更好。
        - "dhash"   : 差分哈希 (dHash)，基于梯度变化，对亮度对比度变化不敏感。
        - "whash"   : 小波哈希 (wHash)，基于离散小波变换，精确度较高。
        默认为 "average"。
    hash_size : int, optional
        哈希矩阵的边长，总位数 = hash_size * hash_size。必须为 8 的倍数以保证
        字节对齐（默认 16，得到 256 位 → 32 字节）。

    返回
    -------
    bytes
        哈希位的字节表示，长度 = (hash_size * hash_size) / 8。

    异常
    -------
    ValueError
        当 `method` 不支持或 `hash_size` 导致位数非 8 的倍数时抛出。
    PIL.UnidentifiedImageError
        当字节数据无法解码为有效图片时抛出。

    示例
    -------
    >>> with open('example.jpg', 'rb') as f:
    ...     img_bytes = f.read()
    >>> b = image_hash(img_bytes, method='phash', hash_size=8)
    >>> print(len(b))  # 8
    >>> print(b.hex()) # 十六进制字符串，如 'ffc3e0c0c0c0c0c0'
    """
    method = method.lower()

    method_map = {
        "average": imagehash.average_hash,
        "phash": imagehash.phash,
        "dhash": imagehash.dhash,
        "whash": imagehash.whash,
    }

    if method not in method_map:
        raise ValueError(
            f"不支持的哈希方法: '{method}'。"
            f"支持的方法: {list(method_map.keys())}"
        )

    # 检查总位数是否为 8 的倍数
    total_bits = hash_size * hash_size
    if total_bits % 8 != 0:
        raise ValueError(
            f"hash_size = {hash_size} 导致总位数 {total_bits} 不是 8 的倍数，"
            "无法转换为字节串。请使用 8 的倍数，例如 8、16、32。"
        )

    with Image.open(io.BytesIO(data)) as img:
        hash_obj = method_map[method](img, hash_size=hash_size)

    return hash_to_bytes(hash_obj)


if __name__ == '__main__':
    with open("sample/sample00.jpg", mode="rb") as file:
        img_bytes = file.read()
    result_bytes = image_hash(img_bytes, hash_size=16)
    print(f"字节长度: {len(result_bytes)}")          # 32 (256位)
    print(f"十六进制: {result_bytes.hex()}")        # 可读的十六进制串

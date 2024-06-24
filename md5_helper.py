# md5_calculator.py

import os
import hashlib


def calculate_md5(file_path):
    """
    计算文件的 MD5 值。
    :param file_path: 文件路径
    :return: 文件的 MD5 值
    """
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        # 分块读取文件内容并更新哈希对象
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()


def get_files_md5_map(directory):
    """
    对目录下的所有文件计算 MD5，并返回文件名和 MD5 值的映射。
    :param directory: 目录路径
    :return: 文件名和 MD5 值的映射字典
    """
    files_md5_map = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                md5_value = calculate_md5(file_path)
                # 去掉文件名的 .md 后缀
                file_name_without_ext = os.path.splitext(file)[0]
                files_md5_map[file_name_without_ext] = md5_value
    return files_md5_map


def save_files_md5_map_to_file(files_md5_map, output_file_path):
    with open(output_file_path, 'w') as file:
        for file_name, md5_value in files_md5_map.items():
            file.write(f"{file_name}: {md5_value}\n")


def load_files_md5_map_from_file(input_file_path):
    files_md5_map = {}
    with open(input_file_path, 'r') as file:
        for line in file:
            file_name, md5_value = line.strip().split(': ')
            files_md5_map[file_name] = md5_value
    return files_md5_map

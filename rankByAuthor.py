import re

def extract_first_author(entry):
    """提取 BibTeX 条目中的第一个作者的姓氏"""
    match = re.search(r"\\bibitem\[[^\]]*\]\{[^\}]*\}([^{,]+)", entry)
    if match:
        return match.group(1).strip()
    return ""

def sort_bibtex_entries(file_path, output_path):
    """按作者姓氏排序 BibTeX 条目"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用双换行分割每个 BibTeX 条目
    entries = content.split("\n\n")

    # 按第一个作者的姓氏排序
    sorted_entries = sorted(entries, key=extract_first_author)

    # 写入到新的文件
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n\n".join(sorted_entries))

    print(f"已排序的 BibTeX 条目保存到 {output_path}")

# 文件路径（替换为你的文件路径）
input_file = "/Users/jiangguanxuan/Downloads/Bibitem-Generator/reference.txt"
output_file = "/Users/jiangguanxuan/Downloads/Bibitem-Generator/1.0.txt"

# 确保输入文件存在
import os
if not os.path.exists(input_file):
    raise FileNotFoundError(f"输入文件不存在: {input_file}")


# 调用排序函数
sort_bibtex_entries(input_file, output_file)

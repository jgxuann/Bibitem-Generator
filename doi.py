import re
import requests

def get_doi(title):
    """通过 CrossRef API 查询文献的 DOI"""
    url = "https://api.crossref.org/works"
    params = {"query.title": title, "rows": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["message"]["items"]:
            return data["message"]["items"][0].get("DOI", None)
    return None

def process_file(input_file, output_file):
    """为文献条目添加 DOI"""
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    # 使用双换行分割文献条目
    entries = content.split("\n\n")
    processed_entries = []

    for entry in entries:
        title = None  # 初始化标题变量
        # 改进的标题提取正则表达式
        title_match = re.search(r"\\textit\{(.+?)\}", entry)  # 匹配 \textit{...} 里的内容
        if not title_match:
            title_match = re.search(r"\{(.+?)\}", entry)  # 如果没有 \textit{...}，尝试匹配其他大括号中的内容
        if title_match:
            title = title_match.group(1)
            print(f"正在查询标题: {title}")
            doi = get_doi(title)
            if doi:
                print(f"找到 DOI: {doi}")
                # 添加 DOI 字段
                entry = entry.strip() + f",\n  doi = {{{doi}}}\n"
            else:
                print(f"未找到 DOI: {title}")
        else:
            print(f"未提取到标题，跳过此条目")

        # 调试：打印当前条目和提取的标题
        print(f"当前条目:\n{entry}")
        if title:
            print(f"提取的标题: {title}")
        else:
            print("提取的标题: 无")

        processed_entries.append(entry)

    # 保存处理后的结果
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n\n".join(processed_entries))

    print(f"已处理的文献保存到: {output_file}")

# 文件路径（修改为你的文件路径）
input_file = "/Users/yangshirao/Desktop/learnDL/LMEM_IJHCS/1.0.txt"  # 输入文件路径
output_file = "/Users/yangshirao/Desktop/learnDL/LMEM_IJHCS/2.0.txt"  # 输出文件路径

# 调用函数
process_file(input_file, output_file)

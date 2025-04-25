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
input_file = "/Users/jiangguanxuan/Downloads/Bibitem-Generator/1.0.txt"  # 输入文件路径
output_file = "/Users/jiangguanxuan/Downloads/Bibitem-Generator/2.0.txt"  # 输出文件路径

# 调用函数
process_file(input_file, output_file)



# import re

# def format_bibitem(entry):
#     """将 BibTeX 条目转换为自定义 \bibitem 格式"""
#     # 提取字段
#     key_match = re.search(r"@.*?\{(.*?),", entry)
#     title_match = re.search(r"title=\{(.*?)\}", entry)
#     author_match = re.search(r"author=\{(.*?)\}", entry)
#     journal_match = re.search(r"journal=\{(.*?)\}", entry)
#     volume_match = re.search(r"volume=\{(.*?)\}", entry)
#     pages_match = re.search(r"pages=\{(.*?)\}", entry)
#     year_match = re.search(r"year=\{(.*?)\}", entry)
#     doi_match = re.search(r"doi=\{(.*?)\}", entry)

#     # 获取字段值
#     key = key_match.group(1) if key_match else "unknown_key"
#     title = title_match.group(1) if title_match else "Unknown Title"
#     author = author_match.group(1) if author_match else "Unknown Author"
#     journal = journal_match.group(1) if journal_match else "Unknown Journal"
#     volume = volume_match.group(1) if volume_match else "Unknown Volume"
#     pages = pages_match.group(1) if pages_match else "Unknown Pages"
#     year = year_match.group(1) if year_match else "Unknown Year"
#     doi = doi_match.group(1) if doi_match else "Unknown DOI"

#     # 格式化作者（只保留前两位作者，后面加 "et al."）
#     authors = author.split(" and ")
#     if len(authors) > 2:
#         author_formatted = f"{authors[0]}, {authors[1]}, et al."
#     else:
#         author_formatted = ", ".join(authors)

#     # 格式化为目标 \bibitem 格式
#     formatted_entry = (
#         f"\\bibitem[{authors[0]} et al.({year})]{{{key}}}\n"
#         f"  {author_formatted},\n"
#         f"  \\textit{{{title}}},\n"
#         f"  in: \\textit{{{journal}}}, vol. {volume}, pp. {pages}, {year}.,\n"
#         f"  doi = {{{doi}}}\n"
#     )
#     return formatted_entry

# def process_file(input_file, output_file):
#     """处理文件并将 BibTeX 条目转换为自定义格式"""
#     with open(input_file, "r", encoding="utf-8") as file:
#         content = file.read()

#     # 使用双换行分割条目
#     entries = content.split("\n\n")
#     processed_entries = []

#     for entry in entries:
#         if entry.strip():  # 跳过空条目
#             formatted_entry = format_bibitem(entry)
#             processed_entries.append(formatted_entry)

#     # 保存处理后的结果
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write("\n\n".join(processed_entries))

#     print(f"已处理的文献保存到: {output_file}")

# # 文件路径（修改为你的文件路径）
# input_file = "/Users/jiangguanxuan/Downloads/Bibitem-Generator/1.0.txt"  # 输入文件路径
# output_file = "/Users/jiangguanxuan/Downloads/Bibitem-Generator/2.0.txt"  # 输出文件路径

# # 调用函数
# process_file(input_file, output_file)

# import re

# def format_bibitem(entry):
#     """将 BibTeX 条目转换为自定义 \bibitem 格式"""
#     # 预处理：移除换行和多余空格，方便正则匹配
#     entry_clean = re.sub(r'\s+', ' ', entry.strip())
    
#     # 提取字段（优化正则表达式，支持跨行和简单嵌套）
#     key_match = re.search(r"@\w+\{([^,]+),", entry_clean)
#     title_match = re.search(r"title\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", entry_clean, re.IGNORECASE)
#     author_match = re.search(r"author\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", entry_clean, re.IGNORECASE)
#     journal_match = re.search(r"(journal|booktitle)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", entry_clean, re.IGNORECASE)
#     volume_match = re.search(r"volume\s*=\s*\{([^}]*)\}", entry_clean, re.IGNORECASE)
#     pages_match = re.search(r"pages\s*=\s*\{([^}]*)\}", entry_clean, re.IGNORECASE)
#     year_match = re.search(r"year\s*=\s*\{([^}]*)\}", entry_clean, re.IGNORECASE)
#     doi_match = re.search(r"doi\s*=\s*\{([^}]*)\}", entry_clean, re.IGNORECASE)

#     # 获取字段值（带默认值）
#     key = key_match.group(1) if key_match else "unknown_key"
#     title = title_match.group(1).strip('{}') if title_match else "Unknown Title"
#     author = author_match.group(1).strip('{}') if author_match else "Unknown Author"
#     journal = journal_match.group(2).strip('{}') if journal_match else "Unknown Journal"
#     volume = volume_match.group(1) if volume_match else "Unknown Volume"
#     pages = pages_match.group(1) if pages_match else "Unknown Pages"
#     year = year_match.group(1) if year_match else "Unknown Year"
#     doi = doi_match.group(1) if doi_match else "Unknown DOI"

#     # 处理作者格式
#     authors = [a.strip() for a in re.split(r"\s+and\s+", author)]
#     if len(authors) > 2:
#         author_formatted = f"{authors[0]}, {authors[1]}, et al."
#         short_cite = f"{authors[0]} et al.({year})"
#     else:
#         author_formatted = ", ".join(authors)
#         short_cite = f"{' & '.join(authors)} ({year})" if len(authors) > 1 else f"{authors[0]} ({year})"

#     # 构建格式化条目
#     return f"""\\bibitem[{short_cite}]{{{key}}}
#   {author_formatted},
#   \\textit{{{title}}},
#   in: \\textit{{{journal}}}, vol. {volume}, pp. {pages}, {year}.
#   doi: {{{doi}}}
# """

# def test_single_entry():
#     """交互式测试单个条目"""
#     print("\n\033[1;36m请输入BibTeX条目（输入空行结束）：\033[0m")
#     lines = []
#     while True:
#         try:
#             line = input()
#             if not line.strip() and len(lines) > 0:  # 允许空行结束输入
#                 break
#             lines.append(line)
#         except EOFError:  # 支持 Ctrl+D 结束输入
#             break
    
#     entry = "\n".join(lines)
#     if not entry.strip():
#         print("\033[91m错误：输入为空\033[0m")
#         return
    
#     try:
#         result = format_bibitem(entry)
#         print("\n\033[1;32m转换结果：\033[0m")
#         print(result)
#     except Exception as e:
#         print(f"\033[91m转换错误：{str(e)}\033[0m")

# def process_file(input_file, output_file):
#     """处理整个文件"""
#     with open(input_file, "r", encoding="utf-8") as f:
#         entries = re.split(r'\n\s*\n', f.read())  # 更健壮的分隔方式
    
#     with open(output_file, "w", encoding="utf-8") as f:
#         for entry in entries:
#             if entry.strip():
#                 f.write(format_bibitem(entry) + "\n\n")
    
#     print(f"已处理 {len(entries)} 个条目，保存至 {output_file}")

# if __name__ == "__main__":
#     import sys
#     print("\033[1;33mBibTeX 转换工具\033[0m")
#     print("1. 测试单个条目\n2. 处理文件")
    
#     choice = input("请选择模式 (1/2): ")
#     if choice == '1':
#         test_single_entry()
#     elif choice == '2':
#         input_file = input("输入文件路径: ").strip()
#         output_file = input("输出文件路径: ").strip()
#         process_file(input_file, output_file)
#     else:
#         print("\033[91m无效选项\033[0m")
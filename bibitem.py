import re

def format_bibitem(entry):
    """将 BibTeX 条目转换为自定义 \bibitem 格式"""
    # 预处理：移除换行和多余空格，方便正则匹配
    entry_clean = re.sub(r'\s+', ' ', entry.strip())
    
    # 提取字段（优化正则表达式，支持跨行和简单嵌套）
    key_match = re.search(r"@\w+\{([^,]+),", entry_clean)
    title_match = re.search(r"title\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", entry_clean, re.IGNORECASE)
    author_match = re.search(r"author\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", entry_clean, re.IGNORECASE)
    journal_match = re.search(r"(journal|booktitle)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", entry_clean, re.IGNORECASE)
    volume_match = re.search(r"volume\s*=\s*\{([^}]*)\}", entry_clean, re.IGNORECASE)
    pages_match = re.search(r"pages\s*=\s*\{([^}]*)\}", entry_clean, re.IGNORECASE)
    year_match = re.search(r"year\s*=\s*\{([^}]*)\}", entry_clean, re.IGNORECASE)
    doi_match = re.search(r"doi\s*=\s*\{([^}]*)\}", entry_clean, re.IGNORECASE)

    # 获取字段值（带默认值）
    key = key_match.group(1) if key_match else "unknown_key"
    title = title_match.group(1).strip('{}') if title_match else "Unknown Title"
    author = author_match.group(1).strip('{}') if author_match else "Unknown Author"
    journal = journal_match.group(2).strip('{}') if journal_match else "Unknown Journal"
    volume = volume_match.group(1) if volume_match else "Unknown Volume"
    pages = pages_match.group(1) if pages_match else "Unknown Pages"
    year = year_match.group(1) if year_match else "Unknown Year"
    doi = doi_match.group(1) if doi_match else "Unknown DOI"

    # 处理作者格式
    authors = [a.strip() for a in re.split(r"\s+and\s+", author)]
    if len(authors) > 2:
        author_formatted = f"{authors[0]}, {authors[1]}, et al."
        short_cite = f"{authors[0]} et al.({year})"
    else:
        author_formatted = ", ".join(authors)
        short_cite = f"{' & '.join(authors)} ({year})" if len(authors) > 1 else f"{authors[0]} ({year})"

    # 构建格式化条目
    return f"""\\bibitem[{short_cite}]{{{key}}}
  {author_formatted},
  \\textit{{{title}}},
  in: \\textit{{{journal}}}, vol. {volume}, pp. {pages}, {year}.
  doi: {{{doi}}}
"""

def test_single_entry():
    """交互式测试单个条目"""
    print("\n\033[1;36m请输入BibTeX条目（输入空行结束）：\033[0m")
    lines = []
    while True:
        try:
            line = input()
            if not line.strip() and len(lines) > 0:  # 允许空行结束输入
                break
            lines.append(line)
        except EOFError:  # 支持 Ctrl+D 结束输入
            break
    
    entry = "\n".join(lines)
    if not entry.strip():
        print("\033[91m错误：输入为空\033[0m")
        return
    
    try:
        result = format_bibitem(entry)
        print("\n\033[1;32m转换结果：\033[0m")
        print(result)
    except Exception as e:
        print(f"\033[91m转换错误：{str(e)}\033[0m")

def process_file(input_file, output_file):
    """处理整个文件"""
    with open(input_file, "r", encoding="utf-8") as f:
        entries = re.split(r'\n\s*\n', f.read())  # 更健壮的分隔方式
    
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in entries:
            if entry.strip():
                f.write(format_bibitem(entry) + "\n\n")
    
    print(f"已处理 {len(entries)} 个条目，保存至 {output_file}")

if __name__ == "__main__":
    import sys
    print("\033[1;33mBibTeX 转换工具\033[0m")
    print("1. 测试单个条目\n2. 处理文件")
    
    choice = input("请选择模式 (1/2): ")
    if choice == '1':
        test_single_entry()
    elif choice == '2':
        input_file = input("输入文件路径: ").strip()
        output_file = input("输出文件路径: ").strip()
        process_file(input_file, output_file)
    else:
        print("\033[91m无效选项\033[0m")
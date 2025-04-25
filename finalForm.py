import re
import os

def convert_entry(entry):
    """精确转换doi字段并处理标点"""
    # 匹配模式：年份 + 任意标点 + doi声明
    pattern = r"""
        (\b\d{4}\b)          # 年份
        (\.?,?)\s*           # 原有标点（.或,）
        (doi\s*[:=]?\s*{)    # doi声明
        ([^}]+)              # doi值
        (})                  # 闭合括号
    """
    
    # 替换为：年份. , + 标准URL
    replacement = r'\1., \\url{https://doi.org/\4}'
    
    # 执行替换
    converted = re.sub(
        pattern,
        replacement,
        entry,
        flags=re.IGNORECASE | re.VERBOSE
    )
    
    return converted

def process_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = re.split(r'\n\s*\n+', content)
        processed = []
        
        for idx, entry in enumerate(entries, 1):
            if entry.strip():
                print(f"处理条目 {idx}/{len(entries)}")
                processed.append(convert_entry(entry))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(processed))
            
        print(f"\n转换完成！输出文件：{os.path.abspath(output_path)}")
    
    except Exception as e:
        print(f"处理出错：{str(e)}")

# 使用示例（请修改为实际路径）
input_file = "/Users/jiangguanxuan/Downloads/Bibitem-Generator/3.0.txt"
output_file = "/Users/jiangguanxuan/Downloads/Bibitem-Generator/finalForm.txt"

if __name__ == "__main__":
    process_file(input_file, output_file)
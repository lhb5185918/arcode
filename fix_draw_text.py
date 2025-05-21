"""
修复所有draw_text调用中的width参数，确保它是整数
"""
import os
import re
import sys

def fix_draw_text_in_file(file_path):
    """
    修复文件中的draw_text调用
    """
    print(f"处理文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找draw_text调用中的width参数
    pattern = r'arcade\.draw_text\([^)]*width=([^,\)]+)'
    
    # 修复所有匹配
    def replace_width(match):
        width_param = match.group(1).strip()
        # 如果不是简单的整数，则包装在int()中
        if not width_param.isdigit() and not width_param.startswith('int('):
            return match.group(0).replace(f'width={width_param}', f'width=int({width_param})')
        return match.group(0)
    
    modified_content = re.sub(pattern, replace_width, content)
    
    # 如果内容有修改，写回文件
    if content != modified_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"已修复文件: {file_path}")
        return True
    
    return False

def main():
    """
    主函数
    """
    fixed_count = 0
    
    # 获取当前目录下所有.py文件
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_draw_text_in_file(file_path):
                    fixed_count += 1
    
    print(f"共修复了 {fixed_count} 个文件中的draw_text调用")

if __name__ == "__main__":
    main() 
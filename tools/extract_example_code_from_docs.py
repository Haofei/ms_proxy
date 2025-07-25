import os
import re
import sys

def extract_cpp_code(md_path, cpp_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'## Example\r?\n\r?\n```cpp\r?\n(.*?)\r?\n```'
    code_blocks = re.findall(pattern, content, re.DOTALL)

    if len(code_blocks) == 0:
        return  # No match, skip
    elif len(code_blocks) > 1:
        raise ValueError(f"File '{md_path}' contains more than one '## Example' C++ code block.")

    cpp_code = code_blocks[0]
    header = f"// This file was auto-generated from:\n// {md_path}\n\n"

    with open(cpp_path, 'w', encoding='utf-8') as out:
        out.write(header)
        out.write(cpp_code)

def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_example_code_from_docs.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.md'):
                md_path = os.path.join(root, file)
                rel_path = os.path.relpath(md_path, input_dir)
                rel_base = os.path.splitext(rel_path)[0].replace(os.sep, '_')
                cpp_path = os.path.join(output_dir, f"example_{rel_base}.cpp")
                extract_cpp_code(md_path, cpp_path)

if __name__ == '__main__':
    main()

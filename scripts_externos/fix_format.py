import re

def fix_formatting(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'},\n\s+,\n\s+\.category = ', '},\n        .category = ', content)
    
    content = re.sub(r'(\.flags = [^,]+),\n\s+,\n\s+(\.category = [^,]+),', r'\1,\n        \2,', content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("fixed")

if __name__ == '__main__':
    fix_formatting('src/data/battle_moves.h')

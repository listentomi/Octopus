with open('../clause2subquestion/spider/train_src.txt', 'r') as f:
    src_lines = f.readlines()
with open('../clause2subquestion/spider/train_tgt.txt', 'r') as f:
    tgt_lines = f.readlines()

Translation_examples = []

for src,tgt in zip(src_lines,tgt_lines):
    parts = src.split('|')
    _src = parts[-1].strip()
    _tgt = tgt.strip()
    Translation_examples.append((_src,_tgt))

with open('Translation_examples.txt', 'w') as file:
    # 将每一对元组写入文件
    for item in Translation_examples:
        file.write(f"{item[0]}|{item[1]}\n")
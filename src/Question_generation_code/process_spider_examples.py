with open('dev.sql', 'r') as f:
    spider = f.readlines()

spider_examples = []
for i in range(0, len(spider), 3):
    # 读取当前索引及后两个索引处的元素
    question = spider[i]
    sql = spider[i+1]
    spider_examples.append({ question, sql})

with open('spider_examples.txt', 'w') as f:
    # 写入内容到文件
    for item in spider_examples:
        f.write(f"{item}\n")
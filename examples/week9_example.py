import os

# Week 9 example: 파일 입출력
fn = 'examples_week9.txt'
with open(fn,'w',encoding='utf-8') as f:
    f.write('line1\nline2\n')

with open(fn,'r',encoding='utf-8') as f:
    lines = f.readlines()
    print(len(lines))

with open(fn,'a',encoding='utf-8') as f:
    f.write('line3\n')

os.remove(fn)  # cleanup

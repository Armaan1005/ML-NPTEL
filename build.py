"""Build index.html from data/template.html + data/questions.json + data/hints.txt."""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
p = lambda *a: os.path.join(ROOT, *a)

def esc(s):
    return s.strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

data = json.load(open(p('data', 'questions.json'), encoding='utf-8'))
hints = {}
for line in open(p('data', 'hints.txt'), encoding='utf-8').read().strip().splitlines():
    qid, hint, why = line.split(' || ')
    hints[qid.strip()] = (esc(hint), esc(why))

for si, s in enumerate(data):
    for qi, q in enumerate(s['qs']):
        q['h'], q['e'] = hints[f'{si}-{qi}']

blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<' + chr(92) + '/')
page = open(p('data', 'template.html'), encoding='utf-8').read().replace('/*__DATA__*/null', blob)
open(p('index.html'), 'w', encoding='utf-8').write(page)
print('Built index.html')

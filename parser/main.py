from nltk import load_parser
from checker import spellings

cp = load_parser('sql2.fcfg')
# query = input('what\'s your query?')
query = 'What illiterates in rohtak'
# query = spellings(query
trees = list(cp.parse(query.split()))
print(trees)
answer = trees[0].label()['SEM']
answer = [s for s in answer if s]
q = ' '.join(answer)
print(q)
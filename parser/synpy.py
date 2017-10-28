import nltk
import json

indexfile = open('indexes.txt', 'r')
json_output = indexfile.read()
json_output = json.loads(json_output)

indexes = json_output['indexes']
all_columns = json_output['all_columns']

remove_attrs = ['state', 'district']

rules = []


def attribute_name_parser(attr, created_indexes={}, removed_attrs=[], replace=True):
    attr = attr.replace('-', ' ')
    attr = attr.replace('/', ' ')
    if len(attr) > 64:
        # [sys.stdout.write(str(x)) for x in attr]
        attr_splited = filter(lambda x: len(x) > 0, attr.split(' '))
        attr_splited = [i[0].upper() for i in attr_splited]
        index = "".join(attr_splited)
        if replace:
            if index not in created_indexes:
                created_indexes[index] = 1
            else:
                created_indexes[index] += 1
        index = index + str(created_indexes[index])
        if replace:
            print('{0} => {1}'.format(index, attr))
        attr = index
    else:
        attr = attr.replace(" ", "_").replace('-', '_').replace('___', '_').replace('.', '').replace('/_', '/')
        attr = attr.lower()
    for j in removed_attrs:
        if j in attr:
            attr = j.join(attr.split(j)[1:])
    attr = attr.strip('_')
    return attr, created_indexes

for i in indexes:
    val = i['val']
    column = i['column']
    column,_ = attribute_name_parser(column)
    if not isinstance(val, int):
        mod_val = val.lower()
        for j in remove_attrs:
            if j in mod_val:
                mod_val = mod_val.split(j)[1]
                mod_val = mod_val.strip()
                mod_val = mod_val.strip('-')
                mod_val = mod_val.strip()
        print(mod_val)
        query = 'NP[SEM=\'{2} = "{0}"\'] -> \'{1}\''.format(val, mod_val, column)
        if query not in rules:
            rules.append(query)

rulefile = open('sql2.fcfg', 'w')
rulestxt = '''
% start S

S[SEM=(?np + WHERE + ?vp)] -> NP[SEM=?np] VP[SEM=?vp]

VP[SEM=(?v + ?pp)] -> IV[SEM=?v] PP[SEM=?pp]
VP[SEM=(?v + ?ap)] -> IV[SEM=?v] AP[SEM=?ap]
VP[SEM=(?v + ?np)] -> TV[SEM=?v] NP[SEM=?np]
VP[SEM=(?vp1 + ?c + ?vp2)] -> VP[SEM=?vp1] Conj[SEM=?c] VP[SEM=?vp2]

NP[SEM=(?det + ?n)] -> Det[SEM=?det] N[SEM=?n]
NP[SEM=(?n + ?pp)]  -> N[SEM=?n] PP[SEM=?pp]
NP[SEM=?n]  -> N[SEM=?n]  | CardN[SEM=?n]


PP[SEM=(?p + ?np)] -> P[SEM=?p] NP[SEM=?np]
AP[SEM=?pp] -> A[SEM=?a] PP[SEM=?pp]

Det[SEM='SELECT'] -> 'Which' | 'What'
Conj[SEM='AND'] -> 'and'


IV[SEM=''] -> 'are'
TV[SEM=''] -> 'have'
A -> 'located'
P[SEM=''] -> 'in'
P[SEM='>'] -> 'above'

'''

TABLENAME = 'education'

for i in all_columns:
    changed_column_name,_ = attribute_name_parser(i)
    rules.append('N[SEM=\'{0} FROM {1}\'] -> \'{2}\''.format(changed_column_name, TABLENAME, i))

rules.append('N[SEM=\'{0}\'] -> \'{0}\''.format(TABLENAME))

rulestxt = rulestxt + "\n".join(rules)
rulefile.write(rulestxt)
rulefile.close()
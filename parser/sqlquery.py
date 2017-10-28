import json

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

indexfile = open('indexes.txt', 'r')
indexfile = indexfile.read()
data = json.loads(indexfile)

columns = data['all_columns']
indexes = data['indexes']

query = 'literate - persons in state - andhra pradesh'

query = query.lower()

sqlquery = ''

whereclauses = []

for i in indexes:
    val = i['val']
    column = i['column']
    if not isinstance(val, int):
        # print(val)
        if val.lower() in query:
            mod_col, _ = attribute_name_parser(column)
            if (mod_col, val) not in whereclauses:
                whereclauses.append((mod_col, val))

attrs = []
print(columns)
for i in columns:
    # print(i)
    if i.lower() in query.lower():
        i,_ = attribute_name_parser(i)
        if i not in attrs:
            attrs.append(i)

print(attrs)
TABLENAME = 'education'
sqlquery = 'SELECT {0} FROM {1}'.format(",".join(attrs),TABLENAME)
print(sqlquery)
for i in whereclauses:
    print("WHERE {0} = {1}".format(i[0],i[1]))
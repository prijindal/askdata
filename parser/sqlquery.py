import json
import os
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

def get_sqlquery(query):
    PATH = os.path.dirname(os.path.realpath(__file__))
    indexfile = open(PATH + '/indexes.txt', 'r')
    indexfile = indexfile.read()
    data = json.loads(indexfile)

    columns = data['all_columns']
    indexes = data['indexes']

    query = query.lower()

    sqlquery = ''

    whereclauses = []

    major_col = None
    for i in indexes:
        val = i['val']
        column = i['column']
        if not isinstance(val, int):
            # print(val)
            if val.lower() in query:
                mod_col, _ = attribute_name_parser(column)
                if (mod_col, val) not in whereclauses:
                    if major_col is None:
                        major_col = mod_col
                    whereclauses.append((mod_col, val))
 
    if major_col is None:
        major_col = 'total__rural__urban'

    attrs = []
    print(columns)
    for i in columns:
        # print(i)
        if i.lower() in query.lower():
            i,_ = attribute_name_parser(i)
            if i not in attrs:
                attrs.append(i)

    if 'age_group' not in attrs:
        whereclauses.append(('age_group', 'All ages'))
    # if 'total__rural__urban' not in attrs:
    #     attrs.append('total__rural__urban')
    if 'rate' in query:
        attrs.append('year')
    # whereclauses.append(('total__rural__urban', 'Total'))
    print(attrs)
    TABLENAME = 'education'
    # sqlquery = 'SELECT {0}, {1} FROM {2}'.format(major_col, ",".join(attrs),TABLENAME)
    if 'rate' in query:
        sqlquery = 'SELECT year, (literate_persons/total_persons)*100 as literacy_rate FROM {0}'.format(TABLENAME)
    else:
        sqlquery = 'SELECT {1}, (literate_persons/total_persons)*100 as literacy_rate FROM {2}'.format(attrs[0], ",".join(attrs),TABLENAME)
    if len(whereclauses) > 0:
        sqlquery = sqlquery + " WHERE "
        sqlquery = sqlquery + " AND ".join(["{0} = '{1}'".format(i[0],i[1]) for i in whereclauses])
    if len(attrs) > 0:
        sqlquery = sqlquery + " GROUP BY {0}".format(attrs[0])
    print(sqlquery)
    return sqlquery

if __name__ == '__main__':
    get_sqlquery('literate - persons in state - andhra pradesh')

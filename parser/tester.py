import pandas as pd
import os

indexes = []

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

file_names = os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/data/")
all_columns = []
for name in file_names:
    if "INDIA" not in name:
        continue;
    try:
        name = os.path.dirname(os.path.realpath(__file__)) + "/data/" + name
        df = pd.read_excel(name)
        len_col = len(df.index)
        ret_val=""
        for w in df.columns:
            if w not in all_columns:
                all_columns.append(w)
            if (df[w].dtype== "object"):
                col_vals = df[w]
                for val in col_vals:
                    #val,_ = attribute_name_parser(w)
                    if val not in indexes:
                        indexes.append({
                            'val': val,
                            'column': w,
                            'tablename': name
                        })
        #df.clear()
    except Exception:
        continue

index_file = open('indexes.txt', 'w')

import json

json_output = {
    'indexes': indexes,
    'all_columns': all_columns
}

index_file.write(json.dumps(json_output))
index_file.close()







import csv
import sys
import MySQLdb

def readcsv():
    with open('sample.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        rows = list(spamreader)
        return rows

def connect():
    connection = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "root",
                                db = "askdata")
    return connection

def disconnect(connection):
    return connection.close()

def attribute_name_parser(attr, created_indexes, replace=True):
    if len(attr) > 64:
        # [sys.stdout.write(str(x)) for x in attr]
        caps = filter(lambda x: x.isupper(), list(attr))
        index = "".join(caps)
        if replace:
            if index not in created_indexes:
                created_indexes[index] = 1
            else:
                created_indexes[index] += 1
        index = index + str(created_indexes[index])
        # if replace:
            # print('{0} => {1}'.format(index, attr))
        attr = index
    else:
        attr = attr.replace(" ", "_").lower().replace('-','_').replace('___','_').replace('.','').replace('/_','/')
    return attr, created_indexes

def find_attr_type(attr, data):
    is_alpha = [any([j.isalpha() for j in i]) for i in data]
    if any(is_alpha):
        return 'VARCHAR({0})'.format(max([len(i) for i in data]))
    else:
        ## bit or int or float
        minimum = float(min(data))
        maximum = float(max(data))
        is_float = [isinstance(i, float) for i in data]
        if any(is_float):
            return 'DOUBLE'
        data = [int(i) for i in data]
        minimum = float(min(data))
        maximum = float(max(data))
        # print(attr)
        # print(data)
        # print(minimum)
        # print(maximum)
        if maximum <= 127 and minimum >= -128:
            return 'TINYINT'
        if minimum >= 0:
            if maximum <= 255:
                return 'TINYINT UNSIGNED'
            if maximum <= 65535:
                return 'SMALLINT UNSIGNED'
            elif maximum <=  4294967295:
                return 'INT UNSIGNED'
            elif maximum <= 18446744073709551615:
                return 'BIGINT UNSIGNED'
        else:
            if maximum <= 127 and minimum >= -128:
                return 'TINYINT'
            if maximum <= 32767 and minimum >= -32768:
                return 'SMALLINT'
            elif maximum <= 2147483647 and minimum >= - 2147483648:
                return 'INT'
            elif maximum <= 9223372036854775807 and minimum >= -9223372036854775808:
                return 'BIGINT'
        return 'DOUBLE'

def create_table_command(tablename, rows):
    tablename = tablename.lower()
    header = rows[0]
    columns = {}
    created_indexes = {}
    for i in range(len(header)):
        data = [row[i] for row in rows[1:]]
        attr = header[i]
        attr, created_indexes = attribute_name_parser(attr, created_indexes)      
        datatype = find_attr_type(attr, data)
        # print(datatype)
        columns[attr] = {
            'data': data,
            'type': datatype
        }
    column_query = ['`{0}` {1}'.format(attr, columns[attr]['type']) for attr in columns]
    column_query = ',\n'.join(column_query)
    command = '''
        DROP TABLE IF EXISTS {0};
        CREATE TABLE {0} (
            {1}
        );
    '''.format(tablename, column_query)

    columns_list = ['`{0}`'.format(attr) for attr in columns]
    columns_list = ",".join(columns_list)

    insert_command = '''
        INSERT INTO {0} ({1})
        VALUES'''.format(tablename, columns_list)
    subcommands = []
    for row in rows[1:]:
        formatted_values = []
        for j in range(len(row)):
            val = row[j]
            attr = rows[0][j]
            attr, created_indexes = attribute_name_parser(attr, created_indexes, False)
            datatype = columns[attr]['type']
            if "VARCHAR" in datatype :
                val = '"{0}"'.format(val)
            formatted_values.append(val)
        subcommand = '({0})'.format(",".join(formatted_values))
        subcommands.append(subcommand)
    insert_command = insert_command + ',\n'.join(subcommands)
    insert_command = insert_command + ';'
    return command, insert_command

def main():
    rows = readcsv()
    connection = connect()
    create_command, insert_command = create_table_command("LANGUAGE", rows)
    print(create_command)
    with connection.cursor() as cr:
        cr.execute(create_command)
        cr.execute(insert_command)
        connection.commit()

    disconnect(connection)

if __name__ == '__main__':
    main()

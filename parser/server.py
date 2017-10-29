import MySQLdb
from decimal import Decimal
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect():
    connection = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "root",
                                db = "askdata")
    return connection

def disconnect(connection):
    return connection.close()

@app.route("/", methods=["POST"])
def hello():
    content = request.json
    connection = connect()
    cursor = connection.cursor()
    cursor.execute (content['SQL'])
    output = []
    field_names = [i[0] for i in cursor.description]
    print(field_names)
    for row in cursor:
        row_data = []
        for data in row:
            if type(data) is Decimal:
                row_data.append(float(data))
            else:
                row_data.append(str(data))
        output.append(row_data)
    result = {
        'data': output,
        'field_names': field_names
    }
    cursor.close()
    connection.close()
    return jsonify(result)

def main():
    app.run()

if __name__ == '__main__':
    main()

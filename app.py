from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_stuedent():

    connection = sqlite3.connect("db_univ7.db")
    cursor = connection.cursor()
    with connection:
        cursor.execute("select * from student")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    students = []
    for row in rows:
        student = {
            "ID" : row[0],
            "Name" : row[1],
            "Dept_Name" : row[2],
            "Tot_Cred" : row[3]
        }
        students.append(student)
    return students

@app.route('/students', methods = ['GET'])
def get_all_students():
    students = get_stuedent()
    return jsonify(students)

if __name__ == "__main__":
    app.run(debug=True, port=5045)
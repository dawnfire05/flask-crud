from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Helper function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('db_univ7.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database (run this once to set up the table)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route to create a new student (C - Create)
@app.route('/students', methods=['POST'])
def create_student():
    new_student = request.json
    name = new_student['name']
    age = new_student['age']
    grade = new_student['grade']

    conn = get_db_connection()
    conn.execute('INSERT INTO student (name, age, grade) VALUES (?, ?, ?)',
                 (name, age, grade))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student created!'}), 201

# Route to get all students (R - Read)
@app.route('/students', methods=['GET'])
def get_all_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM student').fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])

# Route to get a student by ID (R - Read)
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM student WHERE id = ?', (id,)).fetchone()
    conn.close()

    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify(dict(student))

# Route to update a student (U - Update)
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    updated_student = request.json
    name = updated_student['name']
    age = updated_student['age']
    grade = updated_student['grade']

    conn = get_db_connection()
    conn.execute('''
        UPDATE student SET name = ?, age = ?, grade = ? WHERE id = ?
    ''', (name, age, grade, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student updated!'})

# Route to delete a student (D - Delete)
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM student WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student deleted!'})

if __name__ == '__main__':
    init_db()  # Initialize the database with the student table
    app.run(debug=True)
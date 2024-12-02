from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            register_no TEXT NOT NULL,
            contact_no TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    registrations = conn.execute('SELECT * FROM registrations').fetchall()
    conn.close()
    return render_template('index.html', registrations=registrations)

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    register_no = request.form['register_no']
    contact_no = request.form['contact_no']
    department = request.form['department']
    year = request.form['year']
    status = request.form['status']

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO registrations (name, register_no, contact_no, department, year, status) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, register_no, contact_no, department, year, status))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:reg_id>', methods=['POST'])
def delete(reg_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM registrations WHERE id = ?', (reg_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('members.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        register_no TEXT NOT NULL,
                        contact_no TEXT NOT NULL,
                        department TEXT NOT NULL,
                        year TEXT NOT NULL,
                        status TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('members.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'add' in request.form:  # Add entry
            name = request.form['name']
            register_no = request.form['register_no']
            contact_no = request.form['contact_no']
            department = request.form['department']
            year = request.form['year']
            status = request.form['status']
            cursor.execute("INSERT INTO members (name, register_no, contact_no, department, year, status) VALUES (?, ?, ?, ?, ?, ?)",
                           (name, register_no, contact_no, department, year, status))
        elif 'update' in request.form:  # Update entry
            member_id = request.form['member_id']
            name = request.form['name']
            register_no = request.form['register_no']
            contact_no = request.form['contact_no']
            department = request.form['department']
            year = request.form['year']
            status = request.form['status']
            cursor.execute("UPDATE members SET name = ?, register_no = ?, contact_no = ?, department = ?, year = ?, status = ? WHERE id = ?",
                           (name, register_no, contact_no, department, year, status, member_id))
        elif 'delete' in request.form:  # Delete entry
            member_id = request.form['member_id']
            cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))

        conn.commit()

    # Retrieve all members
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()

    return render_template('index.html', members=members)

if __name__ == '__main__':
    app.run(debug=True)

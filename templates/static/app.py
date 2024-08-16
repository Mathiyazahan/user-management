from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flashing messages

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="mysql-db",
        user="dbuser",
        password="your-password",
        database="mysqldb"
    )

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return render_template('user_info.html', user=user)
        else:
            flash('User not found!')
            return redirect(url_for('add_user', username=username))
    
    return render_template('index.html')

@app.route('/add_user/<username>', methods=['GET', 'POST'])
def add_user(username):
    if request.method == 'POST':
        new_username = request.form['username']
        address = request.form['address']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, address) VALUES (%s, %s)", (new_username, address))
            conn.commit()
            flash('User added successfully!')
            return redirect(url_for('home'))
        except mysql.connector.IntegrityError:
            flash('User already exists!')
            return render_template('add_user.html', username=username)
        finally:
            cursor.close()
            conn.close()

    return render_template('add_user.html', username=username)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'shri#123'
# Configure MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='MySQL#123',
    database='hospital_db'
)

# Create a cursor object using cursor() method
cursor = db.cursor()

def validate_email(email):
    # Simple email validation using regular expression
    pattern = r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
    return re.match(pattern, email)

def validate_phone(phone):
    # Simple phone number validation
    pattern = r"^[0-9]{10}$"
    return re.match(pattern, phone)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['uname']
        email = request.form['email']
        password = request.form['psw']

        # Validation
        if not (name and email and password):
            return "Please fill in all required fields."

        if not validate_email(email):
            return "Invalid email format."

        if len(password) < 8:
            return "Password must be at least 8 characters long."

        hashed_password = generate_password_hash(password)

        # Inserting data into the database
        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, hashed_password)
        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('psw')

        # Validation
        if not (email and password):
            return "Please fill in all required fields."

        if not validate_email(email):
            return "Invalid email format."


        # Fetch user from the database
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))

        return "Invalid email or password."

    return render_template('login.html')

@app.route('/', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/appointmentForm', methods=['GET'])
def appointmentForm():

    return render_template('appointmentForm.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        department = request.form['department']
        date_time = request.form['date_time']
        reason = request.form['reason']
        comments = request.form['comments']

        # Validation
        if not (name and email and phone and address and department and date_time):
            return "Please fill in all required fields."

        if not validate_email(email):
            return "Invalid email format."

        if not validate_phone(phone):
            return "Invalid phone number format."

        # Inserting data into the database
        sql = "INSERT INTO appointments (name, email, phone, address, department, date_time, reason, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, email, phone, address, department, date_time, reason, comments)
        cursor.execute(sql, values)
        db.commit()

        # Fetch the last inserted appointment ID
        cursor.execute(
            "SELECT id, name, email, phone, address, department, date_time, reason, comments FROM appointments ORDER BY id DESC LIMIT 1")
        appointment_details = cursor.fetchone()

        return render_template('confirmation.html', appointment_details=appointment_details)

# Route to display update form for a specific appointment
@app.route('/update/<int:appointment_id>', methods=['GET'])
def update(appointment_id):
    cursor.execute("SELECT * FROM appointments WHERE id = %s", (appointment_id,))
    appointment = cursor.fetchone()
    return render_template('update.html', appointment=appointment)

# Route to handle update form submission
@app.route('/update/<int:appointment_id>', methods=['POST'])
def update_submit(appointment_id):
    # Get updated information from the form
    updated_name = request.form['name']
    updated_email = request.form['email']
    # ... (get other updated fields)

    # Update information in the database
    update_query = "UPDATE appointments SET name = %s, email = %s WHERE id = %s"
    update_values = (updated_name, updated_email, appointment_id)
    cursor.execute(update_query, update_values)
    db.commit()

    return redirect(url_for('update'))  # Redirect to the main page after updating

# Route to confirm and delete appointments
@app.route('/delete/<int:appointment_id>', methods=['GET'])
def delete(appointment_id):
    cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
    db.commit()
    return redirect(url_for('delete'))  # Redirect to the main page after deletion

@app.route('/show', methods=['GET'])
def show():
    cursor.execute("SELECT * FROM appointments")
    records = cursor.fetchall()
    return render_template('show.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)

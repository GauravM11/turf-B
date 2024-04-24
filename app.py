from flask import Flask, request, render_template, redirect
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

# Set up a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gaurav@11",
    database="assignment_db"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pay')
def pay():
    username = request.args.get('username')
    # You can add payment processing logic here if needed
    return render_template('pay.html', username=username)

@app.route('/process', methods=['POST'])
def process():
    try:
        username = request.form['username']
        location = request.form['location']
        num_requests = int(request.form['num_requests'])
        cost_in_rupees = float(request.form['cost_in_rupees'])

        # Update the cost-to-time mapping for the new locations
        if cost_in_rupees == 500:
            allocation_time = timedelta(minutes=30)
        elif cost_in_rupees == 1000:
            allocation_time = timedelta(minutes=60)
        # Add more conditions for other cost values and locations
        elif cost_in_rupees == 1500:
            allocation_time = timedelta(minutes=90)
        elif cost_in_rupees == 2000:
            allocation_time = timedelta(minutes=120)

        # Check if the username is already in the database
        cursor.execute("SELECT COUNT(*) FROM assignments WHERE request_id = %s", (username,))
        user_count = cursor.fetchone()[0]

        # Get the selected gender (male or female)
        selected_gender = request.form['gender']

        # Calculate the cost with a 10% discount if the username is repeating
        if user_count > 0:
            cost_with_discount = cost_in_rupees - (0.10 * cost_in_rupees)
        else:
            cost_with_discount = cost_in_rupees

        # Apply an additional 15% discount for females
        if selected_gender == 'female':
            cost_with_discount -= (0.15 * cost_in_rupees)

        # Determine the number of slots based on the location
        if location in ['location1', 'location2']:
            num_slots = 2
        else:
            num_slots = 3  # For location3, location4, location5

        # Create a cost matrix with the calculated cost
        cost_matrix = [[cost_with_discount] * num_slots for _ in range(num_requests)]

        row_indices = list(range(num_requests))
        col_indices = list(range(num_slots))

        # Initialize the assignments list
        assignments = []

        # Populate the assignments list
        for row, col in zip(row_indices, col_indices):
            assignments.append({
                "request": row + 1,
                "slot": num_slots,
                "cost": cost_matrix[row][col],
                "location": location,
                "time": allocation_time.total_seconds() / 60
            })

        # ...

        return render_template('result.html', username=username, selected_slot=num_slots, assignments=assignments)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

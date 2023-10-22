from flask import Flask, render_template, request,send_from_directory, redirect, url_for
from bson.objectid import ObjectId
from datetime import datetime
from db import get_tasks_collection

app = Flask(__name__, static_folder='public')


# Connect to db.py
tasks_collection = get_tasks_collection()


@app.route('/')
def home():
    # Default sorting criteria
    sort_by = "due_date"
    sort_order = 1
    if 'sort-by' in request.args:
        if request.args['sort-by'] == 'priority':
            sort_by = 'priority'
    if 'sort-order' in request.args and request.args['sort-order'] == 'desc':
        sort_order = -1

    tasks = tasks_collection.find().sort(sort_by, sort_order)

    return render_template('home.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        pinned = True if request.form['pinned'] == 'true' else False
        tags = request.form['tags'].split(",")
        progress = request.form['progress']

        # Convert due_date from string to datetime object
        due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')

        try:
            tasks_collection.insert_one({
                'title': title,
                'description': description,
                'priority': int(priority),
                'due_date': due_date_obj,
                'pinned': pinned,
                'tags': tags,
                'progress': progress
            })
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Error adding task.", 500

        return redirect(url_for('home'))

    return render_template('add_task.html')

@app.route('/acc_register', methods=['GET', 'POST'])
def acc_register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        try:
            result = insert_user(username, password, email)
            
            if result:
                #registration success
                return "Account registered successfully!"
            else:
                #error during registration
                return "Error registering account.", 500

        except Exception as e:
            print(f"An error occurred: {e}")
            return "Error inputing account information.", 500

        
        return redirect(url_for('home'))

   
    return render_template('acc_register.html')


@app.route('/public/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

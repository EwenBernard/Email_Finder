from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db', 'pythonsqlite.db')

templates_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'views', 'templates')
print(templates_folder_path)
app.config['TEMPLATE_FOLDER'] = templates_folder_path
app.template_folder = app.config['TEMPLATE_FOLDER']

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    reconstructed_email = db.Column(db.String(120))
    company_name = db.Column(db.String(120))
    company_domain = db.Column(db.String(120))

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


#Need to add company name and company domain
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    last_name = request.form['last_name']
    reconstructed_email = request.form['reconstructed_email']
    new_user = User(name=name, last_name=last_name, reconstructed_email=reconstructed_email)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

#Need to add company name and company domain
@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    user.name = request.form['name']
    user.last_name = request.form['last_name']
    user.reconstructed_email = request.form['reconstructed_email']
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

#Need to add company name and company domain
def print_database():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Last Name: {user.last_name}, Email: {user.reconstructed_email}")
    return "Check the console for printed database content"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #new_user = User(name="Jean", last_name="paul", reconstructed_email="jean.paul@domain.fr")
        #db.session.add(new_user)
        #db.session.commit()
        print("PRINT DATABASE")
        print_database()
        app.run(debug=True)

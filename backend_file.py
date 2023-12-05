from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pythonsqlite.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    reconstructed_email = db.Column(db.String(120))

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    last_name = request.form['last_name']
    reconstructed_email = request.form['reconstructed_email']
    new_user = User(name=name, last_name=last_name, reconstructed_email=reconstructed_email)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

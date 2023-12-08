from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from retrieve_domain import get_email_from_hunter
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
    company_name = db.Column(db.String(120))


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        company_name = request.form['company_name']

        # Utilisez la nouvelle fonction pour obtenir l'e-mail
        reconstructed_email = get_email_from_hunter(name, last_name, company_name)

        new_user = User(name=name, last_name=last_name, reconstructed_email=reconstructed_email, company_name=company_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('add_user.html')  # Créez un template HTML pour le formulaire d'ajout


@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    
    # Mettez à jour uniquement les champs non vides fournis dans la requête
    if 'name' in request.form:
        user.name = request.form['name']
    if 'last_name' in request.form:
        user.last_name = request.form['last_name']
    if 'company_name' in request.form:
        user.company_name = request.form['company_name']

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
        print("PRINT DATABASE")
        app.run(debug=True)



























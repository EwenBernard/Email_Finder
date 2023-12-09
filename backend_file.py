from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from retrieve_domain import get_email_from_hunter, match_user_input

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

        # Utilisez la nouvelle fonction pour obtenir l'e-mail et le reste des données
        hunter_data = get_email_from_hunter(name, last_name, company_name)
        matched_result, remaining_data = match_user_input(f"{name} {last_name}", hunter_data)

        if matched_result:
            new_user = User(name=matched_result['name'],
                            last_name=matched_result['last_name'],
                            reconstructed_email=matched_result['email'],
                            company_name=matched_result['company'])
            db.session.add(new_user)
            db.session.commit()

        return redirect('/')

    return render_template('add_user.html')

@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    
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
        print("Executing")
        app.run(debug=True)

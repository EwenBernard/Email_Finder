from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from retrieve_domain import get_email_from_hunter, match_user_input
import os

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pythonsqlite.db'

app = Flask(__name__, static_folder='../views/static', template_folder='../views/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db', 'pythonsqlite.db')

"""
templates_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'views', 'templates')
print(templates_folder_path)
app.config['TEMPLATE_FOLDER'] = templates_folder_path
app.template_folder = app.config['TEMPLATE_FOLDER']
"""

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    reconstructed_email = db.Column(db.String(120))
    company_name = db.Column(db.String(120))
    source_1 = db.Column(db.String(500))
    confidence = db.Column(db.Integer())
    best_match = db.Column(db.Integer())


    __tablename__ = 'email_contact_table'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_user():
    print(request.form)

    name = request.form['name']
    last_name = request.form['last_name']
    company_name = request.form['company_name']
    
    # Utilisez la nouvelle fonction pour obtenir l'e-mail et le reste des données
    hunter_data = get_email_from_hunter(name, last_name, company_name)
    matched_result, remaining_data = match_user_input(name, last_name, hunter_data)
    
    if matched_result and matched_result['name'] and matched_result['last_name']:
        new_user = User(name=matched_result['name'],
                        last_name=matched_result['last_name'],
                        reconstructed_email=matched_result['email'],
                        company_name=matched_result['company'],
                        source_1=matched_result['source'],
                        confidence=matched_result['confidence'],
                        best_match=1)
        db.session.add(new_user)
        db.session.commit()
    if remaining_data:
        for user in remaining_data:
            if user['name'] and user['last_name']:
                new_user = User(name=user['name'],
                            last_name=user['last_name'],
                            reconstructed_email=user['email'],
                            company_name=user['company'],
                            source_1=user['source'],
                            confidence=user['confidence'],
                            best_match=0)
                db.session.add(new_user)
                db.session.commit()
    
    new_user = User(name=request.form['name'],
                    last_name=request.form['last_name'],
                    reconstructed_email="test@gmail.com",
                    company_name=request.form['company_name'])
    db.session.add(new_user)
    db.session.commit()
    
    response_data = {
    'matched_result': matched_result,
    'remaining_data': remaining_data
    }
    """
    fake_data = {
        'matched_result': {
            'name': 'Jean',
            'last_name': 'Soma',
            'email': 'jean.soma@example.com',
            'company': 'efrei.fr',
            'sources': "mcdo.com",
            'confidence': 92,
            'best_match': 1,
        },
        'remaining_data': [
            {
                'name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@example.com',
                'company': 'XYZ Ltd',
                'sources': 'Source 2',
                'confidence': 85,
                'best_match': 0,
            },
            {
                'name': 'Bob',
                'last_name': 'Johnson',
                'email': 'bob.johnson@example.com',
                'company': '123 Corp',
                'sources': 'Source 3',
                'confidence': 90,
                'best_match': 0,
            }]}
    
    empty_data = {
        'matched_result' : [],
        'remaining_data': [
            {
                'name': 'Jane',
                'last_name': 'Smith',
                'reconstructed_email': 'jane.smith@example.com',
                'company_name': 'XYZ Ltd',
                'sources': ['Source 2'],
                'confidence': 85,
                'best_match': 0,
            },
            {
                'name': 'Bob',
                'last_name': 'Johnson',
                'reconstructed_email': 'bob.johnson@example.com',
                'company_name': '123 Corp',
                'sources': ['Source 3'],
                'confidence': 90,
                'best_match': 0,
            }
        ]
    }
    """
    return jsonify(response_data)


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
        app.run(debug=True,host='0.0.0.0', port=8001)


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Integer, nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = generate_password_hash(data['password'])
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful!', 'user_id': user.id}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/portfolio', methods=['POST'])
def add_to_portfolio():
    data = request.json
    new_stock = Portfolio(user_id=data['user_id'], stock_symbol=data['stock_symbol'], shares=data['shares'])
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({'message': 'Stock added to portfolio!'}), 201

@app.route('/portfolio/<int:user_id>', methods=['GET'])
def get_portfolio(user_id):
    portfolio = Portfolio.query.filter_by(user_id=user_id).all()
    return jsonify([{'stock_symbol': stock.stock_symbol, 'shares': stock.shares} for stock in portfolio]), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

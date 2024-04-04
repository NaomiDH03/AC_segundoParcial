from flask import Flask, request, jsonify, abort  
from flask_sqlalchemy import SQLAlchemy  
from dotenv import load_dotenv 
import os
from datetime import datetime
from flask import render_template

load_dotenv()  

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class Videogames(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(80), nullable=False)  
    developer = db.Column(db.String(80), nullable=False)
    platform = db.Column(db.String(80), nullable=False)
    rating_board = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Boolean, default=False) 
    #imagen = db.Column(db.String(200)) 
    

    def llenar(self):  
        return {
            'id': self.id,
            'name': self.name,
            'developer': self.developer,
            'platform': self.platform,
            'rating_board': self.rating_board,
            'category': self.category,
            'status': self.status
            #'imagen': self.imagen
        }
        
@app.route('/')  
def index():
    return 'Bienvenido a los videojuegos' 

#CRUD

#Esto es para traer absolutamente todas las tareas GET
@app.route('/tasks', methods=['GET']) 
def get_tasks():
    tasks = Videogames.query.all() 
    return jsonify([task.llenar() for task in tasks])

#Esto es para hacer un post, o sea, crear un nuevo videojuego
@app.route('/create_task', methods=['POST'])  
def create_task():
    if not request.json or not 'name' in request.json:
        abort(400) 
    task = Videogames(
        name=request.json['name'],
        developer=request.json.get('developer', ''),
        platform=request.json.get('platform', ''),
        rating_board=request.json.get('rating_board', ''),
        category=request.json.get('category', ''),
        status=request.json.get('status', False)
    )
    db.session.add(task) 
    db.session.commit()  
    return jsonify(task.llenar()), 201 

#Esto es para actualizar algún campo, en este caso es el nombre
app.route('/tasks_update/<int:task_id>', methods=['PUT'])  
def update_task(task_id):
    task = Videogames.query.get(task_id)
    if task is None:
        abort(404)  
    if not request.json:
        abort(400) 
    name = request.json.get('name') 
    if name is not None:
        task.name = name  
    db.session.commit() 
    return jsonify(task.llenar()) 

#Esto es para borrar un videojuego de acuerdo a su ID
@app.route('/tasks_delete/<int:task_id>', methods=['DELETE'])  
def delete_task(task_id):
    task = Videogames.query.get(task_id)  
    if task is None: 
        abort(404)
    db.session.delete(task)  
    db.session.commit()  
    return jsonify({'status': True}), 201 

#Para filtrar por categoria y si quieres otra solo cambias la columna
@app.route('/category_filter/<string:category>', methods=['GET'])  
def filter(category):
    tasks = Videogames.query.filter(Videogames.category == category).all()
    if not tasks:
        abort(404)
    return jsonify([task.llenar() for task in tasks]), 201


#Para ordenar los juegos alfabeticamente
@app.route('/order_asc', methods=['GET'])  
def order():
    tasks = Videogames.query.order_by(Videogames.name).all()
    if not tasks:
        abort(404)
    return jsonify([task.llenar() for task in tasks]), 201

#Para mostrarlo en el html
@app.route('/show_videogames', methods=['GET'])  
def show_games():
    games = Videogames.query.all()
    return render_template('index.html', games=games)

if __name__ == '__main__':  
    with app.app_context():  
        db.create_all()  
        print("Tables created...")

    app.run(debug=True)  
    

from flask import Flask, render_template, url_for, request, redirect
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    task = db.Column(db.String(200), nullable=False)
    made = db.Column(db.String(200), default=date.today())
    steps = db.relationship('Step', backref='todo')
    def __repr__(self):
         return f"{self.task}"

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    procedure = db.Column(db.String(200), nullable=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'))
    def __repr__(self):
         return f"{self.procedure}"

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_task = Todo(name=request.form['content2'], task=request.form['content'])
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR: can not add to database'
    else:
        tasks = Todo.query.order_by(Todo.made).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except:
        return "ERROR: can not delete object"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    change_task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        change_task.task = request.form['content']
        change_task.name = request.form['content2']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR: can not edit goal'
    else:
        return render_template('update.html', task=change_task)


@app.route('/update_steps/<int:id>', methods=['GET', 'POST'])
def update_steps_list(id):
    if request.method == 'POST':
        try:
            new_step = Step(procedure=request.form['content'], todo_id = id)
            db.session.add(new_step)
            db.session.commit()
            return redirect('/')           #fix pathway
        except:
            return 'ERROR: can not update your steps'
    else:
        return render_template('update.html')


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import fcntl

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    srl = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.srl} - {self.title}"



@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:srl>', methods=['GET', 'POST'])
def update(srl):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        toup = Todo.query.filter_by(srl=srl).first()
        toup.title = title
        toup.desc = desc
        db.session.add(toup)
        db.session.commit()
        return redirect("/")

    toup = Todo.query.filter_by(srl=srl).first()
    return render_template('update.html', toup=toup)

@app.route('/delete/<int:srl>')
def delete(srl):
    todele = Todo.query.filter_by(srl=srl).first()
    print(todele)
    db.session.delete(todele)
    db.session.commit()
    return redirect("/")


app.app_context().push()

if __name__ == "__main__":
    app.run(debug=True)
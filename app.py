from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title =  db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/',methods=['GET','POST'])
def hello_word():
    if(request.method=='POST'):
        print(request.form['title'])
        print("it is the post API!!")
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo) 
        db.session.commit()
    allTodo=Todo.query.all() 
    # return 'hello world! this is the flask || tutorial!!'
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if(request.method=='POST'):
        print("--= enter the first stage of upadate =--")
        # it is update operation
        print(request.form['title'])
        print("it is the post API!!")
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo) 
        db.session.commit()
        print("==== enter the update last stage ====")
        return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()
    print("---  going to update page---")
    print(todo)
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route('/show')
def show():
    todoall=Todo.query.all() 
    print(todoall)
    print("hello world for showing the python route!!")
    return 'this is the production page!'

@app.route('/html')
def htmluse():
    return render_template('index.html')
           
if __name__=="__main__":
    app.run(debug=True, port=2929)
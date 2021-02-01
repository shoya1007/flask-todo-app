from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
#下記によってtodo.dbという名前のデータベースを設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
#dbを生成
db=SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)
    
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)
    
    else:
        #POSTされた内容を受け取る
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        #受け取った文字型の日付を日付型に変換
        due = datetime.datetime.strptime(due, '%Y-%m-%d')
        #Postクラスに受け取った内容を渡す
        new_post = Post(title=title, detail=detail, due=due)
        
        #dbに内容を追加
        db.session.add(new_post)
        #追加した内容を保存
        db.session.commit()
        return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)

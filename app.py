import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import flask_login
import datetime

login_manager = flask_login.LoginManager()

# users = {'foo@bar.tld': {'password': 'secret'}}

app = Flask(__name__)
# login_manager.init_app(app)
app.secret_key = 'secret'
# mail = Mail(app)

#下記によってtodo.dbという名前のデータベースを設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# メールサーバーとしてsmtp.sendgrid.netを指定
# app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
# # ポート番号として587を指定
# app.config['MAIL_PORT'] = 587
# # TLS通信を有効化
# app.config['MAIL_USE_TLS'] = True
# # 認証情報として、ユーザ名にapikey(全てのsendgridアカウントで共通)を指定
# app.config['MAIL_USERNAME'] = 'apikey'
# # 認証情報として、パスワードを設定
# app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
# app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
# mail=Mail(app)
#dbを生成
db=SQLAlchemy(app)

engine=sqlalchemy.create_engine('sqlite:///todo.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

class User(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password=db.Column(db.String(20), nullable=False)

if __name__ == '__main__':
    db.create_all()

# @login_manager.user_loader
# def user_loader(user_id):
#     # if email not in users:
#     #     return
#     user = User()
#     user_id=user.id
#     print(user_id)
    
#     user = session.query(User).filter(User.id==user_id).first()
#     # user=User()
#     print('45:', user)
#     return user


# @login_manager.request_loader
# def request_loader(request):
#     email = request.form.get('email')
#     print('52:', email)
#     user = session.query(User).filter(User.email == email).first()
#     print(type(user))
#     print(user)
#     # if email!=user.email:
#     #     return

#     # user = User()
#     # user.id = email

    
#     # user.is_authenticated = request.form['password'] == users[email['password']]
#     # print(user)
#     # user.is_authenticated = request.form.get('password') == user.password
#     # user.is_authenticated=request.form['password']==user.password
#     return user

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')

    # print(request.form.get('password'))
    # email = request.form.get('email')
    # print(email) 
    # user = session.query(User).filter(User.email == email).one()    
    # print(user) 
    # if request.form['password'] == users[email]['password']:
    #     user = User()
    #     user.id = email
    #     flask_login.login_user(user)
    #     return redirect('/index')

    # if request.form['password'] == user.password:        
    #     flask_login.login_user(user)    
    #     return redirect('/index')

    # return 'Bad login'

# @app.route('/protected')
# @flask_login.login_required
# def protected():
#     return 'Logged in as:' + flask_login.current_user.id

# @app.route('/logout')
# def logout():
#     flask_login.logout_user()
#     return redirect('/')

# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':        
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        # return render_template('login.html')
        return redirect('/')

@app.route('/index', methods=['GET', 'POST'])
# @flask_login.login_required
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()        
        # user_name = flask_login.current_user.name
        # print(user_name)
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
        
        return redirect('/index')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect('/index')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.datetime.strptime(request.form.get('due'), '%Y-%m-%d')
        
        db.session.commit()
        return redirect('/index')

if __name__ == '__main__':
    app.run(debug=True)

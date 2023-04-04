from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_restful import Api
from data import db_session


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# login_manager = LoginManager()
# login_manager.init_app(app)
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     db_sess = db_session.create_session()
#     return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Тест')


def main():
    app.run()


if __name__ == '__main__':
    main()
from flask import Flask, render_template, redirect
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_restful import Api
from data import db_session
from data.accessory import Accessory
from data.clothes import Clothes
from data.login_form import LoginForm
from data.sneakers import Sneakers
from data.sports import Sports
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).all()
    clothes = db_sess.query(Clothes).all()
    accessory = db_sess.query(Accessory).all()
    sports = db_sess.query(Sports).all()
    return render_template('index.html', title='Тест', sneakers=sneakers, clothes=clothes, accessory=accessory, sports=
                           sports)

@app.route('/shoes_page')
def shoes_page():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).all()
    return render_template('test.html', title='Тест', sneakers=sneakers)


def main():
    db_session.global_init("db/store.db")
    app.run()
    # user = Sports()
    # user.name = "Nike Kiger 9"
    # user.description = """На каменистых и неровных дорожках выбирайте комфорт и скорость Kiger 9. Эта обувь
    #                       предназначена для любых неожиданных и напряженных ситуаций. Благодаря полноразмерному
    #                       пеноматериалу Nike React и новому воздухопроницаемому верху эти маневренные и быстрые
    #                       кроссовки идеально подходят для быстрого перехода из города в тропу. Ближе к земле и легче,
    #                       чем предыдущая версия, это идеальный союзник для катания по тропам в полной безопасности."""
    # user.picture = "img/sports/sports_3.jpg"
    # user.sex = 'male'
    # user.cost = 159.99
    # user.type = 'basketball'
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()

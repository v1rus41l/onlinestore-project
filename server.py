from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.security import check_password_hash
import datetime

from data import db_session
from data.accessory import Accessory
from data.basket import Basket
from data.clothes import Clothes
from data.favourite import Favourite
from data.login_form import LoginForm
from data.sneakers import Sneakers
from data.sports import Sports
from data.users import User
from forms.user import RegisterForm
from forms.confirm_email import ConfirmForm
from data.message_sender import send_email
from data import accessory_resources, sport_resources, clothes_resources, sneakers_resources

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
user_email = ''
user_name = ''
user_surname = ''
user_password = ''
cod = ''

# для списка объектов
api.add_resource(accessory_resources.AccessoryListResource, '/api/v2/accessory')

# для одного объекта
api.add_resource(accessory_resources.AccessoryResource, '/api/v2/accessory/<int:accessory_id>')

# для списка объектов
api.add_resource(sport_resources.SportListResource, '/api/v2/sport')

# для одного объекта
api.add_resource(sport_resources.SportResource, '/api/v2/sport/<int:sport_id>')

# для списка объектов
api.add_resource(sneakers_resources.SneakersListResource, '/api/v2/sneakers')

# для одного объекта
api.add_resource(sneakers_resources.SneakersResource, '/api/v2/sneakers/<int:sneakers_id>')

# для списка объектов
api.add_resource(clothes_resources.ClothesListResource, '/api/v2/clothes')

# для одного объекта
api.add_resource(clothes_resources.ClothesResource, '/api/v2/clothes/<int:clothes_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).all()[:3]
    clothes = db_sess.query(Clothes).all()[:3]
    accessory = db_sess.query(Accessory).all()[:3]
    sports = db_sess.query(Sports).all()[:3]
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('index.html', title='Главная страница', sneakers=sneakers, clothes=clothes,
                               accessory=accessory, sports=
                               sports, user=user)
    else:
        db_sess.close()
        return render_template('index.html', title='Главная страница', sneakers=sneakers, clothes=clothes,
                               accessory=accessory, sports=
                               sports)



def main():
    db_session.global_init("db/store.db")
    app.run()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global user_name, user_email, user_password, user_surname, cod
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            db_sess.close()
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user_email = form.email.data
        user_name = form.name.data
        user_surname = form.surname.data
        user_password = form.password.data
        cod = send_email(user_email)
        db_sess.close()
        return redirect('/email_confirming')
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('register.html', title='Регистрация', form=form, user=user)
    else:
        db_sess.close()
        return render_template('register.html', title='Регистрация', form=form)


@app.route('/email_confirming', methods=['GET', 'POST'])
def email_confirming():
    global user_name, user_email, user_password, user_surname
    form = ConfirmForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if form.cod.data != cod:
            db_sess.close()
            return render_template('confirm.html', title='Регистрация',
                                   form=form,
                                   message="Неверный код")
        user = User(
            name=user_name,
            surname=user_surname,
            email=user_email,
        )
        user.set_password(user_password)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    db_sess.close()
    return render_template('confirm.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect("/")
        if current_user.is_authenticated:
            user = db_sess.query(User).filter(User.id == current_user.id)[0]
            db_sess.close()
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form, user=user)
        else:
            db_sess.close()
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('login.html', title='Авторизация', form=form, user=user)
    else:
        db_sess.close()
        return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/shoes_page')
def shoes_page():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).all()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers, user=user)
    else:
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


# shoes_filter
@app.route('/shoes_min_to_max')
def shoes_min_to_max():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).order_by(Sneakers.cost)
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers, user=user)
    else:
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)

@app.route('/shoes_max_to_min')
def shoes_max_to_min():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).order_by(Sneakers.cost)[::-1]
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers, user=user)
    else:
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


@app.route('/shoes_male')
def shoes_male():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).filter(Sneakers.sex == 'male')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers, user=user)
    else:
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


@app.route('/shoes_female')
def shoes_female():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).filter(Sneakers.sex == 'female')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers, user=user)
    else:
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


@app.route('/shoes_kids')
def shoes_kids():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).filter(Sneakers.sex == 'kids')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers, user=user)
    else:
        db_sess.close()
        return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


@app.route('/clothes_page')
def clothes_page():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).all()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes, user=user)
    else:
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes)


# shoes_filter
@app.route('/clothes_min_to_max')
def clothes_min_to_max():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).order_by(Clothes.cost)
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes, user=user)
    else:
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes)

@app.route('/clothes_max_to_min')
def clothes_max_to_min():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).order_by(Clothes.cost)[::-1]
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes, user=user)
    else:
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes)


@app.route('/clothes_male')
def clothes_male():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).filter(Clothes.sex == 'male')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes, user=user)
    else:
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes)


@app.route('/clothes_female')
def clothes_female():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).filter(Clothes.sex == 'female')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes, user=user)
    else:
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes)


@app.route('/clothes_kids')
def clothes_kids():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).filter(Clothes.sex == 'kids')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes, user=user)
    else:
        db_sess.close()
        return render_template('clothes_page.html', title='Одежда', clothes=clothes)


@app.route('/accessory_page')
def accessory_page():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).all()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory, user=user)
    else:
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


#accessory filters
@app.route('/accessory_max_to_min')
def accessory_max_to_min():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).order_by(Accessory.cost)[::-1]
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory, user=user)
    else:
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


@app.route('/accessory_min_to_max')
def accessory_min_to_max():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).order_by(Accessory.cost)
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory, user=user)
    else:
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)

@app.route('/accessory_bottle')
def accessory_bottle():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).filter(Accessory.type == 'bottle')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory, user=user)
    else:
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)

@app.route('/accessory_ball')
def accessory_ball():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).filter(Accessory.type == 'ball')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory, user=user)
    else:
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


@app.route('/accessory_headdress')
def accessory_headdress():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).filter(Accessory.type == 'headdress')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory, user=user)
    else:
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


@app.route('/accessory_bag')
def accessory_bag():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).filter(Accessory.type == 'bag')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory, user=user)
    else:
        db_sess.close()
        return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


@app.route('/sports_page')
def sports_page():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).all()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports, user=user)
    else:
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports)


#sports filter
@app.route('/sports_min_to_max')
def sports_min_to_max():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).order_by(Sports.cost)
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports, user=user)
    else:
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/sports_max_to_min')
def sports_max_to_min():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).order_by(Sports.cost)[::-1]
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports, user=user)
    else:
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports)

@app.route('/sports_soccer')
def sports_soccer():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'football')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports, user=user)
    else:
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports)



@app.route('/sports_running')
def sports_running():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'running')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports, user=user)
    else:
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/sports_basketball')
def sports_basketball():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'basketball')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports, user=user)
    else:
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/sports_tennis')
def sports_tennis():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'tennis')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports, user=user)
    else:
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/sports_golf')
def sports_golf():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'golf')
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports, user=user)
    else:
        db_sess.close()
        return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/shoes_tovar_<int:id>', methods=['GET', 'POST'])
def shoes_tovar(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        tovar = db_sess.query(Sneakers).filter(Sneakers.id == id
                                          ).first()
        try:
            favourite = db_sess.query(Favourite).filter(Favourite.name == tovar.name, Favourite.by_who == current_user.id)[0]
            in_favourite = True
        except:
            in_favourite = False
        try:
            basket = db_sess.query(Basket).filter(Basket.name == tovar.name, Basket.by_who == current_user.id)[0]
            in_basket = True
        except:
            in_basket = False
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('tovar_shoes.html',
                               title=f'{tovar.name}', tovar=tovar, in_favourite=in_favourite,
                               in_basket=in_basket, user=user)
    else:
        db_sess.close()
        return render_template('tovar_shoes.html',
                               title=f'{tovar.name}', tovar=tovar, in_favourite=in_favourite,
                               in_basket=in_basket)


@app.route('/clothes_tovar_<int:id>', methods=['GET', 'POST'])
def clothes_tovar(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        tovar = db_sess.query(Clothes).filter(Clothes.id == id
                                          ).first()
        try:
            favourite = db_sess.query(Favourite).filter(Favourite.name == tovar.name, Favourite.by_who == current_user.id)[0]
            in_favourite = True
        except:
            in_favourite = False
        try:
            basket = db_sess.query(Basket).filter(Basket.name == tovar.name, Basket.by_who == current_user.id)[0]
            in_basket = True
        except:
            in_basket = False
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('tovar_clothes.html',
                               title=f'{tovar.name}',
                               tovar=tovar,
                               in_favourite=in_favourite,
                               in_basket=in_basket,
                               user=user
                               )
    else:
        db_sess.close()
        return render_template('tovar_clothes.html',
                               title=f'{tovar.name}',
                               tovar=tovar,
                               in_favourite=in_favourite,
                               in_basket=in_basket,
                               )


@app.route('/accessory_tovar_<int:id>', methods=['GET', 'POST'])
def accessory_tovar(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        tovar = db_sess.query(Accessory).filter(Accessory.id == id
                                          ).first()
        try:
            favourite = db_sess.query(Favourite).filter(Favourite.name == tovar.name, Favourite.by_who == current_user.id)[0]
            in_favourite = True
        except:
            in_favourite = False
        try:
            basket = db_sess.query(Basket).filter(Basket.name == tovar.name, Basket.by_who == current_user.id)[0]
            in_basket = True
        except:
            in_basket = False
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('tovar_accessory.html',
                               title=f'{tovar.name}',
                               tovar=tovar,
                               in_favourite=in_favourite,
                               in_basket=in_basket,
                               user=user
                               )
    else:
        db_sess.close()
        return render_template('tovar_accessory.html',
                               title=f'{tovar.name}',
                               tovar=tovar,
                               in_favourite=in_favourite,
                               in_basket=in_basket,
                               )


@app.route('/sport_tovar_<int:id>', methods=['GET', 'POST'])
def sport_tovar(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        tovar = db_sess.query(Sports).filter(Sports.id == id
                                          ).first()
        try:
            favourite = db_sess.query(Favourite).filter(Favourite.name == tovar.name, Favourite.by_who == current_user.id)[0]
            in_favourite = True
        except:
            in_favourite = False
        try:
            basket = db_sess.query(Basket).filter(Basket.name == tovar.name, Basket.by_who == current_user.id)[0]
            in_basket = True
        except:
            in_basket = False
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('tovar_sport.html',
                               title=f'{tovar.name}',
                               tovar=tovar,
                               in_favourite=in_favourite,
                               in_basket=in_basket, user=user
                               )
    else:
        db_sess.close()
        return render_template('tovar_sport.html',
                               title=f'{tovar.name}',
                               tovar=tovar,
                               in_favourite=in_favourite,
                               in_basket=in_basket
                               )


@app.route('/basket')
def basket():
    if request.method == "GET":
        db_sess = db_session.create_session()
        basket = db_sess.query(Basket).filter(Basket.by_who == current_user.id).all()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        db_sess.close()
        return render_template('basket.html',
                               title='Корзина',
                               basket=basket,
                               user=user)
    else:
        db_sess.close()
        return render_template('basket.html',
                               title='Корзина',
                               basket=basket)


@app.route('/basket_add_shoes_<int:id>',  methods=['GET', 'POST'])
@login_required
def add_basket_shoes(id):
    db_sess = db_session.create_session()
    tovar = db_sess.query(Sneakers).filter(Sneakers.id == id
                                         ).first()
    db_sess = db_session.create_session()
    basket = Basket()
    basket.name = tovar.name
    basket.cost = tovar.cost
    basket.picture = tovar.picture
    basket.type = 'shoes'
    basket.by_who = current_user.id
    basket.tovar_id = tovar.id
    db_sess.add(basket)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/shoes_tovar_{tovar.id}')


@app.route('/basket_add_clothes_<int:id>',  methods=['GET', 'POST'])
@login_required
def add_basket_clothes(id):
    db_sess = db_session.create_session()
    tovar = db_sess.query(Clothes).filter(Clothes.id == id
                                         ).first()
    db_sess = db_session.create_session()
    basket = Basket()
    basket.name = tovar.name
    basket.cost = tovar.cost
    basket.picture = tovar.picture
    basket.type = 'clothes'
    basket.by_who = current_user.id
    basket.tovar_id = tovar.id
    db_sess.add(basket)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/clothes_tovar_{tovar.id}')


@app.route('/basket_add_accessory_<int:id>',  methods=['GET', 'POST'])
@login_required
def add_basket_accessory(id):
    db_sess = db_session.create_session()
    tovar = db_sess.query(Accessory).filter(Accessory.id == id
                                         ).first()
    db_sess = db_session.create_session()
    basket = Basket()
    basket.name = tovar.name
    basket.cost = tovar.cost
    basket.picture = tovar.picture
    basket.type = 'accessory'
    basket.tovar_id = tovar.id
    basket.by_who = current_user.id
    db_sess.add(basket)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/accessory_tovar_{tovar.id}')


@app.route('/basket_add_sport_<int:id>',  methods=['GET', 'POST'])
@login_required
def add_basket_sport(id):
    db_sess = db_session.create_session()
    tovar = db_sess.query(Sports).filter(Sports.id == id
                                         ).first()
    db_sess = db_session.create_session()
    basket = Basket()
    basket.name = tovar.name
    basket.cost = tovar.cost
    basket.picture = tovar.picture
    basket.type = 'sport'
    basket.by_who = current_user.id
    basket.tovar_id = tovar.id
    db_sess.add(basket)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/sport_tovar_{tovar.id}')


@app.route('/basket_delete_item_<int:id>',  methods=['GET', 'POST'])
@login_required
def delete_basket_sport(id):
    db_sess = db_session.create_session()
    basket = db_sess.query(Basket).filter(Basket.id == id).first()
    db_sess.delete(basket)
    db_sess.commit()
    db_sess.close()
    return redirect('/basket')


@app.route('/favourite')
def favourite():
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        favourite = db_sess.query(Favourite).filter(Favourite.by_who == current_user.id).all()
        db_sess.close()
    if current_user.is_authenticated:
        return render_template('favourite.html',
                               title='Избранное',
                               favourite=favourite, user=user
                               )
    else:
        return render_template('favourite.html',
                               title='Избранное',
                               favourite=favourite
                               )


@app.route('/favourite_add_shoes_<int:id>',  methods=['GET', 'POST'])
@login_required
def add_favourite_shoes(id):
    db_sess = db_session.create_session()
    tovar = db_sess.query(Sneakers).filter(Sneakers.id == id
                                         ).first()
    db_sess = db_session.create_session()
    favourite = Favourite()
    favourite.name = tovar.name
    favourite.cost = tovar.cost
    favourite.picture = tovar.picture
    favourite.type = 'shoes'
    favourite.by_who = current_user.id
    favourite.tovar_id = tovar.id
    db_sess.add(favourite)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/shoes_tovar_{tovar.id}')


@app.route('/favourite_add_clothes_<int:id>',  methods=['GET', 'POST'])
@login_required
def add_favourite_clothes(id):
    db_sess = db_session.create_session()
    tovar = db_sess.query(Clothes).filter(Clothes.id == id
                                         ).first()
    db_sess = db_session.create_session()
    favourite = Favourite()
    favourite.name = tovar.name
    favourite.cost = tovar.cost
    favourite.picture = tovar.picture
    favourite.type = 'clothes'
    favourite.tovar_id = tovar.id
    favourite.by_who = current_user.id
    db_sess.add(favourite)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/clothes_tovar_{tovar.id}')


@app.route('/favourite_add_accessory_<int:id>',  methods=['GET', 'POST'])
@login_required
def add_favourite_accessory(id):
    db_sess = db_session.create_session()
    tovar = db_sess.query(Accessory).filter(Accessory.id == id
                                         ).first()
    db_sess = db_session.create_session()
    favourite = Favourite()
    favourite.name = tovar.name
    favourite.cost = tovar.cost
    favourite.picture = tovar.picture
    favourite.type = 'accessory'
    favourite.by_who = current_user.id
    favourite.tovar_id = tovar.id
    db_sess.add(favourite)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/accessory_tovar_{tovar.id}')


@app.route('/favourite_add_sport_<int:id>',  methods=['GET', 'POST'])
@login_required
def add_favourite_sport(id):
    db_sess = db_session.create_session()
    tovar = db_sess.query(Sports).filter(Sports.id == id
                                         ).first()
    db_sess = db_session.create_session()
    favourite = Favourite()
    favourite.name = tovar.name
    favourite.cost = tovar.cost
    favourite.picture = tovar.picture
    favourite.by_who = current_user.id
    favourite.tovar_id = tovar.id
    favourite.type = 'sport'
    db_sess.add(favourite)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/sport_tovar_{tovar.id}')


@app.route('/fav_delete_item_<int:id>',  methods=['GET', 'POST'])
@login_required
def delete_fav_sport(id):
    db_sess = db_session.create_session()
    favourite = db_sess.query(Favourite).filter(Favourite.id == id).first()
    db_sess.delete(favourite)
    db_sess.commit()
    db_sess.close()
    return redirect('/favourite')


@app.route('/profile')
def profile():
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id)[0]
        favourite = list(db_sess.query(Favourite).filter(Favourite.by_who == current_user.id))[-3:][::-1]
        date = user.created_date.strftime("%B %Y")
        db_sess.close()
    return render_template('profile.html',
                           title='Профиль',
                           user=user,
                           favourite=favourite, date=date
                           )

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id)[0]
    db_sess.close()
    return render_template('settings.html',
                           title='Настройки профиля', user=user
                           )

@app.route('/ava_form', methods=['GET', 'POST'])
def ava_form():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id)[0]
    photo = request.files['file']
    if photo and photo.filename[photo.filename.find('.') + 1:] in (
            'png',
            'jpg',
            'jpeg'
    ):
        with open(f'static/img/user-photos/user_{user.id}.png', 'wb') as file:
            file.write(photo.read())
            user.avatar = f'/img/user-photos/user_{user.id}.png'
            db_sess.commit()
    db_sess.close()
    return redirect('/settings')


@app.route('/info_form', methods=['GET', 'POST'])
def info_form():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id)[0]
    user.name = request.form['name']
    user.surname = request.form['surname']
    db_sess.commit()
    db_sess.close()
    return redirect('/settings')


@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id)[0]
    print(request.form['old_pass'])
    if user.check_password(request.form['old_pass']):
        if not request.form['new_pass'] or not request.form['repeat_pass']:
            db_sess.close()
            return render_template('settings.html',
                                   title='Настройки профиля', user=user,
                                   message='Поля должны быть заполнены'
                                   )
        elif request.form['new_pass'] == request.form['repeat_pass']:
            user.set_password(request.form['new_pass'])
            db_sess.commit()
            db_sess.close()
            return redirect('/settings')
        else:
            db_sess.close()
            return render_template('settings.html',
                                   title='Настройки профиля', user=user,
                                   message='Пароли не совпадают'
                                   )
    else:
        db_sess.close()
        return render_template('settings.html',
                               title='Настройки профиля', user=user,
                               message='Неверный пароль'
                               )


if __name__ == '__main__':
    main()

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
    sneakers = db_sess.query(Sneakers).all()[:3]
    clothes = db_sess.query(Clothes).all()[:3]
    accessory = db_sess.query(Accessory).all()[:3]
    sports = db_sess.query(Sports).all()[:3]
    return render_template('index.html', title='Тест', sneakers=sneakers, clothes=clothes, accessory=accessory, sports=
                           sports)


def main():
    db_session.global_init("db/store.db")
    app.run()
    # user = Clothes()
    # user.name = "Nike Sportswear Phoenix Fleece"
    # user.description = """Обновите свой флисовый гардероб этой ультра-комфортной моделью. Флисовая толстовка Phoenix с
    #                       объемным кроем и рельефной резинкой выглядит просто и без излишеств."""
    # user.picture = "img/clothes/clothes_4.jpg"
    # user.sex = 'female'
    # user.cost = 59.99
    # user2 = Clothes()
    # user2.name = "Nike Sportswear Tech Fleece Windrunner"
    # user2.description = """Худи Nike Sportswear Tech Fleece изготовлена из двусторонней структурной трехмерной ткани,
    #                        которая удерживает тепло вашего тела, не будучи слишком громоздкой и тяжелой."""
    # user2.picture = "img/clothes/clothes_5.jpg"
    # user2.sex = 'female'
    # user2.cost = 129.99
    # user3 = Clothes()
    # user3.name = "Nike Miler"
    # user3.description = """Базовая модель и икона бега — обновленная версия куртки Nike Miler. Эта водоотталкивающая
    #                        модель имеет капюшон для защиты от непогоды. Складная модель демонстрирует стиль, пропитанный
    #                        историей Nike. Этот продукт полностью изготовлен из переработанных полиэфирных волокон."""
    # user3.picture = "img/clothes/clothes_6.jpg"
    # user3.sex = 'male'
    # user3.cost = 89.99
    # user4 = Clothes()
    # user4.name = "Nike Sportswear Club"
    # user4.description = """Носите его отдельно или под другим слоем для тренировок в прохладную погоду. Худи Nike
    #                        Sportswear из теплого флиса с начесом внутри для невероятной мягкости."""
    # user4.picture = "img/clothes/clothes_7.jpg"
    # user4.sex = 'kids'
    # user4.cost = 49.99
    # user5 = Clothes()
    # user5.name = "Nike Sportswear Phoenix Fleece"
    # user5.description = """Обновите свой флисовый гардероб этой ультра-комфортной моделью. Свободный ультрадлинный крой
    #                     и разрезы по кромке этих брюк из ткани Fleece Phoenix позволяют продемонстрировать свою любимую
    #                     обувь, а высокая талия в рубчик и большой шнурок придают эффектный вид."""
    # user5.picture = "img/clothes/clothes_8.jpg"
    # user5.sex = 'female'
    # user5.cost = 64.99
    # user6 = Clothes()
    # user6.name = "Nike Sportswear"
    # user6.description = """В этой толстовке большого размера достаточно места для рук и тела, что гарантирует вам
    #                     расслабленный комфорт, где бы вы ни находились (например, в классе). Гладкая снаружи и
    #                     начесанная внутри, эта легкая флисовая одежда легко надевается, когда вам нужно немного
    #                     дополнительного тепла."""
    # user6.picture = "img/clothes/clothes_9.jpg"
    # user6.sex = 'kids'
    # user6.cost = 54.99
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.add(user2)
    # db_sess.add(user3)
    # db_sess.add(user4)
    # db_sess.add(user5)
    # db_sess.add(user6)
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


@app.route('/shoes_page')
def shoes_page():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).all()
    return render_template('shoes_page.html', title='Тест', sneakers=sneakers)


# shoes_filter
@app.route('/shoes_min_to_max')
def shoes_min_to_max():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).order_by(Sneakers.cost)
    return render_template('clothes_min_to_max.html', title='Тест', sneakers=sneakers)

@app.route('/shoes_max_to_min')
def shoes_max_to_min():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).order_by(Sneakers.cost)[::-1]
    return render_template('clothes_max_to_min.html', title='Тест', sneakers=sneakers)


@app.route('/shoes_male')
def shoes_male():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).filter(Sneakers.sex == 'male')
    return render_template('shoes_male.html', title='Тест', sneakers=sneakers)


@app.route('/shoes_female')
def shoes_female():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).filter(Sneakers.sex == 'female')
    return render_template('shoes_female.html', title='Тест', sneakers=sneakers)


@app.route('/shoes_kids')
def shoes_kids():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).filter(Sneakers.sex == 'kids')
    return render_template('shoes_kids.html', title='Тест', sneakers=sneakers)


@app.route('/clothes_page')
def clothes_page():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).all()
    return render_template('clothes_page.html', title='Тест', clothes=clothes)


# shoes_filter
@app.route('/clothes_min_to_max')
def clothes_min_to_max():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).order_by(Clothes.cost)
    return render_template('clothes_min_to_max.html', title='Тест', clothes=clothes)

@app.route('/clothes_max_to_min')
def clothes_max_to_min():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).order_by(Clothes.cost)[::-1]
    return render_template('clothes_max_to_min.html', title='Тест', clothes=clothes)


@app.route('/clothes_male')
def clothes_male():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).filter(Clothes.sex == 'male')
    return render_template('clothes_male.html', title='Тест', clothes=clothes)


@app.route('/clothes_female')
def clothes_female():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).filter(Clothes.sex == 'female')
    return render_template('clothes_female.html', title='Тест', clothes=clothes)


@app.route('/clothes_kids')
def clothes_kids():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).filter(Clothes.sex == 'kids')
    return render_template('clothes_kids.html', title='Тест', clothes=clothes)


@app.route('/accessory_page')
def accessory_page():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).all()
    return render_template('accessory_page.html', title='Тест', accessory=accessory)


#accessory filters
@app.route('/accessory_max_to_min')
def accessory_max_to_min():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).all()
    return render_template('accessory_max_to_min.html', title='Тест', accessory=accessory)


@app.route('/accessory_min_to_max')
def accessory_min_to_max():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).all()
    return render_template('accessory_min_to_max.html', title='Тест', accessory=accessory)

@app.route('/accessory_bottle')
def accessory_bottle():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).all()
    return render_template('accessory_bottle.html', title='Тест', accessory=accessory)

@app.route('/accessory_ball')
def accessory_ball():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).all()
    return render_template('accessory_ball.html', title='Тест', accessory=accessory)


@app.route('/accessory_headdress')
def accessory_headdress():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).all()
    return render_template('accessory_headdress.html', title='Тест', accessory=accessory)


@app.route('/accessory_bag')
def accessory_bag():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).all()
    return render_template('accessory_bag.html', title='Тест', accessory=accessory)


if __name__ == '__main__':
    main()

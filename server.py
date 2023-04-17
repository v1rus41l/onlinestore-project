from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_restful import Api
from data import db_session
from data.accessory import Accessory
from data.basket import Basket
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
    return render_template('index.html', title='Главная страница', sneakers=sneakers, clothes=clothes, accessory=accessory, sports=
                           sports)


def main():
    db_session.global_init("db/store.db")
    app.run()
    # user = Sports()
    # user.name = "Nike Pegasus Turbo Next"
    # user.description = """Проглотите мили с легендарным крылатым ботинком. Благодаря обновленной пене, которая стала
    #                       легче и более отзывчивой, а также легкому верху этот красочный дизайн поможет вам набрать
    #                       темп, не жертвуя комфортом, когда вы пытаетесь побить свои личные рекорды. Эти вневременные
    #                       кроссовки изготовлены с использованием экологически ответственного подхода, по крайней мере,
    #                       50% его веса составляют переработанные материалы, но при этом они идеально подходят для
    #                       повседневной жизни."""
    # user.picture = "img/sports/sports_4.jpg"
    # user.sex = 'tennis'
    # user.cost = 179.99
    # user2 = Sports()
    # user2.name = "Nike Air Zoom Infinity Tour"
    # user2.description = """Мечтаете о Грузии весной? Мы, да. Эта версия с мягкими персиковыми тонами и чистой базой
    #                        приглашает вас насладиться теплым, обволакивающим бризом юга Соединенных Штатов. Два больших
    #                        блока Zoom Air. Больше места для ног. Лучшее сцепление. Все это помогает вам выкладываться по
    #                        максимуму на протяжении всей игры. Яркие детали и фруктовые акценты напоминают о том, что
    #                        нужно сохранять хладнокровие, несмотря ни на что."""
    # user2.picture = "img/sports/sports_5.jpg"
    # user2.sex = 'golf'
    # user2.cost = 249.99
    # user3 = Sports()
    # user3.name = "Nike Gripknit Phantom GX"
    # user3.description = """Вы хотите улучшить свою игру? Разработанные для вас и для самых больших звезд мира, бутсы
    #                        Elite предлагают беспрецедентное качество. Потому что мы знаем, что вы требуете совершенства
    #                        как для себя, так и для своей обуви. В этих бутсах используется революционная технология Nike
    #                        Gripknit, обеспечивающая лучшее сцепление с мячом. Их интуитивно понятный дизайн обеспечивает
    #                        непревзойденную точность при бросках и дриблинге."""
    # user3.picture = "img/sports/sports_6.jpg"
    # user3.sex = 'football'
    # user3.cost = 289.99
    # user4 = Sports()
    # user4.name = "Air Jordan XXXVII"
    # user4.description = """У вас есть страсть к баскетболу и скорости? Наденьте эти кроссовки и раскройте весь свой
    #                        потенциал на корте. Последний AJ был разработан для идеального взлета и посадки, с
    #                        несколькими вставками Air для дополнительного отскока и нашей фирменной пеной Formula 23 для
    #                        поглощения ударов. Верх выполнен из прочной ткани перевивочного переплетения. Вы получаете
    #                        оптимальную поддержку без ущерба для качества игры."""
    # user4.picture = "img/sports/sports_7.jpg"
    # user4.sex = 'basketball'
    # user4.cost = 199.99
    # user5 = Sports()
    # user5.name = "Nike Invincible 3"
    # user5.description = """Предлагая максимальную амортизацию при каждом шаге, Invincible 3 гарантирует исключительный
    #                        комфорт, чтобы оставаться на вершине в любых обстоятельствах. Этот упругий и поддерживающий
    #                        дизайн, созданный для того, чтобы держать вас в тонусе, поможет вам пройти любимую трассу и
    #                        перенесет вас на следующую пробежку с новыми силами."""
    # user5.picture = "img/sports/sports_8.jpg"
    # user5.sex = 'running'
    # user5.cost = 209.99
    # user6 = Sports()
    # user6.name = "LeBron XX"
    # user6.description = """После почти двадцати лет карьеры, которая превзошла все ожидания, Леброн Джеймс по-прежнему
    #                        отказывается довольствоваться чем-либо, кроме совершенства, даже когда он устанавливает
    #                        стандарты для будущих поколений. Сегодня его новейшие фирменные кроссовки LeBron XX
    #                        (или LeBron 20) стали легче, ниже и невероятно быстры. Это не похоже ни на одну другую обувь,
    #                        которую Леброн носил до сих пор. Обладая невероятным комфортом и поддержкой, он поставляется
    #                        в сверхбыстром низком профиле, чтобы всегда быть на шаг впереди бешеной игры на паркетных
    #                        полах."""
    # user6.picture = "img/sports/sports_9.jpg"
    # user6.sex = 'basketball'
    # user6.cost = 249.99
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
    return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


# shoes_filter
@app.route('/shoes_min_to_max')
def shoes_min_to_max():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).order_by(Sneakers.cost)
    return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)

@app.route('/shoes_max_to_min')
def shoes_max_to_min():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).order_by(Sneakers.cost)[::-1]
    return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


@app.route('/shoes_male')
def shoes_male():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).filter(Sneakers.sex == 'male')
    return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


@app.route('/shoes_female')
def shoes_female():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).filter(Sneakers.sex == 'female')
    return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


@app.route('/shoes_kids')
def shoes_kids():
    db_sess = db_session.create_session()
    sneakers = db_sess.query(Sneakers).filter(Sneakers.sex == 'kids')
    return render_template('shoes_page.html', title='Кроссовки', sneakers=sneakers)


@app.route('/clothes_page')
def clothes_page():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).all()
    return render_template('clothes_page.html', title='Одежда', clothes=clothes)


# shoes_filter
@app.route('/clothes_min_to_max')
def clothes_min_to_max():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).order_by(Clothes.cost)
    return render_template('clothes_page.html', title='Одежда', clothes=clothes)

@app.route('/clothes_max_to_min')
def clothes_max_to_min():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).order_by(Clothes.cost)[::-1]
    return render_template('clothes_page.html', title='Одежда', clothes=clothes)


@app.route('/clothes_male')
def clothes_male():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).filter(Clothes.sex == 'male')
    return render_template('clothes_page.html', title='Одежда', clothes=clothes)


@app.route('/clothes_female')
def clothes_female():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).filter(Clothes.sex == 'female')
    return render_template('clothes_page.html', title='Одежда', clothes=clothes)


@app.route('/clothes_kids')
def clothes_kids():
    db_sess = db_session.create_session()
    clothes = db_sess.query(Clothes).filter(Clothes.sex == 'kids')
    return render_template('clothes_page.html', title='Одежда', clothes=clothes)


@app.route('/accessory_page')
def accessory_page():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).all()
    return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


#accessory filters
@app.route('/accessory_max_to_min')
def accessory_max_to_min():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).order_by(Accessory.cost)[::-1]
    return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


@app.route('/accessory_min_to_max')
def accessory_min_to_max():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).order_by(Accessory.cost)
    return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)

@app.route('/accessory_bottle')
def accessory_bottle():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).filter(Accessory.type == 'bottle')
    return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)

@app.route('/accessory_ball')
def accessory_ball():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).filter(Accessory.type == 'ball')
    return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


@app.route('/accessory_headdress')
def accessory_headdress():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).filter(Accessory.type == 'headdress')
    return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


@app.route('/accessory_bag')
def accessory_bag():
    db_sess = db_session.create_session()
    accessory = db_sess.query(Accessory).filter(Accessory.type == 'bag')
    return render_template('accessory_page.html', title='Аксессуары', accessory=accessory)


@app.route('/sports_page')
def sports_page():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).all()
    return render_template('sports_page.html', title='Спорт', sports=sports)


#sports filter
@app.route('/sports_min_to_max')
def sports_min_to_max():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).order_by(Sports.cost)
    return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/sports_max_to_min')
def sports_max_to_min():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).order_by(Sports.cost)[::-1]
    return render_template('sports_page.html', title='Спорт', sports=sports)

@app.route('/sports_soccer')
def sports_soccer():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'football')
    return render_template('sports_page.html', title='Спорт', sports=sports)



@app.route('/sports_running')
def sports_running():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'running')
    return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/sports_basketball')
def sports_basketball():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'basketball')
    return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/sports_tennis')
def sports_tennis():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'tennis')
    return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/sports_golf')
def sports_golf():
    db_sess = db_session.create_session()
    sports = db_sess.query(Sports).filter(Sports.type == 'golf')
    return render_template('sports_page.html', title='Спорт', sports=sports)


@app.route('/shoes_tovar_<int:id>', methods=['GET', 'POST'])
def shoes_tovar(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        tovar = db_sess.query(Sneakers).filter(Sneakers.id == id
                                          ).first()
    return render_template('tovar_shoes.html',
                           title=f'{tovar.name}',
                           tovar=tovar
                           )


@app.route('/clothes_tovar_<int:id>', methods=['GET', 'POST'])
def clothes_tovar(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        tovar = db_sess.query(Clothes).filter(Clothes.id == id
                                          ).first()
    return render_template('tovar_clothes.html',
                           title=f'{tovar.name}',
                           tovar=tovar
                           )


@app.route('/accessory_tovar_<int:id>', methods=['GET', 'POST'])
def accessory_tovar(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        tovar = db_sess.query(Accessory).filter(Accessory.id == id
                                          ).first()
    return render_template('tovar_accessory.html',
                           title=f'{tovar.name}',
                           tovar=tovar
                           )


@app.route('/sport_tovar_<int:id>', methods=['GET', 'POST'])
def sport_tovar(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        tovar = db_sess.query(Sports).filter(Sports.id == id
                                          ).first()
    return render_template('tovar_sport.html',
                           title=f'{tovar.name}',
                           tovar=tovar
                           )


@app.route('/basket')
def basket():
    if request.method == "GET":
        db_sess = db_session.create_session()
        basket = db_sess.query(Basket).all()
    return render_template('basket.html',
                           title='Корзина',
                           basket=basket
                           )


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
    db_sess.add(basket)
    db_sess.commit()
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
    db_sess.add(basket)
    db_sess.commit()
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
    db_sess.add(basket)
    db_sess.commit()
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
    db_sess.add(basket)
    db_sess.commit()
    return redirect(f'/sport_tovar_{tovar.id}')


@app.route('/basket_delete_item_<int:id>',  methods=['GET', 'POST'])
@login_required
def delete_basket_sport(id):
    db_sess = db_session.create_session()
    basket = db_sess.query(Basket).filter(Basket.id == id).first()
    db_sess.delete(basket)
    db_sess.commit()
    return redirect('/basket')


if __name__ == '__main__':
    main()

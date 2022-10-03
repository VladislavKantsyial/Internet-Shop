from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api,Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Запись:{self.title}'


@app.route('/')
def index():  # put application's code here
    Items = Item.query.order_by(Item.price).all()
    return render_template('index.html',data=Items)


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@app.route('/buy/<int:id>')
def item_buy(id):  # put application's code here
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
            secret_key='test')
    checkout = Checkout(api=api)
    data = {
    "currency": "RUB",
    "amount": str(item.price)+"00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)



@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Произошла ошибка'
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)

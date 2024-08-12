from flask import Flask , render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///stock.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Stock(db.Model):
    sno = db.Column(db.Integer ,primary_key=True)
    item_name = db.Column(db.String(100) ,nullable=False)
    quantity = db.Column(db.Integer ,nullable=False)
    purchase = db.Column(db.Float ,nullable=False)
    mrp = db.Column(db.Float ,nullable=False)

    def __repr__(self) -> str:
        # return f"{self.sno} - {self.mrp}"
        return super().__repr__()

with app.app_context():
    db.create_all()


@app.route('/', methods =['GET','POST'])
def home():
    if request.method == 'POST':
        item=request.form['item_name']
        quantity=request.form['quantity']
        purchase=request.form['purchase']
        mrp=request.form['mrp']
        stock=Stock(item_name=item,quantity=quantity,purchase=purchase,mrp=mrp)
        db.session.add(stock)
        db.session.commit()
    allstock=Stock.query.all()
    return render_template('app.html', allstock=allstock)
    



@app.route('/index')
def index():
    return render_template('update.html')
    

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        item=request.form['item_name']
        quantity=request.form['quantity']
        purchase=request.form['purchase']
        mrp=request.form['mrp']
        stock=Stock.query.filter_by(sno=sno).first()
        stock.item=item
        stock.quantity=quantity
        stock.purchase=purchase
        stock.mrp=mrp
        db.session.add(stock)
        db.session.commit()
        return redirect('/')
    stock=Stock.query.filter_by(sno=sno).first()
    return render_template('update.html', stock=stock)

@app.route('/delete/<int:sno>')
def delete(sno):
    stock=Stock.query.filter_by(sno=sno).first()
    db.session.delete(stock)
    db.session.commit()
    return redirect('/')
    



if __name__ == "__main__":
    app.run(debug=True)
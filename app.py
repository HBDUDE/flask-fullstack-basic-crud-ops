from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(15), unique=True, nullable=False)
  # price = db.Column(db.Float, nullable=False)
  # qty = db.Column(db.Integer, nullable=False)
  # date_added = db.Column(db.datetime, nullable=False, default=datetime.utcnow

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return f'Product {str(self.id)}'

@app.route("/")
def index():
  return "hello"

@app.route("/products", methods=["GET", "POST"])
def products():
  if request.method == "POST":
    name = request.form['name']
    new_product = Product(name=name)
    db.session.add(new_product)
    db.session.commit()
    return redirect('/products')
  elif len(Product.query.all()) == 0:
    return render_template("products-empty.html", products="You don't have any products yet!")
  return render_template("products.html", products=Product.query.all())

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
  target_product = Product.query.get_or_404(id)
  if request.method == "POST":
    target_product.name = request.form["name"]
    db.session.commit()
    return redirect("/products")
  return render_template("edit.html", target_product=target_product, id=id)

@app.route("/delete/<int:id>")
def delete(id): 
  target_product = Product.query.get_or_404(id)
  db.session.delete(target_product)
  db.session.commit()
  return redirect("/products")


if __name__ == "__main__":
  app.run(debug=True)
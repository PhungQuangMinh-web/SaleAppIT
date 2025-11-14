import math

from flask import render_template, request
from werkzeug.utils import redirect

import dao
from saleapp import app, login
from flask_login import login_user, current_user

@app.route("/")
def index():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    page = request.args.get("page")
    prods = dao.load_products(q=q, cate_id = cate_id)
    pages = math.ceil(dao.count_product()/app.config["PAGE_SIZE"])
    return render_template("index.html", prods = prods, pages = pages)

@app.route("/products/<int:id>")
def details(id):

    return render_template("product-details.html", prod=dao.get_product_by_id(id))

@app.context_processor
def common_atributes():
    return{
        "cates":dao.load_categories()
    }

@app.route("/login", methods =['get','post'])
def login_my_user():

    if current_user.is_authenticated:
        return redirect("/")

    err_msg = None

    if request.method.__eq__('POST'):
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = "Tai khoan hoac mat khau khong dung"
    return render_template("login.html", err_msg = err_msg)

@login.user_loader
def get_user(id):
    return dao.get_user_by_id(id)
if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
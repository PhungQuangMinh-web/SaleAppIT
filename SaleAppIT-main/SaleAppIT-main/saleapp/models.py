import json
from datetime import datetime
from saleapp import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from enum import Enum as RoleEnum
from flask_login import UserMixin


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2

class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name

class User(Base, UserMixin):
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    avatar = Column(String(300), default="https://www.gravatar.com/avatar/3b3be63a4c2a439b013787725dfce802?d=identicon")
    role = Column(Enum(UserRole), default=UserRole.USER)

class Category(Base):
    products = relationship('Product', backref='category', lazy=True)


class Product(Base):
    price = Column(Float, default=0.0)
    image = Column(String(300), default="https://cdn.tgdd.vn/Products/Images/44/282847/apple-macbook-air-m2-2022-01-750x500.jpg")
    cate_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    description = Column(String(300), nullable=True)

if __name__=="__main__":
    with app.app_context():
        # db.create_all()
        # c1 = Category(name="Laptop")
        # c2 = Category(name="Mobile")
        # c3 = Category(name="Tablet")
        # db.session.add_all([c1,c2,c3])
        # with open("data/product.json", encoding="utf-8") as f:
        #     products = json.load(f)
        #
        #     for p in products:
        #         db.session.add(Product(**p))
        # db.session.commit()
        import hashlib
        password=hashlib.md5("123".encode("utf-8")).hexdigest()

        u1 = User(name="User",username="user", password="123")
        db.session.add(u1)
        db.session.commit()
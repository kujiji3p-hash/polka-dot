# -*- coding: utf-8 -*-
"""
Polka Dot - Database Models
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """Admin user model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """Product categories"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(128))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    """Products (forms, gels, etc.)"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    short_desc = db.Column(db.String(256))

    # Pricing
    price = db.Column(db.Numeric(10, 2), nullable=False)
    old_price = db.Column(db.Numeric(10, 2))

    # Product details
    sku = db.Column(db.String(64), unique=True)
    composition = db.Column(db.Text)  # Состав
    volume = db.Column(db.String(32))  # Объем
    color = db.Column(db.String(32))  # Цвет
    action = db.Column(db.String(128))  # Действие
    shelf_life = db.Column(db.String(64))  # Срок годности
    country = db.Column(db.String(64))  # Страна производства
    material = db.Column(db.String(64))  # Материал
    package_contents = db.Column(db.String(256))  # Комплектация
    weight = db.Column(db.String(32))  # Вес

    # Images
    image_main = db.Column(db.String(256))
    image_gallery = db.Column(db.JSON)

    # Status
    status = db.Column(db.String(32), default='active')  # active, preorder, coming_soon, archived
    stock_quantity = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)

    # Foreign keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    preorders = db.relationship('Preorder', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > 0:
            return int((1 - float(self.price) / float(self.old_price)) * 100)
        return 0

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'price': str(self.price),
            'old_price': str(self.old_price) if self.old_price else None,
            'short_desc': self.short_desc,
            'status': self.status,
            'image': self.image_main,
            'category': self.category.name if self.category else None
        }


class Preorder(db.Model):
    """Preorder records"""
    __tablename__ = 'preorders'

    id = db.Column(db.Integer, primary_key=True)

    # Customer info
    customer_name = db.Column(db.String(128), nullable=False)
    customer_phone = db.Column(db.String(32), nullable=False)
    customer_email = db.Column(db.String(120))
    customer_comment = db.Column(db.Text)

    # Order details
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, default=1)

    # Status
    status = db.Column(db.String(32), default='pending')  # pending, confirmed, paid, shipped, cancelled

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Preorder {self.id}>'


class Announcement(db.Model):
    """Announcements and news"""
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)
    short_desc = db.Column(db.String(512))

    # Timeline
    event_date = db.Column(db.Date)
    is_featured = db.Column(db.Boolean, default=False)

    # Media
    image = db.Column(db.String(256))

    # Status
    status = db.Column(db.String(32), default='draft')  # draft, published, archived

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Announcement {self.title}>'


class SiteSettings(db.Model):
    """Site configuration settings"""
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(256))

    def __repr__(self):
        return f'<Setting {self.key}>'

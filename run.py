#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polka Dot Beauty - Main Application Entry Point
Version: 1.0
"""

from app import create_app, db
from app.models import Category, Product, Announcement

app = create_app()

with app.app_context():
    db.create_all()

    # Импортируем и выполняем ваш products.py
    import products

    #products.seed_data()  # если в products.py есть функция seed_data()

    # Или просто скопируйте сюда код из products.py напрямую:
    if not Category.query.first():
        forms = Category(name='Формы', slug='forms', description='Многоразовые формы', sort_order=1)
        gels = Category(name='Гели', slug='gels', description='Профессиональные гели', sort_order=2)
        db.session.add_all([forms, gels])
        db.session.commit()
        print('✅ Категории созданы')

    if not Product.query.first():
        p1 = Product(name='Salon Square', slug='salon-square', short_desc='Верхние формы. 140 шт.', price=1290,
                     status='active', is_featured=True, stock_quantity=100, category_id=1)
        p2 = Product(name='Гель для наращивания', slug='gel-dlya-narashchivaniya', short_desc='Розовый, 15 мл.',
                     price=890, status='active', stock_quantity=50, category_id=2)
        db.session.add_all([p1, p2])
        db.session.commit()
        print('✅ Продукты созданы')

if __name__ == '__main__':
    app.run()

# -*- coding: utf-8 -*-
"""
Polka Dot - Main Routes (Public Pages)
"""

from flask import render_template, request, flash, redirect, url_for, jsonify
from app.main import bp
from app.models import Product, Category, Announcement, Preorder
from app import db

@bp.route('/')
def index():
    """Home page"""
    featured_products = Product.query.filter_by(is_featured=True, status='active').limit(6).all()
    new_products = Product.query.filter_by(status='active').order_by(Product.created_at.desc()).limit(4).all()
    announcements = Announcement.query.filter_by(status='published').order_by(Announcement.event_date.asc()).limit(4).all()
    return render_template('index.html', 
                         featured=featured_products,
                         new_products=new_products,
                         announcements=announcements)

@bp.route('/products')
def products():
    """Products catalog"""
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category', None)
    status = request.args.get('status', 'active')

    query = Product.query

    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first_or_404()
        query = query.filter_by(category_id=category.id)

    if status:
        query = query.filter_by(status=status)

    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )

    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()

    return render_template('products.html', 
                         products=products,
                         categories=categories,
                         current_category=category_slug)

@bp.route('/product/<slug>')
def product_detail(slug):
    """Single product page"""
    product = Product.query.filter_by(slug=slug).first_or_404()
    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()
    return render_template('product_detail.html', product=product, related=related)

@bp.route('/preorder')
def preorder():
    """Preorder page"""
    preorder_products = Product.query.filter_by(status='preorder').order_by(Product.created_at.desc()).all()
    return render_template('preorder.html', products=preorder_products)

@bp.route('/preorder/submit', methods=['POST'])
def preorder_submit():
    """Submit preorder"""
    try:
        preorder = Preorder(
            customer_name=request.form.get('name'),
            customer_phone=request.form.get('phone'),
            customer_email=request.form.get('email'),
            customer_comment=request.form.get('comment'),
            product_id=request.form.get('product_id', type=int),
            quantity=request.form.get('quantity', 1, type=int)
        )
        db.session.add(preorder)
        db.session.commit()
        flash('Предзаказ успешно оформлен! Мы свяжемся с вами.', 'success')
        return redirect(url_for('main.preorder'))
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при оформлении предзаказа. Попробуйте снова.', 'error')
        return redirect(url_for('main.preorder'))

@bp.route('/announcements')
def announcements():
    """Announcements page"""
    page = request.args.get('page', 1, type=int)
    items = Announcement.query.filter_by(status='published').order_by(
        Announcement.event_date.asc()
    ).paginate(page=page, per_page=10, error_out=False)
    return render_template('announcements.html', announcements=items)

@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@bp.route('/api/products')
def api_products():
    """API: Get products JSON"""
    category = request.args.get('category')
    status = request.args.get('status', 'active')

    query = Product.query.filter_by(status=status)
    if category:
        query = query.join(Category).filter(Category.slug == category)

    products = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'slug': p.slug,
        'price': str(p.price),
        'old_price': str(p.old_price) if p.old_price else None,
        'short_desc': p.short_desc,
        'status': p.status,
        'image': p.image_main,
        'category': p.category.name if p.category else None
    } for p in products])

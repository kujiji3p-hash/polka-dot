# -*- coding: utf-8 -*-
"""
Polka Dot - Admin Routes
"""

from flask import render_template, request, flash, redirect, url_for, session
from functools import wraps
from app.admin import bp
from app.models import Product, Category, Announcement, Preorder, User
from app import db

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Доступ запрещен.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['is_admin'] = True
            session['admin_user'] = username
            return redirect(url_for('admin.dashboard'))
        flash('Неверные учетные данные', 'error')
    return render_template('admin/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))

@bp.route('/')
@admin_required
def dashboard():
    stats = {
        'products': Product.query.count(),
        'preorders': Preorder.query.count(),
        'announcements': Announcement.query.count(),
        'pending_preorders': Preorder.query.filter_by(status='pending').count()
    }
    recent_preorders = Preorder.query.order_by(Preorder.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, preorders=recent_preorders)

@bp.route('/products')
@admin_required
def admin_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/products.html', products=products)

@bp.route('/product/new', methods=['GET', 'POST'])
@admin_required
def new_product():
    categories = Category.query.all()
    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            slug=request.form.get('slug'),
            description=request.form.get('description'),
            short_desc=request.form.get('short_desc'),
            price=request.form.get('price'),
            old_price=request.form.get('old_price') or None,
            sku=request.form.get('sku'),
            composition=request.form.get('composition'),
            volume=request.form.get('volume'),
            color=request.form.get('color'),
            action=request.form.get('action'),
            shelf_life=request.form.get('shelf_life'),
            country=request.form.get('country'),
            material=request.form.get('material'),
            package_contents=request.form.get('package_contents'),
            weight=request.form.get('weight'),
            status=request.form.get('status', 'active'),
            stock_quantity=request.form.get('stock_quantity', 0, type=int),
            category_id=request.form.get('category_id', type=int),
            is_featured=bool(request.form.get('is_featured'))
        )
        db.session.add(product)
        db.session.commit()
        flash('Продукт создан', 'success')
        return redirect(url_for('admin.admin_products'))
    return render_template('admin/product_form.html', categories=categories)

@bp.route('/preorders')
@admin_required
def admin_preorders():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    query = Preorder.query
    if status:
        query = query.filter_by(status=status)
    preorders = query.order_by(Preorder.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/preorders.html', preorders=preorders)

@bp.route('/preorder/<int:id>/update', methods=['POST'])
@admin_required
def update_preorder(id):
    preorder = Preorder.query.get_or_404(id)
    preorder.status = request.form.get('status')
    db.session.commit()
    flash('Статус обновлен', 'success')
    return redirect(url_for('admin.admin_preorders'))

@bp.route('/announcements')
@admin_required
def admin_announcements():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements.html', announcements=announcements)

@bp.route('/announcement/new', methods=['GET', 'POST'])
@admin_required
def new_announcement():
    if request.method == 'POST':
        announcement = Announcement(
            title=request.form.get('title'),
            slug=request.form.get('slug'),
            content=request.form.get('content'),
            short_desc=request.form.get('short_desc'),
            event_date=request.form.get('event_date'),
            status=request.form.get('status', 'draft'),
            is_featured=bool(request.form.get('is_featured'))
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Анонс создан', 'success')
        return redirect(url_for('admin.admin_announcements'))
    return render_template('admin/announcement_form.html')

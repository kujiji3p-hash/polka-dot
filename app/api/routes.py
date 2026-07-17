# -*- coding: utf-8 -*-
"""
Polka Dot - API Routes
"""

from flask import jsonify, request
from app.api import bp
from app.models import Product, Category, Announcement

@bp.route('/products')
def get_products():
    category = request.args.get('category')
    status = request.args.get('status', 'active')
    query = Product.query.filter_by(status=status)
    if category:
        query = query.join(Category).filter(Category.slug == category)
    products = query.all()
    return jsonify({
        'success': True,
        'data': [{
            'id': p.id, 'name': p.name, 'slug': p.slug,
            'price': str(p.price), 'status': p.status
        } for p in products]
    })

@bp.route('/categories')
def get_categories():
    categories = Category.query.filter_by(is_active=True).all()
    return jsonify({
        'success': True,
        'data': [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in categories]
    })

@bp.route('/announcements')
def get_announcements():
    announcements = Announcement.query.filter_by(status='published').all()
    return jsonify({
        'success': True,
        'data': [{
            'id': a.id, 'title': a.title, 'slug': a.slug,
            'event_date': str(a.event_date) if a.event_date else None
        } for a in announcements]
    })

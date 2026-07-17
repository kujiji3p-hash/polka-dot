#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polka Dot Beauty - Main Application Entry Point
Version: 1.0
"""

from app import create_app, db
from app.models import User, Product, Category, Preorder, Announcement
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Category': Category,
        'Preorder': Preorder,
        'Announcement': Announcement
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

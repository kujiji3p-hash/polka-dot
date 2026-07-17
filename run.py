#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polka Dot Beauty - Main Application Entry Point
Version: 1.0
"""

from app import create_app, db

app = create_app()

# Автоматически создаём таблицы при запуске
with app.app_context():
    db.create_all()
    print("✅ Таблицы проверены/созданы")

if __name__ == '__main__':
    app.run()

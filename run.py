from app import create_app, db
from app.models import Category, Product, Announcement

# Импортируем функцию seed_data
from products import seed_data

app = create_app()

with app.app_context():
    db.create_all()

    # Запускаем добавление демо-данных
    seed_data()

if __name__ == '__main__':
    app.run()
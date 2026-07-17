from app import create_app, db
from app.models import Category, Product, Announcement

app = create_app()

with app.app_context():
    # Категории
    if not Category.query.first():
        forms = Category(name='Формы', slug='forms', description='Многоразовые верхние формы', sort_order=1)
        gels = Category(name='Гели', slug='gels', description='Профессиональные гели', sort_order=2)
        db.session.add_all([forms, gels])
        db.session.commit()
        print('✅ Категории созданы')

    # Продукты
    if not Product.query.first():
        p1 = Product(
            name='Salon Square',
            slug='salon-square',
            short_desc='Верхние формы. 140 шт.',
            description='Верхние многоразовые формы из PMMA. Салонный квадрат. 140 шт (14 размеров по 10 шт).',
            price=1290,
            sku='PD-SS-001',
            material='PMMA',
            package_contents='140 шт (14 размеров по 10 шт)',
            weight='15 г',
            country='Китай',
            status='active',
            is_featured=True,
            stock_quantity=100,
            category_id=1
        )
        p2 = Product(
            name='Гель для наращивания',
            slug='gel-dlya-narashchivaniya',
            short_desc='Розовый, 15 мл.',
            description='Розовый гель для моделирования и укрепления ногтей.',
            price=890,
            sku='PD-GN-001',
            composition='Acrylates Copolymer, Hydroxypropyl Methacrylate...',
            volume='15 мл',
            color='розовый',
            action='моделирование; укрепление',
            shelf_life='3 года; 12 месяцев после вскрытия',
            country='Россия',
            weight='15 г',
            package_contents='тюбик с гелем',
            status='active',
            stock_quantity=50,
            category_id=2
        )
        db.session.add_all([p1, p2])
        db.session.commit()
        print('✅ Продукты созданы')

    # Анонсы
    if not Announcement.query.first():
        a1 = Announcement(
            title='Запуск линейки Salon Square',
            slug='zapusk-salon-square',
            short_desc='Верхние многоразовые формы уже в продаже!',
            content='Верхние многоразовые формы из PMMA уже в продаже. 14 размеров, профессиональное качество.',
            status='published',
            is_featured=True
        )
        db.session.add(a1)
        db.session.commit()
        print('✅ Анонсы созданы')

    print('🎉 Все данные добавлены!')
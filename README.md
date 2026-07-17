# Polka Dot v1.0

Профессиональный сайт для бьюти-бренда **Polka Dot** — многоразовые верхние формы и гели для мастеров ногтевого сервиса.

## 🎨 Фирменный стиль

- **Паттерн**: Яркие polka dots (точки) на фоне
- **Цвета**: Чёрно-белая палитра + акцент #ff0066 для предзаказа
- **Шрифт**: Montserrat
- **Минимализм**: Чистые формы, много воздуха

## 📁 Структура проекта

```
polka_dot_ver_1.0/
├── app/                    # Flask приложение
│   ├── static/
│   │   ├── css/           # Стили (polka_dot_style.css)
│   │   ├── js/            # Скрипты (polka_dot_app.js)
│   │   └── images/        # Изображения
│   ├── templates/         # HTML шаблоны (Jinja2)
│   │   ├── layout.html    # Базовый шаблон
│   │   ├── index.html     # Главная
│   │   ├── products.html  # Каталог
│   │   ├── product_detail.html
│   │   ├── preorder.html  # Предзаказ
│   │   ├── announcements.html
│   │   ├── about.html
│   │   ├── contact.html
│   │   └── admin/         # Админ-панель
│   ├── main/              # Публичные маршруты
│   ├── admin/             # Админ маршруты
│   ├── api/               # REST API
│   ├── models.py          # SQLAlchemy модели
│   └── __init__.py        # Application factory
├── database/
│   ├── create_tables.sql   # Создание БД PostgreSQL
│   ├── seed_data.sql       # Демо-данные
│   └── setup_dbeaver.md   # Инструкция DBeaver
├── migrations/            # Flask-Migrate
├── config.py              # Конфигурация
├── run.py                 # Точка входа
├── requirements.txt       # Зависимости
└── .env.example           # Шаблон переменных окружения
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
```

### 2. Настройка базы данных (DBeaver)

1. Установите PostgreSQL
2. Создайте базу `polka_dot_db`
3. В DBeaver выполните `database/create_tables.sql`
4. Скопируйте `.env.example` → `.env` и укажите данные БД

### 3. Запуск

```bash
# Инициализация миграций (первый раз)
flask db init
flask db migrate
flask db upgrade

# Запуск сервера
python run.py
```

Сайт будет доступен по адресу: **http://localhost:5000**

## 🔐 Админ-панель

- URL: `/admin/`
- Логин: `admin`
- Пароль: `admin123` (измените в production!)

## 📊 Модели данных

| Модель | Описание |
|--------|----------|
| **User** | Администраторы |
| **Category** | Категории (Формы, Гели) |
| **Product** | Продукты с характеристиками |
| **Preorder** | Предзаказы клиентов |
| **Announcement** | Анонсы и новости |
| **SiteSettings** | Настройки сайта |

## 🛠 Технологии

- **Backend**: Python 3.12 + Flask
- **ORM**: SQLAlchemy + Flask-Migrate
- **Database**: PostgreSQL (DBeaver)
- **Frontend**: HTML5 + CSS3 + Vanilla JS
- **Шаблонизатор**: Jinja2
- **Стили**: Кастомный CSS (без фреймворков)

## 📄 Лицензия

© 2026 Polka Dot. Все права защищены.

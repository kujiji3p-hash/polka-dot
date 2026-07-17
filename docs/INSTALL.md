# Руководство по установке Polka Dot v1.0

## Системные требования

- Windows 10/11, macOS или Linux
- Python 3.10+
- PostgreSQL 14+
- DBeaver (рекомендуется для управления БД)

## Шаг 1: Установка Python зависимостей

```bash
# Перейдите в папку проекта
cd polka_dot_ver_1.0

# Создайте виртуальное окружение
python -m venv venv

# Активируйте
venv\Scripts\activate          # Windows
source venv/bin/activate         # Mac/Linux

# Установите зависимости
pip install -r requirements.txt
```

## Шаг 2: Установка PostgreSQL

### Windows:
1. Скачайте с [postgresql.org](https://www.postgresql.org/download/windows/)
2. Запустите установщик
3. Запомните пароль для пользователя `postgres`
4. Убедитесь, что порт 5432 свободен

### Проверка установки:
```bash
psql --version
```

## Шаг 3: Создание базы данных

### Через командную строку:
```bash
psql -U postgres
CREATE DATABASE polka_dot_db;
\q
```

### Через DBeaver:
1. Создайте подключение к PostgreSQL
2. Правый клик → Create New Database
3. Название: `polka_dot_db`

## Шаг 4: Создание таблиц

1. Откройте DBeaver
2. Подключитесь к `polka_dot_db`
3. Откройте SQL Editor
4. Выполните файл `database/create_tables.sql`
5. Проверьте созданные таблицы

## Шаг 5: Настройка окружения

```bash
# Скопируйте шаблон
cp .env.example .env

# Отредактируйте .env в текстовом редакторе
```

Пример `.env`:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

DATABASE_URL=postgresql://postgres:ВАШ_ПАРОЛЬ@localhost:5432/polka_dot_db
DB_PASSWORD=ВАШ_ПАРОЛЬ

ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

## Шаг 6: Инициализация Flask-Migrate

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Шаг 7: Запуск

```bash
python run.py
```

Откройте браузер: **http://localhost:5000**

## Шаг 8: Доступ к админ-панели

1. Перейдите на `/admin/`
2. Войдите с данными из `.env`
3. Управляйте продуктами, предзаказами и анонсами

## Устранение неполадок

### Ошибка: "ModuleNotFoundError"
```bash
# Убедитесь, что виртуальное окружение активировано
venv\Scripts\activate
pip install -r requirements.txt
```

### Ошибка: "Connection refused" (PostgreSQL)
```bash
# Проверьте, запущен ли PostgreSQL
# Windows: Services → postgresql-x64 → Start
# Linux: sudo service postgresql start
```

### Ошибка: "database does not exist"
```bash
psql -U postgres -c "CREATE DATABASE polka_dot_db;"
```

## Обновление

```bash
git pull              # если используете git
pip install -r requirements.txt --upgrade
flask db upgrade
```

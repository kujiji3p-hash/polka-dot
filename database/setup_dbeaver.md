# Настройка базы данных Polka Dot в DBeaver

## Шаг 1: Установка PostgreSQL

1. Скачайте PostgreSQL с [postgresql.org](https://www.postgresql.org/download/)
2. Установите с паролем для пользователя `postgres` (запомните его!)
3. Убедитесь, что сервер запущен

## Шаг 2: Создание базы данных

```sql
CREATE DATABASE polka_dot_db;
CREATE USER polka_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE polka_dot_db TO polka_user;
```

## Шаг 3: Подключение в DBeaver

1. Откройте DBeaver
2. **Database → New Database Connection → PostgreSQL**
3. Заполните поля:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `polka_dot_db`
   - **Username**: `postgres` (или `polka_user`)
   - **Password**: ваш пароль
4. Нажмите **Test Connection**, затем **Finish**

## Шаг 4: Создание таблиц

1. В DBeaver откройте SQL Editor (Ctrl+]` или правый клик на БД → SQL Editor)
2. Откройте файл `database/create_tables.sql`
3. Нажмите **Execute Script** (Alt+X)
4. Проверьте, что таблицы созданы:
   ```sql
   SELECT table_name FROM information_schema.tables 
   WHERE table_schema = 'public' ORDER BY table_name;
   ```

## Шаг 5: Дополнительные данные (опционально)

```sql
-- Выполните seed_data.sql для демо-данных
\i database/seed_data.sql
```

## Шаг 6: Настройка .env

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:
```
DATABASE_URL=postgresql://postgres:ВАШ_ПАРОЛЬ@localhost:5432/polka_dot_db
DB_PASSWORD=ВАШ_ПАРОЛЬ
```

## Структура базы данных

| Таблица | Описание |
|---------|----------|
| `users` | Администраторы |
| `categories` | Категории продуктов |
| `products` | Продукты (формы, гели) |
| `preorders` | Предзаказы клиентов |
| `announcements` | Анонсы и новости |
| `site_settings` | Настройки сайта |

## Полезные SQL запросы

```sql
-- Все продукты с категориями
SELECT p.name, p.price, c.name as category, p.status
FROM products p
LEFT JOIN categories c ON p.category_id = c.id;

-- Предзаказы с информацией о продукте
SELECT pr.customer_name, pr.customer_phone, p.name as product, pr.status
FROM preorders pr
LEFT JOIN products p ON pr.product_id = p.id;

-- Статистика
SELECT status, COUNT(*) FROM products GROUP BY status;
```

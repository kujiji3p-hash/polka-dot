# Polka Dot API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### GET /api/products
Получить список продуктов

**Query Parameters:**
- `category` — фильтр по категории (forms, gels)
- `status` — фильтр по статусу (active, preorder, coming_soon)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Salon Square",
      "slug": "salon-square",
      "price": "1290.00",
      "status": "active"
    }
  ]
}
```

### GET /api/categories
Получить список категорий

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Формы",
      "slug": "forms"
    }
  ]
}
```

### GET /api/announcements
Получить список анонсов

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Запуск линейки Salon Square",
      "slug": "zapusk-salon-square",
      "event_date": "2026-07-01"
    }
  ]
}
```

## Админ API (через формы)

### POST /admin/product/new
Создать новый продукт

**Form Data:**
- `name` — название
- `slug` — URL-идентификатор
- `price` — цена
- `category_id` — ID категории
- `status` — статус (active, preorder, etc.)

### POST /preorder/submit
Оформить предзаказ

**Form Data:**
- `name` — имя клиента
- `phone` — телефон
- `email` — email (опционально)
- `product_id` — ID продукта
- `quantity` — количество
- `comment` — комментарий (опционально)

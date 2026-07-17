-- ============================================
-- POLKA DOT v1.0 — Database Schema
-- For PostgreSQL (DBeaver)
-- Run this script in DBeaver SQL Editor
-- ============================================

-- Drop tables if exist (for clean setup)
DROP TABLE IF EXISTS preorders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS announcements CASCADE;
DROP TABLE IF EXISTS site_settings CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================
-- TABLE: users (Admin accounts)
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);

-- ============================================
-- TABLE: categories (Product categories)
-- ============================================
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    slug VARCHAR(64) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(128),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_active ON categories(is_active);

-- ============================================
-- TABLE: products (Forms, Gels, etc.)
-- ============================================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    slug VARCHAR(128) NOT NULL UNIQUE,
    description TEXT,
    short_desc VARCHAR(256),

    -- Pricing
    price NUMERIC(10, 2) NOT NULL,
    old_price NUMERIC(10, 2),

    -- Product details (from your images)
    sku VARCHAR(64) UNIQUE,
    composition TEXT,           -- Состав
    volume VARCHAR(32),         -- Объем
    color VARCHAR(32),          -- Цвет
    action VARCHAR(128),        -- Действие
    shelf_life VARCHAR(64),     -- Срок годности
    country VARCHAR(64),        -- Страна производства
    material VARCHAR(64),       -- Материал
    package_contents VARCHAR(256), -- Комплектация
    weight VARCHAR(32),         -- Вес

    -- Images
    image_main VARCHAR(256),
    image_gallery JSONB,

    -- Status
    status VARCHAR(32) DEFAULT 'active',  -- active, preorder, coming_soon, archived
    stock_quantity INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT FALSE,

    -- Foreign keys
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_featured ON products(is_featured);
CREATE INDEX idx_products_category ON products(category_id);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON products 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- TABLE: preorders
-- ============================================
CREATE TABLE preorders (
    id SERIAL PRIMARY KEY,

    -- Customer info
    customer_name VARCHAR(128) NOT NULL,
    customer_phone VARCHAR(32) NOT NULL,
    customer_email VARCHAR(120),
    customer_comment TEXT,

    -- Order details
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    quantity INTEGER DEFAULT 1,

    -- Status
    status VARCHAR(32) DEFAULT 'pending',  -- pending, confirmed, paid, shipped, cancelled

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_preorders_status ON preorders(status);
CREATE INDEX idx_preorders_product ON preorders(product_id);

CREATE TRIGGER update_preorders_updated_at 
    BEFORE UPDATE ON preorders 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- TABLE: announcements
-- ============================================
CREATE TABLE announcements (
    id SERIAL PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    slug VARCHAR(256) NOT NULL UNIQUE,
    content TEXT,
    short_desc VARCHAR(512),

    -- Timeline
    event_date DATE,
    is_featured BOOLEAN DEFAULT FALSE,

    -- Media
    image VARCHAR(256),

    -- Status
    status VARCHAR(32) DEFAULT 'draft',  -- draft, published, archived

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

CREATE INDEX idx_announcements_slug ON announcements(slug);
CREATE INDEX idx_announcements_status ON announcements(status);
CREATE INDEX idx_announcements_date ON announcements(event_date);

-- ============================================
-- TABLE: site_settings
-- ============================================
CREATE TABLE site_settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(64) NOT NULL UNIQUE,
    value TEXT,
    description VARCHAR(256)
);

-- ============================================
-- INITIAL DATA
-- ============================================

-- Default admin user (password: admin123 — change in production!)
-- Password hash generated with werkzeug.security.generate_password_hash('admin123')
INSERT INTO users (username, email, password_hash, is_admin) 
VALUES ('admin', 'admin@polkadot.ru', 
        'pbkdf2:sha256:600000$...', 
        TRUE);

-- Categories
INSERT INTO categories (name, slug, description, sort_order) VALUES
('Формы', 'forms', 'Многоразовые верхние формы для наращивания ногтей', 1),
('Гели', 'gels', 'Профессиональные гели для моделирования и укрепления', 2);

-- Demo products
INSERT INTO products (name, slug, description, short_desc, price, old_price, sku, 
    composition, volume, color, action, shelf_life, country, material, package_contents, weight,
    status, stock_quantity, is_featured, category_id) 
VALUES 
('Salon Square', 'salon-square', 
 'Верхние многоразовые формы из PMMA. Салонный квадрат. Профессиональное качество для мастеров ногтевого сервиса.',
 'Верхние многоразовые формы. PMMA. 140 шт.',
 1290.00, NULL, 'PD-SS-001',
 'полиметилметакрилат (ПММА)', NULL, NULL, NULL, NULL, 'Китай', 'пластик', 
 '140 шт (14 размеров по 10 шт)', '15 г',
 'active', 100, TRUE, 1),

('Прозрачные формы', 'prozrachnye-formy',
 'Прозрачные верхние формы для наращивания. Идеальная видимость при работе.',
 'Прозрачные верхние формы. 140 шт.',
 1190.00, NULL, 'PD-PF-001',
 NULL, NULL, 'прозрачный', NULL, NULL, 'Китай', 'пластик',
 '140 шт (14 размеров по 10 шт)', '15 г',
 'active', 80, FALSE, 1),

('Гель для наращивания', 'gel-dlya-narashchivaniya',
 'Розовый гель для моделирования и укрепления ногтей. Профессиональная формула.',
 'Розовый, моделирование и укрепление. 15 мл.',
 890.00, NULL, 'PD-GN-001',
 'Acrylates Copolymer, Hydroxypropyl Methacrylate, Dimethicone, Microcrystalline Wax, Mica, CI 77491, CI 7492, CI 7891, CI 77007, CI 77266, Ethyl Trimethylbenzoyl Phenylphosphinate',
 '15 мл', 'розовый', 'моделирование; укрепление', '3 года; 12 месяцев после вскрытия', 'Россия', NULL,
 'тюбик с полигелем для наращивания', '15 г',
 'active', 50, TRUE, 2),

('Базовый гель', 'bazovyj-gel',
 'Прозрачный базовый гель для укрепления ногтей. Отличная адгезия.',
 'Прозрачный, укрепление. 15 мл.',
 750.00, NULL, 'PD-BG-001',
 NULL, '15 мл', 'прозрачный', 'укрепление', NULL, NULL, NULL, NULL, '15 г',
 'active', 60, FALSE, 2);

-- Demo announcements
INSERT INTO announcements (title, slug, short_desc, content, event_date, status, is_featured) VALUES
('Запуск линейки Salon Square', 'zapusk-salon-square',
 'Верхние многоразовые формы из PMMA уже в продаже.',
 'Верхние многоразовые формы из PMMA уже в продаже. 14 размеров, профессиональное качество.',
 '2026-07-01', 'published', TRUE),

('Новая линейка гелей', 'novaya-linejka-gelej',
 'Расширение ассортимента гелей: базовые, моделирующие, цветные.',
 'Расширение ассортимента гелей: базовые, моделирующие, цветные. Формула с улучшенной адгезией.',
 '2026-08-01', 'published', FALSE),

('Salon Square Pro', 'salon-square-pro',
 'Улучшенные формы с усиленным креплением. Предзаказ открыт.',
 'Улучшенные формы с усиленным креплением и маркировкой размеров. Предзаказ открыт.',
 '2026-09-01', 'published', TRUE),

('Обучающие материалы', 'obuchayushie-materialy',
 'Видео-уроки и мастер-классы по работе с формами и гелями.',
 'Видео-уроки и мастер-классы по работе с формами и гелями Polka Dot.',
 '2026-10-01', 'published', FALSE);

-- Site settings
INSERT INTO site_settings (key, value, description) VALUES
('site_name', 'Polka Dot', 'Название сайта'),
('site_description', 'Профессиональные бьюти-продукты', 'Описание сайта'),
('contact_email', 'info@polkadot.ru', 'Контактный email'),
('contact_phone', '+7 (999) 123-45-67', 'Контактный телефон'),
('version', 'polka_dot_ver_1.0', 'Версия системы');

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'Tables created successfully!' AS status;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;

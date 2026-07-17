-- ============================================
-- POLKA DOT v1.0 — Additional Seed Data
-- ============================================

-- Preorder products
INSERT INTO products (name, slug, description, short_desc, price, old_price, sku,
    material, package_contents, status, stock_quantity, category_id)
VALUES
('Salon Square Pro', 'salon-square-pro',
 'Улучшенные формы с усиленным креплением. Профессиональное качество.',
 'Улучшенные формы с усиленным креплением.',
 1266.00, 1490.00, 'PD-SSP-001',
 'PMMA', '140 шт (14 размеров по 10 шт)', 'preorder', 0, 1),

('Premium Gel Set', 'premium-gel-set',
 'Набор из 3 гелей: база, моделирование, топ.',
 'Набор из 3 гелей. База, моделирование, топ.',
 2117.00, 2490.00, 'PD-PGS-001',
 NULL, '3 x 15 мл', 'preorder', 0, 2);

-- More announcements
INSERT INTO announcements (title, slug, short_desc, event_date, status, is_featured)
VALUES
('Черная пятница 2026', 'chernaya-pyatnitsa-2026',
 'Большие скидки на всю линейку продуктов.',
 '2026-11-27', 'draft', FALSE),

('Новогодняя коллекция', 'novogodnyaya-kollekciya',
 'Праздничные наборы и подарочная упаковка.',
 '2026-12-01', 'draft', FALSE);

SELECT 'Seed data inserted!' AS status;

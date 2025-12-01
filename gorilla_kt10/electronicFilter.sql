SELECT DISTINCT
    o.order_id,
    o.customer_id,
    o.order_date
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
WHERE cat.category_name = 'Электроника'
ORDER BY o.order_date;
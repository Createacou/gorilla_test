SELECT 
    c.customer_id,
    c.name,
    SUM(oi.quantity * oi.price_at_time) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE 
    EXTRACT(YEAR FROM o.order_date) = EXTRACT(YEAR FROM CURRENT_DATE)
    AND EXTRACT(MONTH FROM o.order_date) = EXTRACT(MONTH FROM CURRENT_DATE)
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
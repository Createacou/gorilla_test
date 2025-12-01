SELECT 
    p.product_id,
    p.name,
    p.price,
    c.category_name
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN (
    SELECT 
        category_id,
        AVG(price) AS avg_price
    FROM products
    GROUP BY category_id
) cat_avg ON p.category_id = cat_avg.category_id
WHERE p.price > cat_avg.avg_price
ORDER BY p.price ASC;
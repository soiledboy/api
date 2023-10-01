my_query = """


WITH product_cte AS (
    SELECT
        id,
        name,
        number,
        rarity,
        imageUrl,
        COUNT(*) OVER () AS row_count
    FROM products
    WHERE number = %s AND (products.rarity = %s OR %s IS NULL)
),


single_product_cte AS (
    SELECT id
    FROM product_cte
    WHERE row_count = 1
),

price_data AS (
    WITH ranked_prices AS (
        SELECT
            prices.market,
            prices.Product_id,
            products.name,
            products.number,
            products.rarity,
            products.imageUrl,
            products.tcgUrl,
            prices.date::date,
            prices.Sub_type,
            DENSE_RANK() OVER (ORDER BY
                CASE
                    WHEN prices.Sub_type = '1st Edition' THEN 1
                    WHEN prices.Sub_type = 'Unlimited' THEN 2
                    WHEN prices.Sub_type = 'Limited' THEN 3
                    ELSE 9999
                END ASC) AS priority_rank
        FROM prices
        INNER JOIN single_product_cte ON prices.Product_id = single_product_cte.id
        INNER JOIN products ON prices.Product_id = products.id
        WHERE date >= %s AND (products.rarity = %s OR %s IS NULL)
    )
    SELECT *
    FROM ranked_prices
    WHERE priority_rank = 1
)


-- If single product matches
SELECT
    market::text AS market,
    price_data.number,
    Product_id::text AS Product_id,
    name,
    rarity,
    imageUrl,
    tcgUrl,
    date,
    Sub_type
FROM price_data

UNION ALL

-- If multiple products match
SELECT
    NULL::text AS market,       -- Setting market to NULL
    product_cte.number,
    NULL::text AS Product_id,  -- Setting Product_id to NULL
    name,                      -- Keeping name as is
    rarity,                    -- Keeping rarity as is
    NULL::text AS imageUrl,    -- Setting imageUrl to NULL
    NULL::text AS tcgUrl,      -- Setting tcgUrl to NULL
    NULL::date AS date,
    NULL::text AS Sub_type
FROM product_cte
WHERE row_count > 1

ORDER BY date ASC, Product_id ASC;


"""


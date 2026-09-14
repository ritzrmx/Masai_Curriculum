-- ============================================================================
-- IITPGenAITAI2606 | Module 2: SQL for Data Analysis
-- PHASE 1 DATABASE — Sessions 4.2, 4.3, 5.1, 5.2
-- (SQL Query Basics · Sorting and Filtering · Aggregation Essentials ·
--  Grouping for KPIs)
-- ============================================================================
-- Every SQL snippet quoted in these four lecture scripts and pre-reads uses
-- a single table literally named `orders`, with customer_name and city
-- stored directly on each order row (this is BEFORE the normalization
-- story introduced in Session 6.1). Run any query from those four
-- sessions' scripts against this `orders` table exactly as written —
-- every exact number quoted in those scripts was calculated against
-- precisely these 4 rows.
--
-- A second table, `orders_extended` (15 rows), is provided ONLY for the
-- open-ended "fuller/larger table" Practical Block activities in Sessions
-- 9 (SQL Query Basics) and 10 (Sorting and Filtering) — those activities
-- ask students to explore a bigger table but do not quote a specific
-- expected result, so there's no conflict using this separate table for
-- them. Do not substitute `orders_extended` into a query that a script
-- quotes an exact number for — use `orders` for that.
-- ============================================================================

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS orders_extended;

-- ----------------------------------------------------------------------------
-- `orders` — THE table every exact quoted number in Sessions 4.2/4.3/5.1/5.2
-- was calculated against. Do not add or remove rows from this table.
-- ----------------------------------------------------------------------------
CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY,
    customer_name  TEXT NOT NULL,
    city           TEXT NOT NULL,
    item           TEXT NOT NULL,
    quantity       INTEGER NOT NULL,
    price          INTEGER NOT NULL,   -- price in rupees (whole units)
    order_date     TEXT NOT NULL       -- ISO format: YYYY-MM-DD
);

INSERT INTO orders (order_id, customer_name, city, item, quantity, price, order_date) VALUES
    (1, 'Ramesh', 'Bengaluru', 'Veg Thali',     2, 120, '2026-08-01'),
    (2, 'Fatima', 'Hyderabad', 'Non-Veg Thali', 1, 150, '2026-08-01'),
    (3, 'Arjun',  'Bengaluru', 'Veg Thali',     1, 120, '2026-08-02'),
    (4, 'Priya',  'Chennai',   'Mini Thali',    3,  90, '2026-08-02');

-- ----------------------------------------------------------------------------
-- `orders_extended` — 15 rows, for exploratory Practical Block use only
-- (Session 9's "larger orders table (15-20 rows)" activity and Session 10's
-- "fuller 15-20 row orders table" multi-column sort activity). No script
-- quotes an exact expected number against this specific table.
-- ----------------------------------------------------------------------------
CREATE TABLE orders_extended (
    order_id       INTEGER PRIMARY KEY,
    customer_name  TEXT NOT NULL,
    city           TEXT NOT NULL,
    item           TEXT NOT NULL,
    quantity       INTEGER NOT NULL,
    price          INTEGER NOT NULL,
    order_date     TEXT NOT NULL
);

INSERT INTO orders_extended SELECT * FROM orders;

INSERT INTO orders_extended (order_id, customer_name, city, item, quantity, price, order_date) VALUES
    (5,  'Ramesh',  'Bengaluru', 'Mini Thali',    1,  90, '2026-08-03'),
    (6,  'Fatima',  'Hyderabad', 'Veg Thali',     2, 120, '2026-08-03'),
    (7,  'Arjun',   'Bengaluru', 'Non-Veg Thali', 1, 150, '2026-08-04'),
    (8,  'Priya',   'Chennai',   'Veg Thali',     2, 120, '2026-08-04'),
    (9,  'Karthik', 'Bengaluru', 'Mini Thali',    1,  90, '2026-08-05'),
    (10, 'Ramesh',  'Bengaluru', 'Veg Thali',     1, 120, '2026-08-06'),
    (11, 'Fatima',  'Hyderabad', 'Mini Thali',    2,  90, '2026-08-06'),
    (12, 'Priya',   'Chennai',   'Non-Veg Thali', 1, 150, '2026-08-07'),
    (13, 'Arjun',   'Bengaluru', 'Mini Thali',    2, 180, '2026-08-07'),
    (14, 'Fatima',  'Hyderabad', 'Non-Veg Thali', 1, 150, '2026-08-08'),
    (15, 'Karthik', 'Bengaluru', 'Veg Thali',     1, 120, '2026-08-08');

-- ============================================================================
-- SANITY CHECKS — every one of these reproduces an exact number quoted in
-- the Session 4.2/4.3/5.1/5.2 lecture scripts. Safe to run, read-only.
-- ============================================================================
-- Session 9 (SQL Query Basics):
--   SELECT * FROM orders;                              -> 4 rows
--   SELECT customer_name, item FROM orders
--     WHERE item = 'Veg Thali' AND item = 'Mini Thali'; -> 0 rows (the AND/OR trap)
--
-- Session 10 (Sorting and Filtering in SQL):
--   SELECT customer_name, price FROM orders ORDER BY price ASC;
--     -> Priya 90, Ramesh 120, Arjun 120, Fatima 150
--   SELECT customer_name, price FROM orders
--     WHERE city='Bengaluru' ORDER BY price DESC LIMIT 3;
--     -> Ramesh 120, Arjun 120 (only 2 Bengaluru rows exist in the core table)
--
-- Session 11 (Aggregation Essentials):
--   SELECT SUM(price), AVG(price) FROM orders;          -> 480, 120.0
--   SELECT MIN(price), MAX(price) FROM orders;           -> 90, 150
--   SELECT COUNT(*), SUM(price) FROM orders
--     WHERE city='Bengaluru';                            -> 2, 240
--
-- Session 12 (Grouping for KPIs):
--   SELECT city, COUNT(*) FROM orders GROUP BY city;
--     -> Bengaluru 2, Chennai 1, Hyderabad 1
--   SELECT city, SUM(price) FROM orders
--     GROUP BY city HAVING SUM(price) > 100;
--     -> Bengaluru 240, Hyderabad 150 (Chennai's 90 dropped)
-- ============================================================================

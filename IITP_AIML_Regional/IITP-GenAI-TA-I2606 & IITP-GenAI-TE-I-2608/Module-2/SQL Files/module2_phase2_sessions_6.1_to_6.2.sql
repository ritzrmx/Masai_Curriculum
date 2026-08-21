-- ============================================================================
-- IITPGenAITAI2606 | Module 2: SQL for Data Analysis
-- PHASE 2 DATABASE — Sessions 6.1, 6.2
-- (Joining Tables Together · Insights from Combined Data)
-- ============================================================================
-- Starting in Session 13 (Joining Tables Together), the story deliberately
-- normalizes the data: customer_name and city move OUT of `orders` and into
-- a new `customers` table, linked by `customer_id`. This is a DIFFERENT
-- schema for `orders` than Phase 1's — do not run Session 13/14 queries
-- against the Phase 1 database, and do not run Session 9-12 queries against
-- this one; the `orders` table means something different in each phase,
-- exactly as the module's narrative intends ("Where did the customer's
-- city go?").
--
-- Every exact number quoted in the Session 13 and 14 lecture scripts and
-- pre-reads was calculated against precisely the rows below.
-- ============================================================================

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customer_addresses;
DROP TABLE IF EXISTS customers;

-- ----------------------------------------------------------------------------
-- `customers` — one row per customer. Karthik (id 5) deliberately has NO
-- matching orders — he's the running example for LEFT JOIN and the
-- "customers who never ordered" business question.
-- ----------------------------------------------------------------------------
CREATE TABLE customers (
    customer_id    INTEGER PRIMARY KEY,
    customer_name  TEXT NOT NULL,
    city           TEXT NOT NULL,
    loyalty_tier   TEXT NOT NULL CHECK (loyalty_tier IN ('Gold', 'Silver', 'Bronze'))
);

INSERT INTO customers (customer_id, customer_name, city, loyalty_tier) VALUES
    (1, 'Ramesh',  'Bengaluru', 'Gold'),
    (2, 'Fatima',  'Hyderabad', 'Silver'),
    (3, 'Arjun',   'Bengaluru', 'Silver'),
    (4, 'Priya',   'Chennai',   'Gold'),
    (5, 'Karthik', 'Bengaluru', 'Bronze');  -- signed up, has NO orders

-- ----------------------------------------------------------------------------
-- `orders` — normalized version. Links to customers via customer_id.
-- NOTE: this schema is deliberately different from Phase 1's `orders` table
-- (no customer_name/city columns here — see header note above).
-- ----------------------------------------------------------------------------
CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY,
    customer_id    INTEGER NOT NULL REFERENCES customers(customer_id),
    item           TEXT NOT NULL,
    quantity       INTEGER NOT NULL,
    price          INTEGER NOT NULL,
    order_date     TEXT NOT NULL
);

INSERT INTO orders (order_id, customer_id, item, quantity, price, order_date) VALUES
    (1, 1, 'Veg Thali',     2, 120, '2026-08-01'),  -- Ramesh
    (2, 2, 'Non-Veg Thali', 1, 150, '2026-08-01'),  -- Fatima
    (3, 3, 'Veg Thali',     1, 120, '2026-08-02'),  -- Arjun
    (4, 4, 'Mini Thali',    3,  90, '2026-08-02');  -- Priya
    -- customer_id 5 (Karthik) intentionally has zero rows here.

-- ----------------------------------------------------------------------------
-- `customer_addresses` — Session 14's join fan-out demonstration table.
-- Ramesh (customer_id 1) has TWO saved addresses; everyone else has one.
-- Joining orders -> customer_addresses duplicates Ramesh's single order.
-- ----------------------------------------------------------------------------
CREATE TABLE customer_addresses (
    customer_id    INTEGER NOT NULL REFERENCES customers(customer_id),
    address_label  TEXT NOT NULL
);

INSERT INTO customer_addresses (customer_id, address_label) VALUES
    (1, 'Home'),
    (1, 'Office'),   -- Ramesh's second address -> causes the fan-out
    (2, 'Home'),
    (3, 'Home'),
    (4, 'Home');

-- ============================================================================
-- SANITY CHECKS — every one of these reproduces an exact number quoted in
-- the Session 13/14 lecture scripts. Safe to run, read-only.
-- ============================================================================
-- Session 13 (Joining Tables Together):
--   SELECT orders.order_id, customers.customer_name, orders.item, orders.price
--   FROM orders INNER JOIN customers
--     ON orders.customer_id = customers.customer_id;
--     -> 4 rows (Ramesh, Fatima, Arjun, Priya) — Karthik excluded
--
--   SELECT customers.customer_name, orders.item, orders.price
--   FROM customers LEFT JOIN orders
--     ON customers.customer_id = orders.customer_id;
--     -> 5 rows — Karthik included, with NULL item/price
--
--   SELECT customers.loyalty_tier, SUM(orders.price) AS total_revenue
--   FROM customers INNER JOIN orders
--     ON customers.customer_id = orders.customer_id
--   GROUP BY customers.loyalty_tier ORDER BY total_revenue DESC;
--     -> Silver 270, Gold 210
--
-- Session 14 (Insights from Combined Data):
--   SELECT orders.order_id, orders.price, customer_addresses.address_label
--   FROM orders INNER JOIN customer_addresses
--     ON orders.customer_id = customer_addresses.customer_id
--   WHERE orders.customer_id = 1;
--     -> 2 rows, both price=120 (Home, Office) -> naive SUM = 240
--   SELECT SUM(price) FROM orders WHERE customer_id = 1;
--     -> 120 (Ramesh's real, undistorted total)
-- ============================================================================

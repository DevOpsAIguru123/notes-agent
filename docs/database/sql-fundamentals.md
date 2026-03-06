# SQL Fundamentals

## Basic Queries

```sql
-- Select with filtering
SELECT name, email, created_at
FROM users
WHERE active = true AND age >= 18
ORDER BY created_at DESC
LIMIT 20;

-- Aggregations
SELECT department, COUNT(*) as headcount, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC;

-- Insert
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- Update
UPDATE users SET active = false WHERE last_login < '2025-01-01';

-- Delete
DELETE FROM orders WHERE status = 'cancelled' AND created_at < '2024-01-01';
```

## Joins

```sql
-- INNER JOIN - only matching rows
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN - all users, even without orders
SELECT u.name, COALESCE(SUM(o.total), 0) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.name;

-- Self join - employees with their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

## Subqueries & CTEs

```sql
-- Subquery
SELECT name FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 100);

-- CTE (Common Table Expression) - more readable
WITH high_spenders AS (
    SELECT user_id, SUM(total) as total_spent
    FROM orders
    GROUP BY user_id
    HAVING SUM(total) > 1000
)
SELECT u.name, hs.total_spent
FROM users u
JOIN high_spenders hs ON u.id = hs.user_id;
```

## Window Functions

```sql
-- Rank employees by salary within each department
SELECT
    name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as overall_rank
FROM employees;

-- Running total
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;
```

## Indexing

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (column order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Partial index (PostgreSQL)
CREATE INDEX idx_active_users ON users(email) WHERE active = true;
```

!!! tip "Index Tips"
    - Index columns used in `WHERE`, `JOIN`, and `ORDER BY`
    - Composite index order should match query patterns
    - Don't over-index — each index slows down writes
    - Use `EXPLAIN ANALYZE` to verify indexes are being used

## Transactions

```sql
BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- If anything fails, ROLLBACK undoes all changes
```

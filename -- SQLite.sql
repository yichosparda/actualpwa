-- SQLite

-- CREATE TABLE products(
--     product_ID INTEGER PRIMARY KEY,
--     product_name TEXT NOT NULL,
--     stock INT CHECK(stock >= 0),
--     price DECIMAL NOT NULL,
--     type TEXT NOT NULL
-- );

-- INSERT INTO products(product_name,stock,price, type)
-- VALUES ('donuts', 30, 7, 'other'),
--     ('berry_delight',30,12.94,'other'),
--     ('muffins',30,6, 'other'),
--     ('eggtart',30, 8, 'other');

-- DROP TABLE products;

UPDATE products SET product_name='Pecan Pie' WHERE product_ID=9;
UPDATE products SET product_name='Chocolate Chip Cookies' WHERE product_ID=16;


-- 3. CREATE THE CHILD TABLE WITH FOREIGN KEY REFERENCE
-- CREATE TABLE employees (
--     emp_id INTEGER PRIMARY KEY,
--     emp_name TEXT NOT NULL,
--     department_id INTEGER,
--     -- Establishes the relationship line
--     FOREIGN KEY (department_id) REFERENCES (dept_id)
-- );
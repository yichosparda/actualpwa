-- SQLite

-- CREATE TABLE items(
--     product TEXT NOT NULL,
--     variant TEXT DEFAULT 'N/A',
--     stock INT CHECK(stock >= 0),
--     price DECIMAL NOT NULL
-- );

INSERT INTO items(product,variant, stock, price)
VALUES('cheesecake','N/A',20, 90.50),
    ('cheesecake','gluten_free',10, 110.75),
    ('cheesecake','dairy_free',10, 102)

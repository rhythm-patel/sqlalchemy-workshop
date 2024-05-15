DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;

CREATE TABLE IF NOT EXISTS item (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    price DECIMAL NOT NULL,
    description VARCHAR
);

CREATE TABLE IF NOT EXISTS address (
    id INTEGER NOT NULL PRIMARY KEY,
    flat_number INTEGER NOT NULL,
    post_code INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS customer (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    address_id INTEGER NOT NULL REFERENCES address (id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER NOT NULL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customer (id),
    order_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER NOT NULL REFERENCES orders (id),
    item_id INTEGER NOT NULL REFERENCES item (id),
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, item_id)
);

-- Insert sample data

INSERT INTO item (name, price, description) VALUES ('Milk', 5, '1L bottle of milk');
INSERT INTO item (name, price, description) VALUES ('Kit Kat', 1, 'a chocolate');
INSERT INTO item (name, price, description) VALUES ('Bread', 10.5, 'a loaf of bread');
INSERT INTO item (name, price, description) VALUES ('Onion', 2, 'an onion');

INSERT INTO address (flat_number, post_code) VALUES (101, 10001);
INSERT INTO address (flat_number, post_code) VALUES (201, 10002);
INSERT INTO address (flat_number, post_code) VALUES (301, 10003);

INSERT INTO customer (name, address_id) VALUES ('Alex', 1);
INSERT INTO customer (name, address_id) VALUES ('Blake', 2);
INSERT INTO customer (name, address_id) VALUES ('Cam', 3);

INSERT INTO orders (customer_id, order_time) VALUES (1, '2024-03-18 10:30:00');
INSERT INTO orders (customer_id, order_time) VALUES (3, '2024-03-20 11:00:00');
INSERT INTO orders (customer_id, order_time) VALUES (2, '2024-03-25 15:00:00');

INSERT INTO order_items (order_id, item_id, quantity) VALUES (1, 2, 4);
INSERT INTO order_items (order_id, item_id, quantity) VALUES (1, 3, 2);
INSERT INTO order_items (order_id, item_id, quantity) VALUES (1, 1, 1);
INSERT INTO order_items (order_id, item_id, quantity) VALUES (2, 2, 2);
INSERT INTO order_items (order_id, item_id, quantity) VALUES (2, 4, 5);

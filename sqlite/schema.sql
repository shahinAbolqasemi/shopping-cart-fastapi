CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                hashed_password TEXT NOT NULL,
                UNIQUE(username)
);

CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id),
                UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS product_cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                cart_id INTEGER NOT NULL,
                FOREIGN KEY (cart_id) REFERENCES cart(id)
);

INSERT INTO user (username, hashed_password)
VALUES
    ('admin', '$2b$12$gXfDXmHJLbaNAplMEefA9Oi0nt6tSjrFDafXpz8BFkx71YIYaYPyS'),
    ('test', '$2b$12$gXfDXmHJLbaNAplMEefA9Oi0nt6tSjrFDafXpz8BFkx71YIYaYPyS');

INSERT INTO cart (user_id)
VALUES
    (1),
    (2);
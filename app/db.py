import sqlite3

from app.models import UserInDB
from app.utils import get_logger
from app.config import ROOT_DIR

logger = get_logger(__name__)


def init_db():
    if (ROOT_DIR / 'sqlite' / 'db.sqlite3').exists():
        logger.info("Database already exists")
    else:
        connection = sqlite3.connect(str(ROOT_DIR / 'sqlite' / 'db.sqlite3'))
        cursor = connection.cursor()
        with open(ROOT_DIR / 'schema.sql', 'r') as f:
            cursor.executescript(f.read())
        connection.commit()
        connection.close()
        logger.debug('Database initialized')


def get_users():
    connection = sqlite3.connect(ROOT_DIR / 'sqlite' / 'db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username, hashed_password FROM user
    """)
    users = cursor.fetchall()
    connection.close()
    return list(map(lambda user: {'username': user[0], 'hashed_password': user[1]}, users))


def get_user(username):
    connection = sqlite3.connect(ROOT_DIR / 'sqlite' / 'db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username, hashed_password FROM user
        WHERE username = ?
    """, (username,))
    user = cursor.fetchone()
    connection.close()
    return UserInDB(username=user[0], hashed_password=user[1])


def get_cart_item(username):
    connection = sqlite3.connect(ROOT_DIR / 'sqlite' / 'db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT product_id, count(*) FROM cart as c
            join user as u
            join product_cart as pc
            on c.id = pc.cart_id and u.id = c.user_id
            where username=?
            group by pc.product_id
    """, (username,))
    cart_item = cursor.fetchall()
    connection.close()
    return list(cart_item)


def get_cart_by_username(username):
    connection = sqlite3.connect(ROOT_DIR / 'sqlite' / 'db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id FROM cart
        WHERE user_id = (SELECT id FROM user WHERE username = ?)
    """, (username,))
    cart = cursor.fetchone()
    connection.close()
    return {'id': cart[0]}


def add_to_cart(product_id, cart_id):
    connection = sqlite3.connect(ROOT_DIR / 'sqlite' / 'db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO product_cart (product_id, cart_id)
        VALUES 
            (?, ?)
    """, (product_id, cart_id))
    connection.commit()
    connection.close()


if __name__ == '__main__':
    init_db()

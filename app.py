import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me'
DATABASE = 'inventory.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'name TEXT NOT NULL, quantity INTEGER NOT NULL, price REAL NOT NULL)'
    )
    conn.execute(
        'CREATE TABLE IF NOT EXISTS orders ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'item_id INTEGER NOT NULL,'
        'quantity INTEGER NOT NULL,'
        'status TEXT NOT NULL,'
        'FOREIGN KEY(item_id) REFERENCES items(id)'
        ')'
    )
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)',
            (name, quantity, price)
        )
        conn.commit()
        conn.close()
        flash('Item added successfully.')
        return redirect(url_for('index'))
    return render_template('add_item.html')


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    if not item:
        conn.close()
        flash('Item not found.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        conn.execute(
            'UPDATE items SET name = ?, quantity = ?, price = ? WHERE id = ?',
            (name, quantity, price, item_id)
        )
        conn.commit()
        conn.close()
        flash('Item updated successfully.')
        return redirect(url_for('index'))
    conn.close()
    return render_template('edit_item.html', item=item)


@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    flash('Item deleted successfully.')
    return redirect(url_for('index'))


@app.route('/orders')
def orders():
    conn = get_db_connection()
    orders = conn.execute(
        'SELECT orders.id, orders.quantity, orders.status, items.name as item_name '
        'FROM orders JOIN items ON orders.item_id = items.id'
    ).fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)


@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = int(request.form['quantity'])
        item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
        if not item:
            flash('Item not found.')
            conn.close()
            return redirect(url_for('add_order'))
        if quantity > item['quantity']:
            flash('Insufficient inventory for this order.')
            conn.close()
            return redirect(url_for('add_order'))
        conn.execute(
            'INSERT INTO orders (item_id, quantity, status) VALUES (?, ?, ?)',
            (item_id, quantity, 'Processing')
        )
        conn.commit()
        conn.close()
        flash('Order placed successfully.')
        return redirect(url_for('orders'))
    conn.close()
    return render_template('add_order.html', items=items)


@app.route('/orders/ship/<int:order_id>')
def ship_order(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    if not order or order['status'] == 'Shipped':
        conn.close()
        flash('Order not found or already shipped.')
        return redirect(url_for('orders'))
    item = conn.execute('SELECT * FROM items WHERE id = ?', (order['item_id'],)).fetchone()
    if order['quantity'] > item['quantity']:
        conn.close()
        flash('Not enough inventory to ship this order.')
        return redirect(url_for('orders'))
    conn.execute('UPDATE items SET quantity = quantity - ? WHERE id = ?', (order['quantity'], order['item_id']))
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', ('Shipped', order_id))
    conn.commit()
    conn.close()
    flash('Order shipped.')
    return redirect(url_for('orders'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

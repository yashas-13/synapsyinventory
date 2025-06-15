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


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

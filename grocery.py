from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('grocery.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    menu_items = conn.execute('SELECT * FROM menu').fetchall()
    wishlist_items = conn.execute('SELECT * FROM wishlist').fetchall()
    purchased_items = conn.execute('SELECT * FROM purchased').fetchall()
    conn.close()
    return render_template('index.html', menu_items=menu_items, wishlist_items=wishlist_items, purchased_items=purchased_items)

@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    name = request.form['name']
    price = request.form['price']
    conn = get_db_connection()
    conn.execute('INSERT INTO wishlist (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/purchase_item/<int:item_id>')
def purchase_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM wishlist WHERE id = ?', (item_id,)).fetchone()
    if item:
        conn.execute('INSERT INTO purchased (name, price) VALUES (?, ?)', (item['name'], item['price']))
        conn.execute('DELETE FROM wishlist WHERE id = ?', (item_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/remove_wishlist_item/<int:item_id>')
def remove_wishlist_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM wishlist WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/remove_purchased_item/<int:item_id>')
def remove_purchased_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM purchased WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

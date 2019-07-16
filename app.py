from flask import Flask, render_template, redirect, url_for, request

import db

DATABASE_URL = 'db.sqlite'

app = Flask(__name__)


@app.route('/')
def index():
    alcoshops = db.get_list(DATABASE_URL)
    return render_template('index.html', alcoshops=alcoshops)

@app.route('/<id>', methods=['GET', 'POST'])
def alcoshop_details(id):
    alcoshop = db.search_shop_by_id(DATABASE_URL, id)
    return render_template('alcoshop-details.html', alcoshop=alcoshop)

@app.route('/new', methods=['GET', 'POST'])
def alcoshop_new():
    return render_template('alcoshop-add.html')

@app.route('/new/add', methods=['POST'])
def alcoshop_add():
    name = request.form['name']
    adress = request.form['adress']
    coordinate = request.form['coordinate']
    rating = request.form['rating']
    alcoshop = db.add_alcoshop(DATABASE_URL, name, adress, coordinate, rating)
    return redirect(url_for('alcoshop_details', id=alcoshop))


@app.route('/<id>/edit', methods=['POST'])
def alcoshop_edit(id):
    alcoshop = db.search_shop_by_id(DATABASE_URL, id)
    return render_template('alcoshop-edit.html', alcoshop=alcoshop)

@app.route('/<id>/save', methods=['POST'])
def save_edit(id):
    name = request.form['name']
    adress = request.form['adress']
    coordinate = request.form['coordinate']
    rating = request.form['rating']
    alcoshop = db.update_alcoshop(DATABASE_URL, id, name, adress, coordinate, rating)
    return redirect(url_for('alcoshop_details', id=alcoshop))

@app.route('/search', methods=['POST'])
def shop_search():
    search = request.form.get("search")
    results = db.search_shop(DATABASE_URL, search)
    return render_template('alcoshop-search.html', alcoshops=results, search=search)


@app.route('/<id>/delete', methods=['POST'])
def delete_shop(id):
    db.delete_by_id(DATABASE_URL, id)
    alcoshops = db.get_list(DATABASE_URL)
    return render_template('index.html', alcoshops=alcoshops)
    # return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

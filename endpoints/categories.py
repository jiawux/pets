from flask import request
from flask_restplus import Resource
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import Category, PetSchema
from flask import Flask, request, jsonify, flash, url_for, redirect, render_template

ns = api.namespace('/category', description='Operations related to categories')

pets_schema = PetSchema(many=True)

@app.route('/', methods=['GET','POST'])
def add_category():
    error=None
    if request.method == 'POST':

        category_name=request.form.get('category_name')

        try:
            if category_name is not None:
                new_category = Category(category_name)

                db.session.add(new_category)
                db.session.commit()

                return redirect(url_for('home_page', pets = Pet.query.all(),
                    categories = Category.query.all()))
            else:
                error = "invalid category_name"
                return render_template('category.html', categories = Category.query.all(), error=error)
        except InvalidRequestError as e:
             return render_template('category.html', categories = Category.query.all(),
                error = "Invalid entries. Try again.")
        except IntegrityError as e:
             return render_template("pet.html", categories = Category.query.all(),
                error = "Entries must be unique. Try again.")

    return render_template('category.html', categories = Category.query.all())

@app.route('/delete/<category_name>', methods=['GET','DELETE'])
def delete_category(category_name):

    delete_category = Category.query.filter_by(category_name=category_name).first()
    db.session.delete(delete_category)
    db.session.commit()

    return '''<h3>
                 <a href = '{}'">Home Page</a>
              </h3>
              <h3>Deleted Category {}'''.format(url_for('home_page',
              pets = Pet.query.all(), categories = Category.query.all()), category_name)

# endpoint to update user
@app.route('/update/<category_name>', methods=['GET','POST'])
def update_category(category_name):

    if request.method == 'POST':

        category = Category.query.filter_by(category_name=category_name).first()
        category_name=request.form.get('category_name')

        try:
            if category_name!="":
                category.category_name = category_name

                updated_category = category_schema.dump(category).data
                db.session.commit()

                return redirect(url_for('home_page', pets = Pet.query.all(),
                    categories = Category.query.all()))
            else:
                return render_template('category.html', categories=Category.query.all(),
                    error = "Please fill out the input fields.")
        except IntegrityError as e:
             return render_template('category.html', categories = Category.query.all(),
                error = "Entries must be unique. Try again.")

    return render_template('category.html', categories = Category.query.all())

# endpoint to show all pets with specific category
@app.route('/pet_by_category/<category_name>', methods=['GET'])
def get_all_pets_by_category(category_name):
    category = Category.query.filter_by(category_name=category_name).first()
    pets = category.pets

    return jsonify(pets_schema.dump(pets).data)

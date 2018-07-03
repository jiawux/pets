from flask import request
from flask_restplus import Resource
from flask import request
from flask_restplus import Resource
from rest_api_demo.api.restplus import api
from pets_api.database.models import Pet
from flask import Flask, request, jsonify, flash, url_for, redirect, render_template

ns = api.namespace('/pet', description='Operations related to pets')


# endpoint to add a new pet
@app.route('/', methods=['GET','POST'])
def pet():
    if request.method == "POST":

        pet_name = request.form.get('pet_name')
        photoUrls = request.form.get('photoUrls')
        status = request.form.get('status')
        category = request.form.get('category')


        pet_category = Category.query.filter_by(category_name=category).first()

        if pet_name=='':
            return render_template("pet.html", categories = Category.query.all(),
                error = "Please fill out the name field.")

        try:
            new_pet = Pet(pet_name, photoUrls, status)

            if (len(pet_category_data.keys()) > 0):
                print("we got hERE")
                pet_category.pets.append(new_pet)

            db.session.add(new_pet)
            db.session.commit()

            return redirect(url_for('home_page', pets = Pet.query.all(),
             categories = Category.query.all()))

        except IntegrityError as e:
             return render_template("pet.html", categories = Category.query.all(),
                error = "Entries must be unique. Try again.")

    return render_template("pet.html", categories = Category.query.all())

@app.route('/delete/<int:pet_id>', methods=['GET','DELETE'])
def delete_pet(pet_id):

    pet = Pet.query.get(pet_id)
    db.session.delete(pet)
    db.session.commit()

    return '''<h3>
                 <a href = '{}'">Home Page</a>
              </h3>
              <h3>Deleted Pet {}'''.format(url_for('home_page',
              pets = Pet.query.all(), categories = Category.query.all()), pet_id)


# endpoint to update user
@app.route('/update/<int:pet_id>', methods=['GET','POST'])
def update_pet(pet_id):


    if request.method == 'POST':
        pet = Pet.query.get(pet_id)

        pet_name = request.form.get('pet_name')
        photoUrls = request.form.get('photoUrls')
        status = request.form.get('status')
        delta = request.form.get('type of category change')
        category_name = request.form.get('category')

        if pet_name != "":
            pet.pet_name = pet_name

        if photoUrls != "":
            pet.photoUrls = photoUrls

        if status != pet.status:
            pet.status = status

        new_category = Category.query.filter_by(category_name=category_name).first()
        if delta == 'add':
            new_category.pets.append(pet)
        elif delta == 'delete':
            if pet in new_category.pets:
                new_category.pets.remove(pet)

        db.session.commit()
        return redirect(url_for('home_page', pets = Pet.query.all(),
         categories = Category.query.all()))

    return render_template("update_pet.html", categories = Category.query.all())

@app.route('/home')
def home_page():
   return render_template('home_page.html', pets = Pet.query.all(),
    categories = Category.query.all())

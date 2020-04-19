from flask import Flask
from flask import render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
#import secrets
import os 


dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')



#conn ="mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class omoeller_pokemon(db.Model):
    pokemon_no = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String(100))
    pokemon_type01 = db.Column(db.String(25))
    pokemon_type02 = db.Column(db.String(25))
    pokemon_evolves_at = db.Column(db.Integer)
    pokemon_post_evolve = db.Column(db.String(100))


class pokemonForm(FlaskForm):
    pokemon_no = IntegerField('Pokemon No:')
    pokemon_name = StringField('Pokemon Name:', validators=[DataRequired()])
    pokemon_type01 = StringField('Type 1:', validators=[DataRequired()])
    pokemon_type02 = StringField('Type 2:')
    pokemon_evolves_at = StringField('Evolves At:')
    pokemon_post_evolve =StringField('Post - Evolution:')


@app.route('/')
def index():
    all_pokemon = omoeller_pokemon.query.all()
    return render_template('index.html', pokemon=all_pokemon, pageTitle='Pokemon List')

@app.route('/add_pokemon', methods=['GET','POST'])
def add_pokemon():
    form = pokemonForm()
    if form.validate_on_submit():
        pokemon = omoeller_pokemon(pokemon_name = form.pokemon_name.data, pokemon_type01 = form.pokemon_type01.data, pokemon_type02 = form.pokemon_type02.data, 
                                   pokemon_evolves_at = form.pokemon_evolves_at.data, pokemon_post_evolve = form.pokemon_post_evolve.data)
        db.session.add(pokemon)
        db.session.commit()
        return redirect('/')
    
    return render_template("add_pokemon.html", form = form, pageTitle ='Pokemon List Homepage')

@app.route('/delete_pokemon/<int:pokemon_no>', methods=['GET', 'POST'])
def delete_pokemon(pokemon_no):
    if request.method == 'POST':
        pokemon = omoeller_pokemon.query.get_or_404(pokemon_no)
        db.session.delete(pokemon)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")

@app.route('/pokemon/<int:pokemon_no>', methods=['GET','POST'])
def get_pokemon(pokemon_no):
    pokemon = omoeller_pokemon.query.get_or_404(pokemon_no)
    return render_template('pokemon.html', form = pokemon, pageTitle='Pokemon', legend = 'Pokemon')


@app.route('/pokemon/<int:pokemon_no>/update', methods=['GET','POST'])
def update_pokemon(pokemon_no):
    pokemon = omoeller_pokemon.querey.get_or_404(pokemon_no)
    form = pokemonForm()

    if form.validate_on_submit():
        pokemon.pokemon_name = form.pokemon_name.data
        pokemon.pokemon_type01 = form.pokemon_type01.data    
        pokemon.pokemon_type02 = form.pokemon_type02.data
        pokemon.pokemon_evolves_at = form.pokemon_evolves_at.data
        pokemon.pokemon_post_evolve = form.pokemon_post_evolve.data
        db.session.commit()
        return redirect(url_for('get_pokemon', pokemon_no = pokemon.pokemon_no))
    form.pokemon_name.data = pokemon.pokemon_name
    form.pokemon_type01.data = pokemon.pokemon_type01
    form.pokemon_type02.data = pokemon.pokemon_type02
    form.pokemon_evolves_at.data = pokemon.pokemon_evolves_at
    form.pokemon_post_evolve.data = pokemon.pokemon_post_evolve
    return render_template('update_pokemon.html', form = form, pageTitle = 'Update Pokemon', legend ='Update A Pokemon')

@app.route('/search', methods={'GET', 'POST'})
def search():
    if request.method =='POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = omoeller_pokemon.query.filter(or_(omoeller_pokemon.pokemon_name.like(search),
                                                        omoeller_pokemon.pokemon_type01.like(search),
                                                        omoeller_pokemon.pokemon_type02.like(search))).all()
        return render_template('index.html', pokemon=results, pageTitle="Pokemon", legend = "Search Results")
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

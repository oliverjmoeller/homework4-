from flask import Flask
from flask import render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import validate_on_submit

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

if __name__ == '__main__':
    app.run(debug=True)

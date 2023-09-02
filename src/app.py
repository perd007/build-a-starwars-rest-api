"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

 #obtenemos todos los usuarios   
@app.route('/user', methods=['GET'])
def get_user():
    users= User.query.all()
    serialized_user= [user.serialize() for user in users]
    if not serialized_user:
        return jsonify({"error": "users not found"})
    
    return jsonify(serialized_user), 200

#obtenemos usuario por id
@app.route('/user/<int:id>', methods=['GET'])
def get_user_id(id):
    user=User.query.get(id)
    if not user:
        return jsonify({"error": "user not found"}), 404 
        
    return jsonify(user.serialize())

#insertamos usuarios a la BD
@app.route('/user', methods=['POST'])
def insert_user():
    data= request.get_json()
    data_name = data.get("name", None)
    data_last_name= data.get("last_name", None)
    data_email= data.get("email", None)
    data_password= data.get("password", None)
    data_date_sus= data.get("date_sus", None)

    new_user= User(name=data_name, last_name=data_last_name, email=data_email, 
                   password=data_password, date_sus=data_date_sus)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201

    except Exception as error:
        db. session.rollback()
        return error, 500

#modificacmos a nuestro usuario
@app.route('/user/<int:id>', methods=['PUT'])
def modify_user(id):

    data = request.get_json()
    data_name = data.get("name", None)
    data_last_name= data.get("last_name", None)
    data_email= data.get("email", None)
    data_password= data.get("password", None)
    data_date_sus= data.get("date_sus", None)
   
    user_to_edit = User.query.get(id)

    if not user_to_edit:
        return jsonify({"error": "user not found"}), 404

    # modificamos los valores de los personajes
    user_to_edit.name = data_name
    user_to_edit.last_name = data_last_name
    user_to_edit.email = data_email
    user_to_edit.password = data_password
    user_to_edit.date_sus= data_date_sus

    try:
        db.session.commit()
        return jsonify({"character":user_to_edit.serialize()}), 200

    except Exception as error:
        db.session.rollback()
        return error

#eliminamos por ip a nuestro usuario
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user_by_id(id):
    # Buscar el personaje en la bbdd
    user_to_delete = User.query.get(id)
    if not user_to_delete:
        return jsonify({'error': 'User not found'}), 404

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify("user deleted successfully"), 200
    except Exception as error:
        db.session.rollback()
        return error

#obtenemos todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets=Planet.query.all()
    if not planets:
        return jsonify({"error": "planets not found"}), 404
    serialized_planets= [planet.serialize() for planet in planets]

    return jsonify(serialized_planets), 200

#obtenemos el planeta por id
@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_id(id):
    planet=Planet.query.get(id)
    if not planet:
        return jsonify({"error": "planet not found"}), 404
    return jsonify(planet.serialize()), 200

#insertamos planetas en la BD
@app.route('/planets', methods=['POST'])
def insert_planet():
    data= request.get_json()
    data_name = data.get("name", None)
    data_population= data.get("population", None)
    data_rotation_period= data.get("rotation_period", None)
    data_orbital_period= data.get("orbital_period", None)
    data_diameter= data.get("diameter", None)
    data_climate= data.get("climate", None)
    data_gravity= data.get("gravity", None)
    data_terrain= data.get("terrain", None)
    data_surface_water= data.get("surface_water", None)
    
    new_planet= Planet(name=data_name, population=data_population, 
                       rotation_period=data_rotation_period, orbital_period=data_orbital_period,
                        diameter=data_diameter, climate=data_climate, terrain=data_terrain,
                       surface_water=data_surface_water, gravity=data_gravity)

    try:
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 201
        
    except Exception as error:
        db.session.rollback()
        return error

#modificamos nuestro planeta
@app.route('/planets/<int:id>', methods=['PUT'])
def modify_planet(id):
    data= request.get_json();  
    data_name = data.get("name", None)
    data_population= data.get("population", None)
    data_rotation_period= data.get("rotation_period", None)
    data_orbital_period= data.get("orbital_period", None)
    data_diameter= data.get("diameter", None)
    data_climate= data.get("climate", None)
    data_gravity= data.get("gravity", None)
    data_terrain= data.get("terrain", None)
    data_surface_water= data.get("surface_water", None)
    
    planet_to_edit = Planet.query.get(id)

    # si el personaje no existe termina la funcion con un 404
    if not planet_to_edit:
        return jsonify({"error": "Planet not found"}), 404
    
    planet_to_edit.name= data_name 
    planet_to_edit.population=data_population
    planet_to_edit.rotation_period=data_rotation_period
    planet_to_edit.orbital_period=data_orbital_period
    planet_to_edit.diameter=data_diameter
    planet_to_edit.climate=data_climate
    planet_to_edit.gravity=data_gravity
    planet_to_edit.terrain= data_terrain
    planet_to_edit.surface_water=data_surface_water

    try:
        db.session.commit()
        return jsonify({"Planet": planet_to_edit.serialize()}), 200

    except Exception as error:
        db.session.rollback()
        return error
    
#eliminamos el planeta
@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet_by_id(id):
    # Buscar el personaje en la bbdd
    planet_to_delete = Planet.query.get(id)
    if not planet_to_delete:
        return jsonify({'error': 'Planet not found'}), 404

    try:
        db.session.delete(planet_to_delete)
        db.session.commit()
        return jsonify("planet deleted successfully"), 200
    except Exception as error:
        db.session.rollback()
        return error
    

#obtenemos los personajes
@app.route('/people', methods=['GET'])
def get_people():
    people=People.query.all()
    if not people:
        return jsonify({"error": "people not found"}), 404
    serialized_people= [person.serialize() for person in people]

    return jsonify(serialized_people)


#obtenemos los personajes por id
@app.route('/people/<int:id>', methods=['GET'])
def get_people_id(id):
    person=People.query.get(id)
    if not person:
        return jsonify({"error": "people not found"}), 404
    
    return jsonify(person.serialize()), 200


#insertamos personajes en la BD
@app.route('/people', methods=['POST'])
def insert_person():
    data= request.get_json()
    data_name= data.get("name", None)
    data_height= data.get("height", None)
    data_mass= data.get("mass", None)
    data_hair_color= data.get("hair_color", None)
    data_skin_color=data.get("skin_color", None)
    data_eye_color=data.get("eye_color", None)
    data_birth_year= data.get("birth_year", None)
    data_gender= data.get("gender", None)
    data_planet_id= data.get("planet_id", None)
    
    new_person= People(name=data_name, height=data_height, mass=data_mass, hair_color=data_hair_color,
                    skin_color=data_skin_color, eye_color=data_eye_color, birth_year=data_birth_year,
                    gender=data_gender, planet_id=data_planet_id)

    try:
        db.session.add(new_person)
        db.session.commit()
        return jsonify(new_person.serialize()), 201
        
    except Exception as error:
        db.session.rollback()
        return error
    

#modificamos personajes
@app.route('/people/<int:id>', methods=['PUT'])
def edit_people_id(id):
  
    data = request.get_json()
    data_name= data.get("name", None)
    data_height= data.get("height", None)
    data_mass= data.get("mass", None)
    data_hair_color= data.get("hair_color", None)
    data_skin_color=data.get("skin_color", None)
    data_eye_color=data.get("eye_color", None)
    data_birth_year= data.get("birth_year", None)
    data_gender= data.get("gender", None)
    data_planet_id= data.get("planet_id", None)

    people_id=People.query.get(id)
   
    if not people_id:
        return jsonify({"error": "Person not found"}), 404
    
    people_id.name=data_name
    people_id.height=data_height
    people_id.mass=data_mass
    people_id.hair_color=data_hair_color
    people_id.skin_color=data_skin_color
    people_id.eye_color=data_eye_color
    people_id.birth_year=data_birth_year
    people_id.gender=data_gender
    people_id.planet_id= data_planet_id

    try:
        db.session.commit()
        return jsonify({"person": people_id.serialize()}), 200

    except Exception as error:
        db.session.rollback()
        return error

#eliminamos al personaje
@app.route('/people/<int:id>', methods=['DELETE'])
def delete_person_by_id(id):
    # Buscar el personaje en la bbdd
    person_to_delete = People.query.get(id)
    if not person_to_delete:
        return jsonify({'error': 'Person not found'}), 404

    try:

        db.session.delete(person_to_delete)
        db.session.commit()
        return jsonify("person deleted successfully"), 200
    
    except Exception as error:
        db.session.rollback()
        return error

#consultamos favoritos
@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites=Favorites.query.all()
    if not favorites:
        return jsonify({"error": "favorites not found"}), 404
    serialized_favorites= [favorite.serialize() for favorite in favorites]

    return jsonify( serialized_favorites)

#consultamos favoritos por usuario
@app.route('/favorite/user/<int:user_id>', methods=['GET'])
def get_favorites_user(user_id):
    favorites=Favorites.query.filter_by(user_id=user_id).all()
    if not favorites:
        return jsonify({"error": "favorites not found"}), 404
    
    serialized_favorites= [favorite.serialize() for favorite in favorites]
    return jsonify( serialized_favorites)

#insertamos en la tabla favoritos el planeta
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def insert_favorites_planet(planet_id):
    data = request.get_json()
    user_id=  data.get("user_id", None)

    user=User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    
    planet=Planet.query.get(planet_id)
    if not planet:
          return jsonify({'error': 'planet not found'}), 404
    
    favorite_exist= Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite_exist:
         return jsonify({"error": "Ya existe el favorito del usuario con el planeta"}), 400
    
    favorite= Favorites(user_id=user_id, planet_id=planet_id)
    try:
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"New Favorite": favorite.serialize()}), 201
  
    except Exception as error:
        db.session.rollback()
        return error

#eliminamos el favorito del planeta
@app.route('/favorite/planet/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_planet_by_id(favorite_id):
    # Buscar el personaje en la bbdd
    favorite_to_delete = Favorites.query.get(favorite_id)
    if not favorite_to_delete:
        return jsonify({'error': 'Planet Favorite not found'}), 404

    try:

        db.session.delete(favorite_to_delete)
        db.session.commit()
        return jsonify("Favorite Planet deleted successfully"), 200
    
    except Exception as error:
        db.session.rollback()
        return error

#insertamos en la tabla favoritos el personaje
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def insert_favorites_people(people_id):
    data = request.get_json()
    user_id=  data.get("user_id", None)

    user=User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    
    person=People.query.get(people_id)
    if not  person:
          return jsonify({'error': 'person not found'}), 404
    
    favorite_exist= Favorites.query.filter_by(user_id=user_id, id=people_id).first()
    if favorite_exist:
         return jsonify({"error": "Ya existe el favorito del usuario con el personaje"}), 400
    
    favorite= Favorites(user_id=user_id, people_id=people_id)
    try:
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"New Favorite": favorite.serialize()}), 201
  
    except Exception as error:
        db.session.rollback()
        return error
    
#eliminamos el favorito del personaje
@app.route('/favorite/people/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_people_by_id(favorite_id):
    # Buscar el personaje en la bbdd
    favorite_to_delete = Favorites.query.get(favorite_id)
    if not favorite_to_delete:
        return jsonify({'error': 'Person Favorite not found'}), 404

    try:

        db.session.delete(favorite_to_delete)
        db.session.commit()
        return jsonify("Favorite Person deleted successfully"), 200
    
    except Exception as error:
        db.session.rollback()
        return error
#
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

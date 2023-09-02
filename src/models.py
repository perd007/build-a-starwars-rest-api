from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name=db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), nullable=False)
    password= db.Column(db.String(20), nullable=False)
    date_sus=db.Column(db.String(20),nullable=False)
    favorites= db.relationship("Favorites", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "date_sus": self.email
            
        }


class Planet(db.Model):
    __tablename__= "planet"
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50),nullable=True)
    population= db.Column(db.Integer, nullable=True)
    rotation_period= db.Column(db.Integer,nullable=False)
    orbital_period= db.Column(db.Integer,nullable=False)
    diameter= db.Column(db.Integer,nullable=False)
    climate= db.Column(db.String(50),nullable=False)
    gravity= db.Column(db.String(50),nullable=False)
    terrain= db.Column(db.String(50),nullable=False)
    surface_water= db.Column(db.Integer,nullable=False)
    people_id= db.relationship("People", backref="planet", lazy=True)
    favorities= db.relationship("Favorites", backref="planet", lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }


class People(db.Model):
    __tablename__= "people"
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50),nullable=False)
    height= db.Column(db.Integer,nullable=False)
    mass= db.Column(db.Integer,nullable=True)
    hair_color= db.Column(db.String(50),nullable=True)
    skin_color= db.Column(db.String(50),nullable=True)
    eye_color= db.Column(db.String(50),nullable=False)
    birth_year= db.Column(db.String(50),nullable=False)
    gender= db.Column(db.String(50),nullable=False)
    planet_id= db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)
    favorities= db.relationship("Favorites", backref="people", lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "planet_id": self.planet_id          
        }
  

class Favorites(db.Model):
    __tablename__='favorites'
    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id= db.Column(db.Integer,db.ForeignKey("planet.id"), nullable=True)
    people_id= db.Column(db.Integer, db.ForeignKey("people.id"),nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id":  self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id

        }
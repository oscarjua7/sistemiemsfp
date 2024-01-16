from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from database import Database
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import relationship, deferred

class Alumnos(Database):
    __tablename__ ='alumnos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    estatus = Column(Integer)
    folio = Column(String(30))
    curp = Column(String(50))
    carrera = Column(String(50))
    domicilio = Column(String(500))
    correo = Column(String(300))
    telefono = Column(String(10))
    sexo = Column(Integer)
    fecha_inscripcion = Column(Date)

class Docentes(Database):
    __tablename__ ='docentes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    folio = Column(String(30))
    periodocontrato = Column(String(50))
    correo = Column(String(50))
    telefono = Column(String(10))
    domicilio = Column(String(500))

class Usuarios(Database):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nom_user =Column(String(100))
    user_ingreso =Column(String(100))
    
class Carreras(Database):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(54))

class Grupos(Database):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(54))
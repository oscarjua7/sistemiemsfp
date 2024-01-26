from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from database import Database
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import relationship, deferred
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import DateTime

class Alumnos(Database):
    __tablename__ ='alumnos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    estatus = Column(Integer)
    folio = Column(String(30))
    curp = Column(String(50))
    domicilio = Column(String(500))
    correo = Column(String(300))
    telefono = Column(String(10))
    sexo = Column(Integer)
    fecha_inscripcion = Column(Date)

    grupo_id = Column(Integer, ForeignKey('grupos.id'))
    grupo = relationship("Grupos")

class Grupos(Database):
    __tablename__ = 'grupos'

    id = Column(Integer, primary_key=True)
    clave = Column(String(5))
    
    carrera_id = Column(Integer, ForeignKey('carreras.id'))
    carrera = relationship("Carreras")
    
    cuatrimestre_id = Column(Integer, ForeignKey('cuatrimestres.id'))
    cuatrimestre = relationship("Cuatrimestres")
    
class Materias(Database):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True)
    nombre_materia = Column(String(100))
    
    carrera_id = Column(Integer, ForeignKey('carreras.id'))
    carrera = relationship("Carreras")
    
    cuatrimestre_id = Column(Integer, ForeignKey('cuatrimestres.id'))
    cuatrimestre = relationship("Cuatrimestres")
                                                                                                        
class Carreras(Database):
    __tablename__ = 'carreras'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(54))
    rvoe = Column(String(10))

class Docentes(Database):
    __tablename__ ='docentes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    folio = Column(String(30))
    carrera = Column(String(50))
    periodocontratoini = Column(DateTime)
    periodocontratofin = Column(DateTime)
    correo = Column(String(50))
    telefono = Column(String(10))
    domicilio = Column(String(500))
    
class Personal(Database):
    __tablename__ ='personal'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    folio = Column(String(30))
    puesto = Column(String(50))
    periodocontratoini = Column(DateTime)
    periodocontratofin = Column(DateTime)
    correo = Column(String(50))
    telefono = Column(String(10))
    domicilio = Column(String(500))

class Cuatrimestres(Database):
    __tablename__ = 'cuatrimestres'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(54))
    
class Usuarios(Database):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nom_user = Column(String(100))
    user_ingreso_hashed = Column(String(128))  # Almacena la contraseña encriptada

    def set_password(self, password):
        self.user_ingreso_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_ingreso_hashed, password)
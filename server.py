import os
import uuid
import re
import models
import shutil
import tempfile
from io import BytesIO
from time import time
from datetime import datetime
from flask import Flask, session
from math import ceil
from functools import wraps

from flask_session import Session
from flask import flash
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template, make_response, send_file, after_this_request
from flask_sslify import SSLify

from datetime import date

from sqlalchemy import or_
from sqlalchemy import and_
from database import engine
from database import Database
from database import db_session

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from sqlalchemy import func

from validate_email_address import validate_email
import re
import models

app= Flask(__name__)
sslify = SSLify(app)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

Session(app)
Database.metadata.create_all(engine)

# Ruta de la base de datos SQLite3
DATABASE_PATH = 'IEMSFP.db'

def backup_database():
    try:
        # Crear un directorio temporal para el respaldo
        backup_dir = tempfile.mkdtemp()
        # Nombre del archivo de respaldo
        backup_filename = 'respaldo.db'
        # Ruta completa del archivo de respaldo
        backup_filepath = os.path.join(backup_dir, backup_filename)

        # Copiar la base de datos al directorio temporal
        shutil.copy(DATABASE_PATH, backup_filepath)

        # Devolver la ruta del archivo de respaldo
        return backup_filepath
    except Exception as e:
        print(f"Error al respaldar la base de datos: {e}")
        return None

def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return route_function(*args, **kwargs)
    return wrapper

@app.get("/")
def home():
    return render_template ('login.html')

@app.route('/respaldo')
def respaldo():
    backup_filepath = backup_database()

    if backup_filepath:
        @after_this_request
        def remove_temporary_file(response):
            try:
                os.remove(backup_filepath)
            except Exception as error:
                print(f"Error al eliminar el archivo temporal: {error}")
            return response

        # Devuelve el archivo para descargar
        return send_file(backup_filepath, as_attachment=True, download_name='respaldo.db', mimetype='application/x-sqlite3')
    else:
        return "Error al realizar el respaldo de la base de datos"

@app.get("/panel_principal")
def panel_principal():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))

    # Contador para el modelo de alumnos
    alumnos = db_session.query(models.Alumnos)
    total_records_alumn = alumnos.count()

    # Contador para el modelo de docentes
    docentes = db_session.query(models.Docentes)
    total_records_docen = docentes.count()

    # Contador para el modelo de personal
    personal = db_session.query(models.Personal)
    total_records_per = personal.count()

    # Contador para el modelo de usuarios
    usuarios = db_session.query(models.Carreras)
    total_records_carreras = usuarios.count()

    return render_template('index.html',
        alumnos=alumnos,
        total_records_alumn=total_records_alumn,
        docentes=docentes,
        total_records_docen=total_records_docen,
        personal=personal,
        total_records_per=total_records_per,
        usuarios=usuarios,
        total_records_carreras=total_records_carreras,
        models=models,
        and_=and_,
    )

@app.get('/reportes_sexo')
def reportes_sexo():
    
    alumnos = db_session.query(models.Alumnos)

    return render_template('reportes/grafica_sexo.html',
        alumnos=alumnos,
        models=models,
        and_=and_,
        fecha_de_reporte=date.today())
    
@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    grupos = db_session.query(models.Grupos).all()
    
    alumnos = db_session.query(models.Alumnos).all()
    
    # Obtener el parámetro 'records' del formulario
    records_por_pagina = int(request.args.get('records', 4))  # Si no se proporciona, se mostrarán 4 registros por página
    
    page = request.args.get('page')
    page = int(page) if (page and page != '') else 1

    total_records = len(alumnos)
    pages_count = ceil(total_records / records_por_pagina)

    page_offset = (page - 1) * records_por_pagina
    page_limit = page_offset + records_por_pagina
    
    alumnos_paginados = alumnos[page_offset:page_limit]

    args = {'arg1': 'valor1', 'arg2': 'valor2'}
    
    return render_template('alumnos/alumnos.html', alumnos=alumnos_paginados, 
                                           page=page,
                                           grupos=grupos,
                                           pages_count=pages_count, 
                                           args=args,
                                           page_offset=page_offset, 
                                           page_limit=page_limit, 
                                           total_records=total_records,
                                           records_por_pagina=records_por_pagina)

@app.get("/docentes")
def docentes():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    docentes = db_session.query(models.Docentes).all()
    
     # Obtener el parámetro 'records' del formulario
    records_por_pagina = int(request.args.get('records', 4))  # Si no se proporciona, se mostrarán 4 registros por página
    
    page_docentes = request.args.get('page_docentes')
    page_docentes = int(page_docentes) if (page_docentes and page_docentes != '') else 1

    total_records_docentes = len(docentes)
    pages_count_docentes = ceil(total_records_docentes / records_por_pagina)

    page_offset = (page_docentes - 1) * records_por_pagina
    page_limit = page_offset + records_por_pagina
    
    docentes_paginados = docentes[page_offset:page_limit]

    args_docentes = {'arg1': 'valor1', 'arg2': 'valor2'}
    
    return render_template ('docentes/docentes.html', docentes=docentes_paginados, 
                                           page_docentes=page_docentes, 
                                           pages_count_docentes=pages_count_docentes, 
                                           args_docentes=args_docentes, 
                                           page_offset=page_offset, 
                                           page_limit=page_limit, 
                                           total_records_docentes=total_records_docentes,
                                           records_por_pagina=records_por_pagina)

@app.route("/personal", methods=['GET', 'POST'])
def personal_administrativo():

    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    personal = db_session.query(models.Personal).all()
 
     # Obtener el parámetro 'records' del formulario
    records_por_pagina = int(request.args.get('records', 4))  # Si no se proporciona, se mostrarán 4 registros por página
    
    page_personal = request.args.get('page_personal')
    page_personal = int(page_personal) if (page_personal and page_personal != '') else 1

    total_records_personal = len(personal)
    pages_count_personal = ceil(total_records_personal / records_por_pagina)

    page_offset = (page_personal - 1) * records_por_pagina
    page_limit = page_offset + records_por_pagina
    
    personal_paginados = personal[page_offset:page_limit]

    args_personal = {'arg1': 'valor1', 'arg2': 'valor2'}
    
    return render_template ('personal/personal_administrativo.html', personal=personal_paginados, 
                                           page_personal=page_personal, 
                                           pages_count_personal=pages_count_personal, 
                                           args_personal=args_personal, 
                                           page_offset=page_offset, 
                                           page_limit=page_limit, 
                                           total_records_personal=total_records_personal,
                                           records_por_pagina=records_por_pagina)

@app.route('/carreras', methods=['GET', 'POST'])
def admin_carreras():
    if request.method == 'POST':
        nombre = request.form['nombre']
        rvoe = request.form['rvoe']

        if not nombre or nombre == '':
            flash('Error: Indica el nombre de la carrera.')
            return redirect(url_for('admin_carreras'))
        
        nueva_carrera = models.Carreras()
        nueva_carrera.nombre = nombre
        nueva_carrera.rvoe = rvoe

        db_session.add(nueva_carrera)
        db_session.commit()
        flash('Info: Registro completado.')
        return redirect(url_for('admin_carreras'))

    carreras = db_session.query(models.Carreras).all()

    # Obtener el parámetro 'records' del formulario
    records_por_pagina = int(request.args.get('records', 4))  # Si no se proporciona, se mostrarán 4 registros por página
    page = request.args.get('page')
    page = int(page) if (page and page != '') else 1

    total_records = len(carreras)
    pages_count = ceil(total_records / records_por_pagina)

    page_offset = (page - 1) * records_por_pagina
    page_limit = page_offset + records_por_pagina
    
    carreras_paginadas = carreras[page_offset:page_limit]
    
    args = {'arg1': 'valor1', 'arg2': 'valor2'}

    return render_template('carreras/home_carreras.html', carreras=carreras_paginadas, 
                                                          page=page, 
                                                          pages_count=pages_count, 
                                                          args=args, 
                                                          page_offset=page_offset, 
                                                          page_limit=page_limit, 
                                                          total_records=total_records,
                                                          records_por_pagina=records_por_pagina)

@app.route('/cuatrimestres', methods=['GET', 'POST'])
def admin_cuatrimestres():
    if request.method == 'POST':
        nombre = request.form['nombre']

        if not nombre or nombre == '':
            flash('Error: Indica el nombre de la carrera.')
            return redirect(url_for('admin_cuatrimestres'))
        
        nueva_carrera = models.Cuatrimestres()
        nueva_carrera.nombre = nombre

        db_session.add(nueva_carrera)
        db_session.commit()
        flash('Info: Registro completado.')
        return redirect(url_for('admin_cuatrimestres'))

    cuatrimestres = db_session.query(models.Cuatrimestres).all()

    # Obtener el parámetro 'records' del formulario
    records_por_pagina = int(request.args.get('records', 4))  # Si no se proporciona, se mostrarán 4 registros por página
    page = request.args.get('page')
    page = int(page) if (page and page != '') else 1

    total_records = len(cuatrimestres)
    pages_count = ceil(total_records / records_por_pagina)

    page_offset = (page - 1) * records_por_pagina
    page_limit = page_offset + records_por_pagina
    
    cuatrimestres_paginadas = cuatrimestres[page_offset:page_limit]
    
    args = {'arg1': 'valor1', 'arg2': 'valor2'}

    return render_template('cuatrimestres/home_cuatrimestres.html', cuatrimestres=cuatrimestres_paginadas, 
                                                          page=page, 
                                                          pages_count=pages_count, 
                                                          args=args, 
                                                          page_offset=page_offset, 
                                                          page_limit=page_limit, 
                                                          total_records=total_records,
                                                          records_por_pagina=records_por_pagina)

@app.route('/grupos', methods=['GET', 'POST'])
def admin_grupos():
    
    if request.method == 'POST':
        
        carrera_id = db_session.query(models.Carreras).all()
        cuatrimestre_id = db_session.query(models.Cuatrimestres).all()
        
        carrera_id = request.form['carrera_id']
        cuatrimestre_id = request.form['cuatrimestre_id']
        clave = request.form['clave']
        
        nuevo_grupo = models.Grupos()

        nuevo_grupo.carrera_id = carrera_id
        nuevo_grupo.cuatrimestre_id = cuatrimestre_id
        nuevo_grupo.clave = clave

        db_session.add(nuevo_grupo)
        db_session.commit()
        flash('Info: Grupo creado correctamente.')
        return redirect(url_for('admin_grupos'))
    
    cuatrimestres = db_session.query(models.Cuatrimestres).all()
    carreras = db_session.query(models.Carreras).all()
    grupos = db_session.query(models.Grupos).all()
    
    # Obtener el parámetro 'records' del formulario
    records_por_pagina = int(request.args.get('records', 4))  # Si no se proporciona, se mostrarán 4 registros por página
    page = request.args.get('page')
    page = int(page) if (page and page != '') else 1

    total_records = len(grupos)
    pages_count = ceil(total_records / records_por_pagina)

    page_offset = (page - 1) * records_por_pagina
    page_limit = page_offset + records_por_pagina
    
    grupos_paginados = grupos[page_offset:page_limit]
    
    args = {'arg1': 'valor1', 'arg2': 'valor2'}
    
    return render_template('grupos/home_grupos.html', grupos=grupos_paginados, 
                                                      page=page, 
                                                      pages_count=pages_count, 
                                                      args=args,
                                                      carreras=carreras,
                                                      cuatrimestres=cuatrimestres,
                                                      page_offset=page_offset, 
                                                      page_limit=page_limit, 
                                                      total_records=total_records,
                                                      records_por_pagina=records_por_pagina)

@app.route('/materias', methods=['GET', 'POST'])
def admin_materias():
    
    if request.method == 'POST':
        
        carrera_id = db_session.query(models.Carreras).all()
        cuatrimestre_id = db_session.query(models.Cuatrimestres).all()
        
        carrera_id = request.form['carrera_id']
        cuatrimestre_id = request.form['cuatrimestre_id']
        nombre_materia = request.form['nombre_materia']
        
        nuevo_grupo = models.Grupos()

        nuevo_grupo.carrera_id = carrera_id
        nuevo_grupo.cuatrimestre_id = cuatrimestre_id
        nuevo_grupo.nombre_materia = nombre_materia

        db_session.add(nuevo_grupo)
        db_session.commit()
        flash('Info: Materia creado correctamente.')
        return redirect(url_for('admin_grupos'))
    
    cuatrimestres = db_session.query(models.Cuatrimestres).all()
    carreras = db_session.query(models.Carreras).all()
    grupos = db_session.query(models.Grupos).all()
    
    return render_template('materias/home_materias.html', grupos=grupos, 
                                                      carreras=carreras,
                                                      cuatrimestres=cuatrimestres)

@app.get('/admin/carreras/<id>/delete')
def admin_carreras_delete(id):
    
    carrera = db_session.query(models.Carreras).get(id)

    if not carrera:
        flash('Error: Carrera no encontrada.')
        return redirect(url_for('admin_carreras'))
    
    db_session.delete(carrera)
    db_session.commit()

    flash('Info: Carrera eliminada correctamente.')
    return redirect(url_for('admin_carreras'))

@app.post('/admin/carreras/<id>/update')
def admin_carreras_update(id):
    
    carrera = db_session.query(models.Carreras).get(id)

    if not carrera:
        flash('Error: Carrera no encontrada.')
        return redirect(url_for('admin_carreras'))
    
    nombre = request.form['nombre']
    rvoe = request.form['rvoe']

    if nombre and nombre != '':
        carrera.nombre = nombre
    if rvoe and rvoe != '':
        carrera.rvoe = rvoe
    
    db_session.add(carrera)
    db_session.commit()

    flash('Info: Carrera actualizada correctamente.')
    return redirect(url_for('admin_carreras'))

@app.post('/admin/cuatrimestres/<id>/update')
def admin_cuatrimestres_update(id):
    
    carrera = db_session.query(models.Cuatrimestres).get(id)

    if not carrera:
        flash('Error: Cuatrimestre no encontrada.')
        return redirect(url_for('admin_cuatrimestres'))
    
    nombre = request.form['nombre']

    if nombre and nombre != '':
        carrera.nombre = nombre
    
    db_session.add(carrera)
    db_session.commit()

    flash('Info: Carrera actualizada correctamente.')
    return redirect(url_for('admin_cuatrimestres'))

@app.get('/admin/cuatrimestres/<id>/delete')
def admin_cuatrimestres_delete(id):
    
    cuatrimestre = db_session.query(models.Cuatrimestres).get(id)

    if not cuatrimestre:
        flash('Error: Cuatrimestre no encontrado.')
        return redirect(url_for('admin_cuatrimestres'))
    
    db_session.delete(cuatrimestre)
    db_session.commit()

    flash('Info: Cuatrimestre eliminado correctamente.')
    return redirect(url_for('admin_cuatrimestres'))

@app.get('/admin/grupos/<id>/delete')
def admin_grupos_delete(id):
    
    grupo = db_session.query(models.Grupos).get(id)

    if not grupo:
        flash('Error: Grupo no encontrado.')
        return redirect(url_for('admin_grupos'))
    
    db_session.delete(grupo)
    db_session.commit()

    flash('Info: Grupo eliminado correctamente.')
    return redirect(url_for('admin_grupos'))

@app.post('/admin/grupos/<id>/update')
def admin_grupos_update(id):
    
    grupo = db_session.query(models.Grupos).get(id)

    if not grupo:
        flash('Error: Grupo no encontrado.')
        return redirect(url_for('admin_grupos'))
    
    carrera_id = request.form['carrera_id']
    cuatrimestre_id = request.form['cuatrimestre_id']
    clave = request.form['clave']

    if carrera_id and carrera_id != '':
        grupo.carrera_id = carrera_id
    if cuatrimestre_id and cuatrimestre_id != '':
        grupo.cuatrimestre_id = cuatrimestre_id
    if clave and clave != '':
        grupo.clave = clave

    db_session.add(grupo)
    db_session.commit()

    flash('Info: Grupo actualizado correctamente.')
    return redirect(url_for('admin_grupos'))
 
# Ruta para generar el PDF
@app.route('/reporte_alumnos')
def reporte_alumnos():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    # Obtiene los datos de la tabla desde la base de datos SQLite
    alumnos = db_session.query(models.Alumnos).all()

    db_session.commit()
    # Lista de registros para enviar al HTML del PDF
    return render_template('reportes/reporte_alumnos.html', alumnos=alumnos)

# Ruta para generar el PDF de cada alumno
@app.get('/alumno/<id>')
def reporte_alumno_id(id):
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    # Obtiene los datos de la tabla desde la base de datos SQLite
    alumno = db_session.query(models.Alumnos).get(id)

    # Lista de registros para enviar al HTML del PDF
    return render_template('reportes/reporte_alumno_id.html', alumno=alumno)

@app.get('/docente/<id>')
def reporte_docente_id(id):
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    # Obtiene los datos de la tabla desde la base de datos SQLite
    docente = db_session.query(models.Docentes).get(id)

    # Lista de registros para enviar al HTML del PDF
    return render_template('reportes/reporte_docente_id.html', docente=docente)

@app.get('/personal/<id>')
def reporte_personal_id(id):
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    # Obtiene los datos de la tabla desde la base de datos SQLite
    personal = db_session.query(models.Personal).get(id)

    # Lista de registros para enviar al HTML del PDF
    return render_template('reportes/reporte_personal_id.html', personal=personal)
# Ruta para generar el PDF
@app.route('/reporte_docentes')
def reporte_docentes():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    # Obtiene los datos de la tabla desde la base de datos SQLite
    docentes = db_session.query(models.Docentes).all()

    # Lista de registros para enviar al HTML del PDF
    return render_template('reportes/reporte_docentes.html', docentes=docentes)

# Ruta para generar el PDF
@app.route('/reporte_personal')
def reporte_personal():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    # Obtiene los datos de la tabla desde la base de datos SQLite
    personal = db_session.query(models.Personal).all()

    # Lista de registros para enviar al HTML del PDF
    return render_template('reportes/reporte_personal.html', personal=personal)

@app.get('/reportes')
def reportes():
    
    alumnos = db_session.query(models.Alumnos)

    return render_template('reportes/grafica_estatus.html',
        alumnos=alumnos,
        models=models,
        and_=and_,
        fecha_de_reporte=date.today())

# Rutas del login
@app.get('/login/')
def login():
    return render_template('login.html')

@app.post('/login')
def login_post():    
    user = request.form['user']
    password = request.form['password']

    # Validar que los campos no estén vacíos
    if not user or not password:
        flash('Advertencia: Usuario y contraseña son obligatorios.')
        return redirect(url_for('login'))

    # Validar que el campo de usuario solo contenga números y letras
    if not re.match("^[a-zA-Z0-9]+$", user):
        flash('Advertencia: El usuario solo puede contener números y letras.')
        return redirect(url_for('login'))

    # Obtener el usuario de la base de datos
    usuario = db_session.query(models.Usuarios).filter(models.Usuarios.nom_user == user).first()

    # Verificar la contraseña utilizando check_password_hash
    if not usuario or not check_password_hash(usuario.user_ingreso_hashed, password):
        flash('Advertencia: Credenciales inválidas.')
        return redirect(url_for('login'))

    session['id'] = usuario.id
    return redirect(url_for('panel_principal'))

@app.get('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.get("/usuarios")
def form_usuarios():
    
    usuarios = db_session.query(models.Usuarios).all()
    return render_template ('usuarios/usuarios.html', usuarios = usuarios)

@app.post("/usuario")
def post_usuarios():
    nombre = request.form['nombre-user']
    contrasena = request.form['password']

    if not nombre or not contrasena:
        flash('Advertencia: Nombre de usuario y contraseña son obligatorios.')
        return redirect(url_for('form_usuarios'))

    # Validar que el campo de usuario solo contenga números y letras
    if not re.match("^[a-zA-Z0-9]+$", nombre):
        flash('Advertencia: El nombre de usuario solo puede contener números y letras.')
        return redirect(url_for('form_usuarios'))

    # Encriptar la contraseña antes de almacenarla
    contrasena_encriptada = generate_password_hash(contrasena)

    nuevo_user = models.Usuarios(
        nom_user=nombre,
        user_ingreso_hashed=contrasena_encriptada
    )

    db_session.add(nuevo_user)
    db_session.commit()

    flash('Usuario registrado exitosamente.')
    return redirect(url_for('form_usuarios'))

@app.get("/usuario/<id>/delete")
def delete_usuario(id):
    '''Ruta para eliminar usuarios'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))

    usuario = db_session.query(models.Usuarios).get(id)
    if usuario == None:
        return "No encontrado",404
    db_session.delete(usuario)
    db_session.commit()

    return redirect(url_for('form_usuarios'))

@app.get('/usuario/<id>/reset')
def usuario_reset(id):
    
    usuario = db_session.query(models.Usuarios).get(id)

    if not usuario:
        flash('Error: Usuario no encontrado.')
        return redirect(url_for('admin_usuarios'))
    
    usuario.user_ingreso_hashed = usuario.nom_user
    
    db_session.add(usuario)
    db_session.commit()

    flash('Info: Usuario reseteado correctamente.')
    return redirect(url_for('admin_usuarios'))

# Ruta registro de alumnos
@app.route("/post_alumnos", methods=['GET', 'POST'])
def post_alumnos():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    grupo_id = db_session.query(models.Carreras).all()
 
    nombre = request.form['nombre_alumno']
    estatus = request.form['estatus_alumno']
    sexo = request.form.get('sexo_alumno')
    folio = request.form['folio_alumno']
    curp = request.form['curp_alumno']
    grupo_id = request.form['grupo_id']
    domicilio = request.form['domicilio_alumno']
    correo = request.form['correo_alumno']
    telefono = request.form['telefono_alumno']
    fecha_inscripcion = request.form['fecha_inscripcion']

    # Validar que el nombre solo contenga letras, espacios y caracteres acentuados en español
    if not re.match("^[a-zA-Z\sáéíóúÁÉÍÓÚüÜñÑ]+$", nombre):
        flash('Advertencia: El nombre solo puede contener letras, espacios y caracteres acentuados en español.')
        return redirect(url_for('alumnos'))

    # Validar que el folio solo contenga números y tenga un máximo de 7 caracteres
    if not re.match("^[0-9]{1,7}$", folio):
        flash('Advertencia: El folio debe contener como máximo 7 números y no se aceptan letras.')
        return redirect(url_for('alumnos'))

    # Validar que el CURP tenga un máximo de 18 caracteres y contenga solo letras mayúsculas y números
    if not re.match("^[A-Z0-9]{18}$", curp):
        flash('Advertencia: El CURP debe contener como máximo 18 caracteres y solo letras mayúsculas y números.')
        return redirect(url_for('alumnos'))

    # Validar que el domicilio contenga solo números, letras y algunos signos de puntuación, incluyendo acentos
    if not re.match("^[a-zA-Z0-9\sáéíóúÁÉÍÓÚüÜñÑ.,'-]+$", domicilio):
        flash('Advertencia: El domicilio solo puede contener números, letras y algunos signos de puntuación, incluyendo acentos.')
        return redirect(url_for('alumnos'))

    # Validar que el teléfono solo contenga números y tenga exactamente 10 caracteres
    if not re.match("^[0-9]{10}$", telefono):
        flash('Advertencia: El teléfono debe contener exactamente 10 números.')
        return redirect(url_for('alumnos'))


    # Puedes agregar más validaciones según tus requisitos para correo y otros campos

    fecha_conversion = datetime.strptime(fecha_inscripcion, '%Y-%m-%d')

    nuevo_alumno = models.Alumnos(
        nombre=nombre,
        estatus=estatus,
        sexo=sexo,
        folio=folio,
        curp=curp,
        grupo_id=grupo_id,
        domicilio=domicilio,
        correo=correo,
        telefono=telefono,
        fecha_inscripcion=fecha_conversion
    )

    db_session.add(nuevo_alumno)
    db_session.commit()
    flash('Registro completado.')
    return redirect(url_for('alumnos', include=nuevo_alumno.id, _anchor=f'popup/modal-egresado-{nuevo_alumno.id}'))

# Rutas de tabla alumnos
@app.post("/post_personal")
def post_personal():
    '''Ruta para alta de alumnos'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))

    nombre = request.form['nombre_personal']
    folio = request.form['folio_personal']
    puesto = request.form['puesto_personal']
    periodocontratoini = request.form['fecha_inicio']
    periodocontratofin = request.form['fecha_fin']
    correo = request.form['correo_personal']
    telefono = request.form['telefono_personal']
    domicilio = request.form['domicilio_personal']

    if nombre == None or nombre == '':
        flash("No registraste ningun producto")
        return redirect(url_for('home'))

    fecha_conversion_inicio = datetime.strptime(periodocontratoini, '%Y-%m-%d')
    fecha_conversion_fin = datetime.strptime(periodocontratofin, '%Y-%m-%d')  

    nuevo_personal = models.Personal(
        nombre = nombre,
        folio = folio,
        puesto = puesto,
        periodocontratoini = fecha_conversion_inicio,
        periodocontratofin = fecha_conversion_fin,
        correo = correo,
        telefono = telefono,
        domicilio = domicilio
    )

    flash('Registro completado.')

    db_session.add(nuevo_personal)
    db_session.commit()
    return redirect(url_for('personal_administrativo'))

# Rutas de tabla docentes
@app.post("/post_docentes")
def post_docentes():
    '''Ruta para alta de alumnos'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))

    nombre = request.form['nombre_docente']
    folio = request.form['folio_docente']
    carrera = request.form['carrera_docente']
    periodocontratoini = request.form['fecha_inicio']
    periodocontratofin = request.form['fecha_fin']
    correo = request.form['correo_docente']
    telefono = request.form['telefono_docente']
    domicilio = request.form['domicilio_docente']

    if nombre == None or nombre == '':
        flash("No registraste ningun producto")
        return redirect(url_for('home'))
    
    fecha_conversion_inicio = datetime.strptime(periodocontratoini, '%Y-%m-%d')
    fecha_conversion_fin = datetime.strptime(periodocontratofin, '%Y-%m-%d')

    nuevo_docente = models.Docentes(
        nombre = nombre,
        folio = folio,
        carrera = carrera,
        periodocontratoini = fecha_conversion_inicio,
        periodocontratofin = fecha_conversion_fin,
        correo = correo,
        telefono = telefono,
        domicilio = domicilio
    )

    flash('Registro completado.')

    db_session.add(nuevo_docente)
    db_session.commit()
    return redirect(url_for('docentes'))

@app.get("/alumno/<id>/delete")
def delete_alumno(id):
    '''Ruta para eliminar alumno por id'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    alumno = db_session.query(models.Alumnos).get(id)
    if alumno == None:
        return "No encontrado",404
    db_session.delete(alumno)
    db_session.commit()

    flash('Info: Alumno eliminado correctamente.')

    return redirect(url_for('alumnos'))

@app.get("/docente/<id>/delete")
def delete_docente(id):
    '''Ruta para eliminar docente por id'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    docente = db_session.query(models.Docentes).get(id)
    if docente == None:
        return "No encontrado",404
    db_session.delete(docente)
    db_session.commit()

    return redirect(url_for('docentes'))

@app.get("/personal/<id>/delete")
def delete_personal(id):
    '''Ruta para eliminar docente por id'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    personal = db_session.query(models.Personal).get(id)
    if personal == None:
        return "No encontrado",404
    db_session.delete(personal)
    db_session.commit()

    return redirect(url_for('personal_administrativo'))

@app.post("/alumno/<id>/update")
def update_alumno(id):
    '''Ruta para actualizar alumno'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    alumno = db_session.query(models.Alumnos).get(id)

    if alumno == None:
        return "No encontrado",404
    
    nombre = request.form['n_nombre_alumno']
    estatus = request.form['n_estatus_alumno']
    folio = request.form['n_folio_alumno']
    curp = request.form['n_curp_alumno']
    grupo_id = request.form['n_grupo_id']
    sexo = request.form['n_sexo_alumno']
    domicilio = request.form['n_domicilio_alumno']
    correo = request.form['n_correo_alumno']
    telefono = request.form['n_telefono_alumno']
    fecha_inscripcion = request.form['n_fecha_inscripcion_alumno']
    
    if nombre != None and nombre != "":
        alumno.nombre = nombre
    if estatus != None and estatus != "":
        alumno.estatus = estatus
    if folio != None and folio != "":
        alumno.folio = folio
    if curp != None and curp != "":
        alumno.curp = curp
    if grupo_id != None and grupo_id != "":
        alumno.grupo_id = grupo_id
    if domicilio != None and domicilio != "":
        alumno.domicilio = domicilio
    if correo != None and correo != "":
        alumno.correo = correo
    if telefono != None and telefono != "":
        alumno.telefono = telefono
    if sexo != None and sexo != "":
        alumno.sexo = sexo
    if fecha_inscripcion != None and fecha_inscripcion != "":
        alumno.fecha_inscripcion = datetime.strptime(fecha_inscripcion, '%Y-%m-%d')
    
    flash('Alumno actualizado correctamente.')
    
    db_session.add(alumno)
    db_session.commit()

    return redirect(url_for('alumnos'))

@app.post("/docente/<id>/update")
def update_docente(id):
    '''Ruta para actualizar docente'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    docente = db_session.query(models.Docentes).get(id)

    if docente is None:
        return "No encontrado", 404
    
    nombre = request.form['n_nombre_docente']
    folio = request.form['n_folio_docente']
    carrera = request.form['n_carrera_docente']
    periodocontratoini = request.form['n_fecha_inicio']
    periodocontratofin = request.form['n_fecha_fin']
    correo = request.form['n_correo_docente']
    telefono = request.form['n_telefono_docente']
    domicilio = request.form['n_domicilio_docente']
    
    if nombre:
        docente.nombre = nombre
    if folio:
        docente.folio = folio
    if carrera:
        docente.carrera = carrera
    if periodocontratoini:
        # Convierte la fecha a objeto datetime
        docente.periodocontratoini = datetime.strptime(periodocontratoini, '%Y-%m-%d')
    if periodocontratofin:
        # Convierte la fecha a objeto datetime
        docente.periodocontratofin = datetime.strptime(periodocontratofin, '%Y-%m-%d')
    if correo:
        docente.correo = correo
    if telefono:
        docente.telefono = telefono
    if domicilio:
        docente.domicilio = domicilio
    
    flash('Docente actualizado correctamente.')
    
    db_session.commit()

    return redirect(url_for('docentes'))


@app.post("/personal/<id>/update")
def update_personal(id):
    '''Ruta para actualizar alumno'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    personal = db_session.query(models.Personal).get(id)

    if personal == None:
        return "No encontrado",404
    
    nombre = request.form['n_nombre_personal']
    folio = request.form['n_folio_personal']
    puesto = request.form['n_puesto_personal']
    periodocontrato = request.form['n_periodo_contrato_personal']
    correo = request.form['n_correo_personal']
    telefono = request.form['n_telefono_personal']
    domicilio = request.form['n_domicilio_personal']
    
    if nombre != None and nombre != "":
        personal.nombre = nombre
    if folio != None and folio != "":
        personal.folio = folio
    if puesto != None and puesto != "":
        personal.puesto = puesto
    if periodocontrato != None and periodocontrato != "":
        personal.periodocontrato = periodocontrato
    if correo != None and correo != "":
        personal.correo = correo
    if correo != None and correo != "":
        personal.correo = correo
    if telefono != None and telefono != "":
        personal.telefono = telefono
    if domicilio != None and domicilio != "":
        personal.domicilio = domicilio
   
    flash('Personal administrativo actualizado correctamente.')
    
    db_session.add(personal)
    db_session.commit()

    return redirect(url_for('personal'))

app.run("0.0.0.0",8081,debug=True)
import os
import uuid
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
from flask import render_template, make_response
from flask_sslify import SSLify

from sqlalchemy import or_
from sqlalchemy import and_
from database import engine
from database import Database
from database import db_session

from werkzeug.utils import secure_filename

import models

app= Flask(__name__)
sslify = SSLify(app)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

Session(app)
Database.metadata.create_all(engine)

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

@app.get("/panel_principal")
def panel_principal():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    return render_template ('index.html')

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
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
                                           pages_count=pages_count, 
                                           args=args, 
                                           page_offset=page_offset, 
                                           page_limit=page_limit, 
                                           total_records=total_records,
                                           records_por_pagina=records_por_pagina)

@app.route('/carreras', methods=['GET', 'POST'])
def admin_carreras():
    
    if request.method == 'POST':
        nombre = request.form['nombre']

        if not nombre or nombre == '':
            flash('Error: Indica el nombre de la carrera.')
            return redirect(url_for('admin_carreras'))
        
        nueva_carrera = models.Carreras()

        nueva_carrera.nombre = nombre

        db_session.add(nueva_carrera)
        db_session.commit()
        flash('Info: Registro completado.')
        return redirect(url_for('admin_carreras'))
    
    carreras = db_session.query(models.Carreras).all()
    return render_template('carreras/home_carreras.html', carreras=carreras)

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

    if nombre and nombre != '':
        carrera.nombre = nombre
    
    db_session.add(carrera)
    db_session.commit()

    flash('Info: Carrera actualizada correctamente.')
    return redirect(url_for('admin_carreras'))

@app.route('/grupos', methods=['GET', 'POST'])
def admin_grupos():
    
    if request.method == 'POST':
        nombre = request.form['nombre']

        if not nombre or nombre == '':
            flash('Error: Indica el nombre del grupo.')
            return redirect(url_for('admin_grupos'))
        
        nuevo_grupo = models.Grupos()

        nuevo_grupo.nombre = nombre

        db_session.add(nuevo_grupo)
        db_session.commit()
        flash('Info: Grupo creado correctamente.')
        return redirect(url_for('admin_grupos'))
    
    grupos = db_session.query(models.Grupos).all()
    return render_template('grupos/home_grupos.html', grupos=grupos)

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
    
    nombre = request.form['nombre']

    if nombre and nombre != '':
        grupo.nombre = nombre

    db_session.add(grupo)
    db_session.commit()

    flash('Info: Grupo actualizado correctamente.')
    return redirect(url_for('admin_grupos'))

@app.get("/docentes")
def docentes():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    docentes = db_session.query(models.Docentes).all()
    
    page = request.args.get('page')
    page = int(page) if (page and page != '') else 1

    page_size = 4
    total_records = len(docentes)
    pages_count = ceil(total_records / page_size)

    page_offset = (page - 1) * page_size
    page_limit = page_offset + page_size
    
    docentes_paginados = docentes[page_offset:page_limit]

    args = {'arg1': 'valor1', 'arg2': 'valor2'}
    
    return render_template ('docentes/docentes.html', docentes=docentes_paginados, 
                                            page=page, 
                                            pages_count=pages_count, 
                                            args=args, 
                                            page_offset=page_offset, 
                                            page_limit=page_limit, 
                                            total_records=total_records)
    
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
        and_=and_,)

@app.get('/reportes_sexo')
def reportes_sexo():
    
    alumnos = db_session.query(models.Alumnos)

    return render_template('reportes/grafica_sexo.html',
        alumnos=alumnos,
        models=models,
        and_=and_,)

# Rutas del login
@app.get('/login/')
def login():
    return render_template('login.html')

@app.post('/login')
def login_post():    
    user = request.form['user']
    password = request.form['password']

    #validar usuario y contraseña
    usuarios = db_session.query(models.Usuarios).filter(
        and_(models.Usuarios.nom_user==user,
        models.Usuarios.user_ingreso==password)
    ).first()

    if not usuarios:
        flash('Advertencia: Credenciales invalidas.')
        return redirect(url_for('login_post'))
    
    session['id'] = usuarios.id
    return redirect(url_for('panel_principal'))

@app.get('/logout')
def logout():
    session.clear()

    return redirect(url_for('login'))

@app.get("/usuarios")
def form_usuarios():
    
    usuarios = db_session.query(models.Usuarios).all()
    return render_template ('usuarios/formulario-usuarios.html', usuarios = usuarios)

# Rutas de tabla usuarios.
@app.post("/usuario")
def post_usuarios():

    nombre = request.form['nombre-user']
    contrasena = request.form['password']

    if nombre == None or nombre == '':
         return "No registrado",404
    
    nuevo_user = models.Usuarios(
        nom_user = nombre,
        user_ingreso = contrasena
    )

    db_session.add(nuevo_user)
    db_session.commit()
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

# Ruta registro de alumnos
@app.post("/post_alumnos")
def post_alumnos():
    '''Ruta para alta de alumnos'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    nombre = request.form['nombre_alumno']
    estatus = request.form['estatus_alumno']
    sexo = request.form['sexo_alumno']
    folio = request.form['folio_alumno']
    curp = request.form['curp_alumno']
    carrera = request.form['carrera_alumno']
    domicilio = request.form['domicilio_alumno']
    correo = request.form['correo_alumno']
    telefono = request.form['telefono_alumno']
    fecha_inscripcion = request.form['fecha_inscripcion']

    if nombre == None or nombre == '':
        flash("No registraste ningun producto")
        return redirect(url_for('home'))
    
    fecha_conversion = datetime.strptime(fecha_inscripcion, '%Y-%m-%d')

    nuevo_alumno = models.Alumnos(
        nombre = nombre,
        estatus = estatus,
        sexo = sexo,
        folio = folio,
        curp = curp,
        carrera = carrera,
        domicilio = domicilio,
        correo = correo,
        telefono = telefono,
        fecha_inscripcion= fecha_conversion
    )   

    flash('Registro completado.')

    db_session.add(nuevo_alumno)
    db_session.commit()
    return redirect(url_for('alumnos'))

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
    periodocontrato = request.form['periodo_contrato_docente']
    correo = request.form['correo_docente']
    telefono = request.form['telefono_docente']
    domicilio = request.form['domicilio_docente']

    if nombre == None or nombre == '':
        flash("No registraste ningun producto")
        return redirect(url_for('home'))
    

    nuevo_docente = models.Docentes(
        nombre = nombre,
        folio = folio,
        carrera = carrera,
        periodocontrato = periodocontrato,
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

    return redirect(url_for('personal'))

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
    carrera = request.form['n_carrera_alumno']
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
    if carrera != None and carrera != "":
        alumno.carrera = carrera
    if domicilio != None and domicilio != "":
        alumno.domicilio = domicilio
    if correo != None and correo != "":
        alumno.correo = correo
    if telefono != None and telefono != "":
        alumno.telefono = telefono
    if fecha_inscripcion != None and fecha_inscripcion != "":
        alumno.fecha_inscripcion = datetime.strptime(fecha_inscripcion, '%Y-%m-%d')
    
    flash('Alumno actualizado correctamente.')
    
    db_session.add(alumno)
    db_session.commit()

    return redirect(url_for('alumnos'))

@app.post("/docente/<id>/update")
def update_docente(id):
    '''Ruta para actualizar alumno'''
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    docente = db_session.query(models.Docentes).get(id)

    if docente == None:
        return "No encontrado",404
    
    nombre = request.form['n_nombre_docente']
    folio = request.form['n_folio_docente']
    carrera = request.form['n_carrera_docente']
    periodocontrato = request.form['n_periodo_contrato_docente']
    correo = request.form['n_correo_docente']
    telefono = request.form['n_telefono_docente']
    domicilio = request.form['n_domicilio_docente']
    
    if nombre != None and nombre != "":
        docente.nombre = nombre
    if folio != None and folio != "":
        docente.folio = folio
    if carrera != None and carrera != "":
        docente.carrera = carrera
    if periodocontrato != None and periodocontrato != "":
        docente.periodocontrato = periodocontrato
    if correo != None and correo != "":
        docente.correo = correo
    if correo != None and correo != "":
        docente.correo = correo
    if telefono != None and telefono != "":
        docente.telefono = telefono
    if domicilio != None and domicilio != "":
        docente.domicilio = domicilio
    
    flash('Docente actualizado correctamente.')
    
    db_session.add(docente)
    db_session.commit()

    return redirect(url_for('docentes'))

@app.get("/personal")
def personal():
    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))

    sesion_iniciada = session.get('id', False)

    if not sesion_iniciada:
        return redirect(url_for('login'))
    
    personal = db_session.query(models.Personal).all()
    
    page = request.args.get('page')
    page = int(page) if (page and page != '') else 1

    page_size = 4
    total_records = len(personal)
    pages_count = ceil(total_records / page_size)

    page_offset = (page - 1) * page_size
    page_limit = page_offset + page_size
    
    personal_paginados = personal[page_offset:page_limit]

    args = {'arg1': 'valor1', 'arg2': 'valor2'}
    
    return render_template ('personal/personal_administrativo.html', personal=personal_paginados, 
                                            page=page, 
                                            pages_count=pages_count, 
                                            args=args, 
                                            page_offset=page_offset, 
                                            page_limit=page_limit, 
                                            total_records=total_records)

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
    periodocontrato = request.form['periodo_contrato_personal']
    correo = request.form['correo_personal']
    telefono = request.form['telefono_personal']
    domicilio = request.form['domicilio_personal']

    if nombre == None or nombre == '':
        flash("No registraste ningun producto")
        return redirect(url_for('home'))
    

    nuevo_personal = models.Personal(
        nombre = nombre,
        folio = folio,
        puesto = puesto,
        periodocontrato = periodocontrato,
        correo = correo,
        telefono = telefono,
        domicilio = domicilio
    )

    flash('Registro completado.')

    db_session.add(nuevo_personal)
    db_session.commit()
    return redirect(url_for('personal'))

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
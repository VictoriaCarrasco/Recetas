from flask import render_template, request, session, redirect, flash
from app_recetas.modelos.modelo_usuarios import Usuario
from app_recetas import app 
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt (app)

@app.route('/', methods=['GET'])
def desplegar_login_registro():
    return render_template ('login_registro.html')

@app.route('/crear/usuario', methods=['POST'])
def nuevo_usuario():
    #Validar formulario: si hay algo falla en el formulario devuelveme/redireccioname a la página principal.
    data ={
        **request.form #Request form es el formulario, y los asteriscos copian TODO formulario al diccionario data.
    }
    usuario_existe = Usuario.obtener_uno_con_email(data)
    if Usuario.validar_registro(data, usuario_existe) == False:
        return redirect ('/')
    else:
        password_escriptado = bcrypt.generate_password_hash(data['password'])
        data ['password'] = password_escriptado
        id_usuario = Usuario.crear_uno(data)     #Insertar en la base de datos el nuevo usuario
        session ['nombre'] = data ['nombre']    #Agregar los datos del usuario en sesion 
        session['apellido'] = data ['apellido']
        session ['id_usuario'] = id_usuario

        return redirect ("/recetas")
    
#Redireccionar al home
@app.route('/login', methods=['POST'])
def procesa_login():
    data = {
        "email": request.form ['email_login']
    }
    usuario_existe = Usuario.obtener_uno_con_email (data)
    if usuario_existe == None:
        flash("Este usuario no existe.", "error_email_login")
        return redirect ('/')
    else: 
        if not bcrypt.check_password_hash(usuario_existe.password, request.form['password_login']): 
            flash("Credenciales incorrectas.", "error_password_login")
            return redirect ('/')
        else: 
            session ['nombre'] = usuario_existe.nombre
            session['apellido'] = usuario_existe.apellido
            session ['id_usuario'] = usuario_existe.id
            return redirect ('/recetas')

@app.route('/logout', methods = ['POST'])
def procesa_logout():
    session.clear()
    return redirect ('/')
#!flask/bin/python
from flask import Flask, jsonify, request
import json
import pyodbc
import pandas as pd
from flask_httpauth import HTTPBasicAuth

server = 'tcp:127.0.0.1'
database = 'master'
username = 'sa'
password = 'icaiSQL2019'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                        SERVER='+server+';DATABASE='+database+'; \
                            UID='+username+';PWD='+password)
auth = HTTPBasicAuth()
app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
    df = pd.read_sql_query('SELECT username FROM usuarios WHERE username = ? AND pswd = ?',cnxn, params = [username,password])
    if(df.empty):
         return False
    else:
        return True


@app.route('/api/v1.0/bicimad/index', methods=['GET'])
#http://127.0.0.1:6878/api/v1.0/bicimad/index
def menu():
    return '''<br>¿Que desea hacer?<br>
                <form action="fechas">
                    <br>Consultar todas las fechas:
                  <input type="submit" value="Consultar"><br>
              </form>
              <form action="orgbs">
                    <br>Consultar todas las bases de origen:
                  <input type="submit" value="Consultar"><br>
              </form>
              <form action="dstbs">
                  <br>Consultar todas las bases de destino:
                  <input type="submit" value="Consultar"><br>
              </form>
              <form action="todofecha">
                <br>Consultar todos los datos de una fecha:
                  <input type="submit" value="Consultar"><br>
              </form>
              <form action="todofechaydst">
                <br>Consultar todos los datos de una fecha y una base de destino:
                  <input type="submit" value="Consultar"><br>
              </form>
              <form action="todofechayviaje">
                <br>Consultar todos los datos de una fecha y de una base de destino y origen:
                  <input type="submit" value="Consultar"><br>
              </form>
              <form action="todofechayviajeytiempo">
                <br>Consultar todos los datos de una fecha y de una base de destino y origen y con tiempo máximo:
                  <input type="submit" value="Consultar"><br>
              </form>
              <form action="insertar">
                <br>Insertar nuevos datos:
                  <input type="submit" value="Insertar"><br>
              </form>'''

@app.route('/api/v1.0/bicimad/fechas', methods=['GET'])
#http://127.0.0.1:6878/api/v1.0/bicimad/fechas
def get_dates():
    df = pd.read_sql_query('SELECT DISTINCT Fecha FROM bicimad',cnxn)
    result = df.to_html()
    return result

@app.route('/api/v1.0/bicimad/orgbs', methods=['GET'])
#http://127.0.0.1:6878/api/v1.0/bicimad/orgbs
def get_orgbs():
    df = pd.read_sql_query('SELECT DISTINCT idunplug_base FROM bicimad',cnxn)
    result = df.to_html()
    return result

@app.route('/api/v1.0/bicimad/dstbs', methods=['GET'])
#http://127.0.0.1:6878/api/v1.0/bicimad/dstbs
def get_dstbs():
    df = pd.read_sql_query('SELECT DISTINCT idplug_base FROM bicimad',cnxn)
    result = df.to_html()
    return result

@app.route('/api/v1.0/bicimad/todofecha', methods=['GET', 'POST'])
#http://127.0.0.1:6878/api/v1.0/bicimad/todofecha
def get_allfromDate():
    if request.method == 'GET':
        return '''<br>Insertar fecha de la que quiere consultar movimientos<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  <input type="submit" value="Consultar"><br>
              </form>'''
    elif request.method == 'POST':
        fecha = request.form.get('date')
        temp = fecha.split("-")
        formatedDate = temp[2]+"/"+temp[1]+"/"+temp[0]
        df = pd.read_sql_query('SELECT * FROM bicimad WHERE Fecha = ?',cnxn, params = [formatedDate])
        if(df.empty):
            return '''<br>Insertar fecha de la que quiere consultar movimientos<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  <input type="submit" value="Consultar"><br>
              </form>
              <br>No hay ningún dato para esa fecha. Inténtelo con otra.<br>'''
              
        else:
            result = df.to_html()
            return result

@app.route('/api/v1.0/bicimad/todofechaydst', methods=['GET', 'POST'])
#http://127.0.0.1:6878/api/v1.0/bicimad/todofechaydst
def get_allfromDateaAndDstBase():
    if request.method == 'GET':
        return '''<br>Insertar fecha y base de destino de la que quiere consultar movimientos<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  ID base de destino: <input type="text" name="iddst"><br>
                  <input type="submit" value="Consultar"><br>
              </form>'''
    elif request.method == 'POST':
        fecha = request.form.get('date')
        dst = request.form.get('iddst')
        temp = fecha.split("-")
        formatedDate = temp[2]+"/"+temp[1]+"/"+temp[0]
        df = pd.read_sql_query('SELECT * FROM bicimad WHERE Fecha = ? AND idplug_base = ?',cnxn, params = [formatedDate,dst])
        if(df.empty):
            return '''<br>Insertar fecha y base de destino de la que quiere consultar movimientos<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  ID base de destino: <input type="text" name="iddst"><br>
                  <input type="submit" value="Consultar"><br>
              </form>
              <br>No hay ningún dato para esa fecha y base de destino. Inténtelo con otra.<br>'''
              
        else:
            result = df.to_html()
            return result
    

@app.route('/api/v1.0/bicimad/todofechayviaje', methods=['GET', 'POST'])
#http://127.0.0.1:6878/api/v1.0/bicimad/todofechayviaje
def get_allfromDateaAndViaje():
    if request.method == 'GET':
        return '''<br>Insertar fecha e id de las bases de origen y destino de la que quiere consultar movimientos<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  ID base de origen: <input type="text" name="idorg"><br>
                  ID base de destino: <input type="text" name="iddst"><br>
                  <input type="submit" value="Consultar"><br>
              </form>'''
    elif request.method == 'POST':
        fecha = request.form.get('date')
        org = request.form.get('iddst')
        dst = request.form.get('idorg')
        temp = fecha.split("-")
        formatedDate = temp[2]+"/"+temp[1]+"/"+temp[0]
        df = pd.read_sql_query('SELECT * FROM bicimad WHERE Fecha = ? AND idplug_base = ? AND idunplug_base = ?',cnxn, params = [formatedDate,dst,org])
        if(df.empty):
            return '''<br>Insertar fecha e id de las bases de origen y destino de la que quiere consultar movimientos<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  ID base de origen: <input type="text" name="idorg"><br>
                  ID base de destino: <input type="text" name="iddst"><br>
                  <input type="submit" value="Consultar"><br>
              </form>
              <br>No hay ningún dato para esa fecha y base de destino. Inténtelo con otra.<br>'''
              
        else:
            result = df.to_html()
            return result
    

@app.route('/api/v1.0/bicimad/todofechayviajeytiempo', methods=['GET', 'POST'])
#http://127.0.0.1:6878/api/v1.0/bicimad/todofechayviajeytiempo
def get_allfromDateaAndViajeAndMaxTime():
    if request.method == 'GET':
        return '''<br>Insertar fecha e id de las bases de origen y destino además del tiempo maximo de la que quiere consultar movimientos<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  ID base de origen: <input type="text" name="idorg"><br>
                  ID base de destino: <input type="text" name="iddst"><br>
                  Inserte tiempo máximo del viaje: <input type="text" name="maxtime"><br>
                  <input type="submit" value="Consultar"><br>
              </form>'''
    elif request.method == 'POST':
        fecha = request.form.get('date')
        org = request.form.get('iddst')
        dst = request.form.get('idorg')
        maxtime = request.form.get('maxtime')
        temp = fecha.split("-")
        formatedDate = temp[2]+"/"+temp[1]+"/"+temp[0]
        df = pd.read_sql_query('SELECT * FROM bicimad WHERE Fecha = ? AND idplug_base = ? AND idunplug_base = ? AND travel_time < ?',cnxn, params = [formatedDate,dst,org,maxtime])
        if(df.empty):
            return '''<br>Insertar fecha e id de las bases de origen y destino además del tiempo maximo de la que quiere consultar movimientos<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  ID base de origen: <input type="text" name="idorg"><br>
                  ID base de destino: <input type="text" name="iddst"><br>
                  Inserte tiempo máximo del viaje: <input type="text" name="maxtime"><br>
                  <input type="submit" value="Consultar"><br>
              </form>
              <br>No hay ningún dato para esa fecha y base de destino. Inténtelo con otra.<br>'''
              
        else:
            result = df.to_html()
            return result
    

@app.route('/api/v1.0/bicimad/insertar', methods=['GET', 'POST'])
@auth.login_required
#http://127.0.0.1:6878/api/v1.0/bicimad/insertar
def Insertar():
    #print(usuarioValidado)
    if request.method == 'GET':
        return '''<br>Rellene los campos para enviar al servidor. Se validará sesión al mandar al servido<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  Rango de edad: <input type="text" name="ageRange"><br>
                  Tipo de usuario: <input type="text" name="usertype"><br>
                  Id de la estación de origen: <input type="text" name="idunplug_station"><br>
                  Id de la estación de destino: <input type="text" name="idplug_station"><br>
                  Id de la base de origen: <input type="text" name="idunplug_base"><br>
                  Id de la base de destino: <input type="text" name="idplug_base"><br>
                  Tiempo del viaje en segundos: <input type="text" name="travel_time"><br>
                  Fichero: <input type="text" name="Fichero"><br>
                  <input type="submit" value="Enviar"><br>
              </form>'''
    elif request.method == 'POST':
        date = request.form.get('date')
        ageRange = request.form.get('ageRange')
        user_type = request.form.get('usertype')
        idunplug_station = request.form.get('idunplug_station')
        idplug_station = request.form.get('idplug_station')
        idunplug_base = request.form.get('idunplug_base')
        idplug_base = request.form.get('idplug_base')
        travel_time = request.form.get('travel_time')
        Fichero = request.form.get('Fichero')
        temp = date.split("-")
        Fecha = temp[2]+"/"+temp[1]+"/"+temp[0]

        cursor = cnxn.cursor()
        cursor.execute('INSERT INTO bicimad VALUES (?,?,?,?,?,?,?,?,?)', [Fecha,ageRange,user_type,idunplug_station,idplug_station,idunplug_base,idplug_base,travel_time,Fichero])
        cursor.commit()
        if cursor:
            return '''<form action="index">
                    <br>Subido correctamente al servidor.
                    <input type="submit" value="Menú"><br>
                </form>'''
        else:
            return '''<br>Rellene los campos para enviar al servidor. Se validará sesión al mandar al servido<br>
                <form method="POST">
                  Fecha: <input type="date" name="date"><br>
                  Rango de edad: <input type="text" name="ageRange"><br>
                  Tipo de usuario: <input type="text" name="usertype"><br>
                  Id de la estación de origen: <input type="text" name="idunplug_station"><br>
                  Id de la estación de destino: <input type="text" name="idplug_station"><br>
                  Id de la base de origen: <input type="text" name="idunplug_base"><br>
                  Id de la base de destino: <input type="text" name="idplug_base"><br>
                  Tiempo del viaje en segundos: <input type="text" name="travel_time"><br>
                  Fichero: <input type="text" name="Fichero"><br>
                  <input type="submit" value="Enviar"><br>
                  Problema al insertar, inténtelo de nuevo.
              </form>'''

@app.route('/api/v1.0/bicimad/update', methods=['PUT'])
#http://127.0.0.1:6878/api/v1.0/bicimad/update
def update():
    #print(usuarioValidado)
    if request.method == 'PUT':
        Fecha = request.args.get('date')
        ageRange = request.args.get('ageRange')
        user_type = request.args.get('usertype')
        idunplug_station = request.args.get('idunplug_station')
        idplug_station = request.args.get('idplug_station')
        idunplug_base = request.args.get('idunplug_base')
        idplug_base = request.args.get('idplug_base')
        travel_time = request.args.get('travel_time')
        Fichero = request.args.get('Fichero')

        cursor = cnxn.cursor()
        cursor.execute('UPDATE bicimad SET travel_time = ? WHERE Fecha = ? AND ageRange = ? AND user_type = ? AND idunplug_station = ? AND idplug_station = ? AND idunplug_base = ? AND idplug_base = ? AND Fichero = ?', [travel_time,Fecha,ageRange,user_type,idunplug_station,idplug_station,idunplug_base,idplug_base,Fichero])
        cursor.commit()
        print(cursor)
        if cursor:
            return '''<form action="index">
                    <br>Update realizado.
                    <input type="submit" value="Menú"><br>
                </form>'''
        else:
            return "Error en la inserción, inténtelo de nuevo."
if __name__ == '__main__':
    app.run(port=6878)

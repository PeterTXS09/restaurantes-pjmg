from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL conexiones
app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'b203e369d03890'
app.config['MYSQL_PASSWORD'] = '9b778ac6'
app.config['MYSQL_DB'] = 'heroku_cd7e4cd69f65108'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    platos = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT orden.idorden, mesa.nombre_mesa, plato.nombre_plato FROM detalle, orden, mesa, plato WHERE detalle.idorden = orden.idorden and orden.idmesa = mesa.idmesa and detalle.idplato = plato.idplato')
    data = cur.fetchall()
    return render_template('index.html', datos = data)

@app.route('/crear-orden', methods=['POST'])
def Crear_orden():
    if request.method =='POST':
        mesa = request.form['mesa']
        print(mesa)
        plato = request.form['plato']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO ORDEN(idmesa) VALUES (%s)', [mesa])
        mysql.connection.commit()
        id = cur.lastrowid
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO DETALLE(idorden, idplato) VALUES (%s, %s)', [id, plato])
        mysql.connection.commit()
        flash('Orden creada correctamente')
        return redirect(url_for('Index'))

@app.route('/editar-orden/<id>')
def Editar_orden(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT orden.idorden, orden.idmesa, detalle.idplato FROM detalle, orden where orden.idorden = detalle.idorden and orden.idorden = %s LIMIT 1', [id])
    editar = cur.fetchall()
    mysql.connection.commit()
    return render_template('editar-orden.html', seleccionado = editar[0])

@app.route('/actualizar-orden/<id>', methods=['POST'])
def actualizar_orden(id):
    if request.method == 'POST':
        plato_old = request.form['plato_old']
        print('PLATO OLD: ', plato_old)
        mesa_old = request.form['mesa_old']
        mesa = request.form['mesa']
        print('MESA: ', mesa)
        orden = id
        print('ORDEN: ', orden)
        plato = request.form['plato']
        print('PLATO: ', plato)
        cur = mysql.connection.cursor()
        cur.execute('select iddetalle from detalle, orden where detalle.idplato = %s and orden.idmesa = %s LIMIT 1', [format(plato_old), format(orden)])
        detalle = cur.fetchall()
        print(detalle)
        cur = mysql.connection.cursor()
        cur.execute('UPDATE detalle SET idplato=%s WHERE idorden = %s', [format(plato), format(orden)])
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute('UPDATE orden SET idmesa=%s WHERE idorden = %s', [format(mesa), format(orden)])
        mysql.connection.commit()
        flash('Orden actualizada')
        return redirect(url_for('Index'))


@app.route('/eliminar-orden/<string:id>')
def Eliminar_orden(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT idorden from detalle where iddetalle = %s', [id])
    dato = cur.fetchall()
    mysql.connection.commit()
    cur = mysql.connection.cursor()
    cur.execute('DELETE From detalle WHERE iddetalle = %s', [id])
    mysql.connection.commit()
    cur.execute('DELETE From orden WHERE idorden = %s', [dato])
    mysql.connection.commit()
    flash('Orden eliminada')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = False)

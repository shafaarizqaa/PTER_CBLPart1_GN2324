from flask import Flask, render_template, url_for, redirect, request, flash
import sqlite3

def tableCheck(conn, tab_name) :
   query = f"""SELECT name FROM sqlite_master 
   WHERE type='table' AND name='{tab_name}'
   """
   conn.execute(query)
   return conn.fetchone() is not None 

def createTable() :
   db = sqlite3.connect('cars.db')
   dbCursor = db.cursor()

   if not(tableCheck(dbCursor, 'cars')) :
      query = """
         CREATE TABLE cars (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         brand VARCHAR NOT NULL,
         type VARCHAR NOT NULL,
         price INTEGER NOT NULL
         )
      """
      dbCursor.execute(query)
      return True
   else :
      return False

if createTable() == True:
   print('Berhasil membuat Table')

app = Flask(__name__)
app.secret_key = 'carslist'

def dbConn() :
   db = sqlite3.connect('cars.db')
   db.row_factory = sqlite3.Row
   return db

@app.route('/')
def index():
   conn = dbConn()
   datas = conn.execute("SELECT * FROM cars").fetchall()

   conn.close()

   return render_template('index.html', rows = datas)

@app.route('/add', methods = ["GET", "POST"])
def addCars() :
   if request.method == "POST" :
      cid = request.form['cid']
      cname = request.form['cname']
      ctype = request.form['ctype']
      cprice = request.form['cprice']

      if cid != '' and cname != '' and ctype != '' and cprice != '' :
         conn = dbConn()
         conn.execute(
            """
            INSERT INTO cars VALUES (
            ?, ?, ?, ?
            )
            """, (cid, cname, ctype, cprice)
         )
         conn.commit()
         conn.close()
         flash('Data Mobil Berhasil ditambahkan', 'success')
         return redirect(url_for('index'))
      else :
         flash('Data Mobil Gagal ditambahkan', 'failed')

   return render_template('addCars.html')

@app.route('/edit/<id>', methods = ["GET", "POST"])
def editCars(id) :
   conn = dbConn()
   data = conn.execute(f"SELECT * FROM cars WHERE id = {id}").fetchone()

   if request.method == "POST" :
      cname = request.form['cname']
      ctype = request.form['ctype']
      cprice = request.form['cprice']

      if cname != '' and ctype != '' and cprice != '' :
         conn = dbConn()
         conn.execute(
            f"""
            UPDATE cars SET 
            brand = ?, 
            type = ?, 
            price = ? 
            WHERE id = {id}
            """, (cname, ctype, cprice)
         )
         conn.commit()
         conn.close()
         flash('Data Mobil Berhasil diubah', 'success')
         return redirect(url_for('index'))
      else :
         flash('Data Mobil Gagal diubah', 'failed')

   return render_template('editCars.html', row = data)

@app.route('/delete/<id>')
def delete(id) :
   id = int(id)
   conn = dbConn()
   conn.execute(f"DELETE FROM cars WHERE id = {id}")
   conn.commit()
   conn.close()

   flash('Data Mobil Berhasil Dihapus', 'delsuccess')
   return redirect(url_for('index'))

app.run(debug=True)
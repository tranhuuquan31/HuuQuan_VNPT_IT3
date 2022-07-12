from flask import Flask, render_template, request, url_for, redirect
import sqlite3 as sql
app = Flask(__name__)

def dbconn():
    con = sql.connect("onlineshop.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    return cur

@app.route('/createdb',methods = ['POST', 'GET'])
def create():
    cur=dbconn()
    cur.execute("CREATE TABLE orders(item TEXT, price REAL, cust_name TEXT)")

    cur.execute("INSERT into orders (item, price, cust_name) values (?,?,?)",("Oximeter","50","Alice"))
    cur.execute("INSERT into orders (item, price, cust_name) values (?,?,?)",("Sanitizer","20","Paul"))
    cur.execute("INSERT into orders (item, price, cust_name) values (?,?,?)",("Mask","10","Anita"))
    cur.execute("INSERT into orders (item, price, cust_name) values (?,?,?)",("Sanitizer","20","Tara"))
    cur.execute("INSERT into orders (item, price, cust_name) values (?,?,?)",("Thermometer","30","Bob")) 
    cur.execute("INSERT into orders (item, price, cust_name) values (?,?,?)",("Mask","10","Alice")) 
    #return " Table is created."
    cur.execute("select * from orders")
    rows = cur.fetchall()
    return render_template("onlineshoprecords.html", rows = rows)

@app.route('/showtable',methods = ['GET','POST'])  
def showtable():  
    cur=dbconn()  
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    return render_template("onlineshoprecords.html", rows = rows)

@app.route("/query1",methods = ['GET','POST'])  
def query1():  
    cur=dbconn()
    res1=cur.execute("select sum(price) from orders")  
    return f' result is :{res1}'

if __name__ == '__main__':
   app.run(debug= True)
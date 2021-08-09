from flask import request
from flask.json import jsonify
from flask_mysqldb import MySQL
from config import app
import pymysql
from pymysql import connect,Error
# Connect to the MySQL Database Server
def connect ():
    try:
        with pymysql.connect(
            host="127.0.0.1",
            user="root",            
            password='',
            database="postett_local",
    ) as connection:
            return connection
    except Error as e:
        return e
    #mysql = MySQL(app)
    #con = mysql.connection
    #return con
@app.route('/', methods=['POST'])
def UpdateUser():
        con=connect()
        user = request.get_json()
        lastkey=list(user.keys())[-1]
        query="UPDATE users SET "
        for key in user:
            if (key!='id'):
                if (key==lastkey):

                    query=query+key+" = "+"'"+user[key]+"'"
                else:
                    query=query+key+" = "+"'"+user[key]+"'"+','
        query=query+" WHERE id = "+"'"+user['id']+"'"+";"    
        cur=con.cursor()
        print(query)
        #try:
        cur.execute(query)
        cur.close()
        con.close()
        return jsonify('success')
        #except Exception:
        cur.close()
        return jsonify('Error: unable to update items')        
if __name__ == '__main__':
    app.run()
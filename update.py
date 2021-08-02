from flask import request
from flask.json import jsonify
from flask_mysqldb import MySQL
from config import app
# Connect to the MySQL Database Server
def connect ():
    mysql = MySQL(app)
    con = mysql.connection
    return con
@app.route('/', methods=['POST'])
def UpdateUser():
        con=connect()
        cur=con.cursor()
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
        
        cur.execute(query)
        con.commit()
        cur.close()
        return jsonify('success') 
if __name__ == '__main__':
    app.run()
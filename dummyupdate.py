from flask.json import jsonify
import mysql.connector
from flask import request
from flask import Flask
 
app = Flask(__name__) 
@app.route('/', methods=['POST'])
def update():
    try:
        hostname = 'localhost'
        username = 'root'
        password = ''
        db_name  = 'postett_local'
        # Connect to DB
        database_connector = mysql.connector.connect(host=hostname,user=username,password=password,database=db_name)
        cursor=database_connector.cursor()
        user = request.get_json()
        lastkey=list(user.keys())[-1]
        query="UPDATE users SET "
        for key in user:
            if (key!="id"):
                if (key==lastkey):

                    query=query+key+" = "+"'"+user[key]+"'"
                else:
                    query=query+key+" = "+"'"+user[key]+"'"+','
        query=query+" WHERE id = "+"'"+user['id']+"'"+";"
        print(query)   
    
        cursor.execute(query)
        database_connector.commit()
        return jsonify("good update")
    except:
        return jsonify("error in update")
if __name__ == '__main__':
    app.run()
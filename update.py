from flask import request
from flask.json import jsonify
from config import app
import mysql.connector
from database.DBConnector import DBConnector
# Connect to the MySQL Database Server
def connectDB(query):
    try:
        connector = DBConnector()
        mydb = connector.connect_database()
        if mydb.is_connected():
            mycursor = mydb.cursor(dictionary=True)  # Creating a cursor object using
            mycursor.execute(query)
            mydb.commit()
            return jsonify("successfull update")


    except mysql.connector.Error as err:
        return f"Something went wrong: {err}"


    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            

@app.route('/', methods=['POST'])
def UpdateUser():
    

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
        result=connectDB(query)
        return result
       
if __name__ == '__main__':
    app.run()
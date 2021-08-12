from flask import request
from flask.json import jsonify
from config import app
import mysql.connector
from database.DBConnector import DBConnector
# Connect to the MySQL Database Server
def connectDB(select_query,update_query):
    try:
        connector = DBConnector()
        mydb = connector.connect_database()
        if mydb.is_connected():
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(select_query)
            selectresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                mycursor.execute(update_query)
                mydb.commit()
                return jsonify("successfull update")
            else:
                return jsonify("unregistered user")

    except mysql.connector.Error as err:
        return f"Something went wrong: {err}"
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            

@app.route('/', methods=['POST'])
def UpdateUser():
    

        user = request.get_json()
        select_query="SELECT * from users WHERE id = "+"'"+user['id']+"'"+";"

        lastkey=list(user.keys())[-1]
        update_query="UPDATE users SET "
        for key in user:
            if (key!='id'):
                if (key==lastkey):

                    update_query=update_query+key+" = "+"'"+user[key]+"'"
                else:
                    update_query=update_query+key+" = "+"'"+user[key]+"'"+','
        update_query=update_query+" WHERE id = "+"'"+user['id']+"'"+";"    
        result=connectDB(select_query,update_query)
        return result
       
if __name__ == '__main__':
    app.run()
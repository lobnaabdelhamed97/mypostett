from flask import request
from flask.json import jsonify
from config import app
import mysql.connector
from database.DBConnector import DBConnector
# Connect to the MySQL Database Server
def connectDB(select_query,edit_query,delete_query=""):
    try:
        connector = DBConnector()
        mydb = connector.connect_database()
        if mydb.is_connected():
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(select_query)
            selectresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                if(delete_query!=""):
                    mycursor.execute(delete_query)
                    mydb.commit()
                mycursor.execute(edit_query)
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
            
@app.route('/editAccount', methods=['POST'])
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
@app.route('/updateEmail', methods=['POST'])
def updateEmail():
    emaildetails=request.get_json()
    userid=emaildetails['user_id']
    marketingEmail=emaildetails['subscription_status']
    radioSelling=emaildetails['selling_notification']
    radioBuying=emaildetails['buying_notification']
    select_query="SELECT * from email_preferences WHERE user_id = "+"'"+emaildetails['user_id']+"'"+";"
    delete_query="DELETE FROM email_preferences WHERE user_id = "+"'"+emaildetails['user_id']+"'"+";"
    insert_query="INSERT INTO email_preferences(user_id,subscription_status,selling_notification,buying_notification) VALUES ("+userid+","+marketingEmail+","+radioSelling+","+radioBuying+");"
    result=connectDB(select_query,insert_query,delete_query)
    return result


if __name__ == '__main__':
    app.run()
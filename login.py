from config import app
from flask import jsonify,make_response
from flask_jwt import JWT, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from database.DBConnector import DBConnector

class User(object):	
	def __init__(self, id, username):
		self.id = id
		self.username = username

	def __str__(self):
		return "User(id='%s')" % self.id
@app.route('/rest-auth')
@jwt_required()
def get_response():
	return jsonify('You are an authenticate person to see this message')
def authenticate(username, password):	
	if username and password:
		try:
			connector = DBConnector()
			mydb = connector.connect_database()
			if mydb.is_connected():

			    mycursor = mydb.cursor(dictionary=True)
			    mycursor.execute("SELECT id, user_name, password FROM users WHERE user_name=%s", username)
			    row = mycursor.fetchone()
			
			if row:
				if row['password']==password:
				#if check_password_hash(row['password'], password):
                
					return User(row['id'], row['user_name'])
				else:
					return jsonify("wrong password")
			else:
				return jsonify("unregistered user")
		except mysql.connector.Error as err:
			return f"Something went wrong: {err}"
		finally:
			mycursor.close() 
			mydb.close()
	return None



def identity(payload):
	if payload['identity']:
		try:
			connector = DBConnector()
			mydb = connector.connect_database()
			if mydb.is_connected():

			    mycursor = mydb.cursor(dictionary=True)
			    mycursor.execute("SELECT id, user_name, password FROM users WHERE id=%s", payload['identity'])
			    row = mycursor.fetchone()
			
			if row:
				return (row['id'], row['user_name'])
			else:
				return None
		except Exception as e:
			print(e)
		finally:
			mycursor.close() 
			mydb.close()
	else:
		return None
	
jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":
    app.run()
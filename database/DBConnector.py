from flask.json import jsonify
import mysql.connector
#from flask import current_app as app
from config import app
import MySQLdb
import MySQLdb.cursors

class DBConnector:
    """
    Database Connector Class
    """

    
    def connect_database(self):
        hostname = app.config['MYSQL_HOST']
        username = app.config['MYSQL_USER']
        password = app.config['MYSQL_PASSWORD']
        db_name  = app.config['MYSQL_DB']
        # Connect to DB
        database_connector = mysql.connector.connect(host=hostname,user=username,password=password,database=db_name)  
        return database_connector
    

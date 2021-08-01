from flask import Flask,request,make_response,jsonify
import pymysql
from pymysql.cursors import Cursor
import hashlib
# Connect to the MySQL Database Server
dbIPAddresss   = "127.0.0.1"
dbUsr          = "root"
dbPwd          = ""
dbName          = "postett_local"
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def requests():
    mySQLConnection   = pymysql.connect(host=dbIPAddresss,
                                    user=dbUsr,
                                    password=dbPwd,
                                    db=dbName,
                                    autocommit=True)
    if request.method == "GET":
        return GetAllUsers(mySQLConnection)
    if request.method == "POST":
        user = request.get_json()
        cur = mySQLConnection.cursor()
        cur.execute("select * from users") 
        records = cur.fetchall()
        cur.close() 
        for row in records:
            if row[4] == user["user_name"]:
                return UpdateUser(mySQLConnection,user)

        return AddNewUser(mySQLConnection)
def UpdateUser(mySQLConnection,user):
        query="UPDATE users SET "
        lastkey=list(user.keys())[-1]
        for key in user:
            if (key==lastkey):
                query=query+key+" = "+"'"+user[key]+"'"+" WHERE user_name = "+"'"+user['user_name']+"'"+";"
            else:
                query=query+key+" = "+"'"+user[key]+"'"+','
            
        cur = mySQLConnection.cursor()
        cur.execute(query)        
        mySQLConnection.commit()
        cur.close()
        return 'success'        
def AddNewUser(mySQLConnection):
        details = request.get_json()
        newdict={}
        keys={'email','password','user_name','first_name','last_name','birthdate','gender','country','city','bio','default_payment','profile_img','address_1'}
        for key in keys:
            if key in details:
                if(key=='password'):
                    newdict[key]=hashlib.md5(details[key].encode()).hexdigest()
                else:
                    newdict[key]=details[key]
            else:
                newdict[key]=pymysql.NULL

        cur = mySQLConnection.cursor()
        cur.execute("INSERT INTO users(email,password,user_name,first_name,last_name,birthdate,gender,country,city,bio,default_payment,profile_img,address_1) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)", (newdict['email'], newdict['password'],newdict['user_name'],newdict['first_name'],newdict['last_name'],newdict['birthdate'],newdict['gender'],newdict['country'],newdict['city'],newdict['bio'],newdict['default_payment'],newdict['profile_img'],newdict['address_1']))
        mySQLConnection.commit()
        cur.close()
        return 'success'

def GetAllUsers(mySQLConnection):
        cursorObject    = mySQLConnection.cursor()

        try:
            getUserSQL = "select * from users"
    # Execute the SQL query for retrieving the user list from MySQL
            cursorObject.execute(getUserSQL)
    # Fetch all the user records
            sqlUsers = cursorObject.fetchall()
            Cursor.close()


        except Exception as e:
            print("Exeception occured:{}".format(e))
        finally:
            mySQLConnection.close()
        return make_response(jsonify(sqlUsers))

if __name__ == '__main__':
    app.run()
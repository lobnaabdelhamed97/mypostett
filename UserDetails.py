from flask import request,make_response
from flask.json import jsonify
from config import app
import mysql.connector
from database.DBConnector import DBConnector
# Connect to the MySQL Database Server
def connectDB(first_query,second_query,third_query,fourth_query):
    try:
        connector = DBConnector()
        mydb = connector.connect_database()
        if mydb.is_connected():
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(first_query)
            selectresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                mycursor.execute(second_query)
                secondresult=mycursor.fetchall()
                if mycursor.rowcount > 0:
                    mycursor.execute(third_query)
                    thirdresult=mycursor.fetchall()
                    if mycursor.rowcount > 0:
                        mycursor.execute(fourth_query)
                        fourthresult=mycursor.fetchall()
                        return make_response(jsonify(selectresult+secondresult+thirdresult+fourthresult))
                    else:
                        return jsonify("unsuccessful selection")
                else:
                    return jsonify("unsuccess selection")

            else:
                return jsonify("unsuccess selection")
        else:
            return jsonify("unsuccess selection")
    except mysql.connector.Error as err:
        return f"Something went wrong: {err}"
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

@app.route('/myDetails', methods=['GET'])
def GetDetails():
        user = request.get_json()

        first_query="select users.id, users.user_name, users.first_name, users.last_name, users.default_payment,users.birthdate,users.gender,users.country,users.city,city.city_name,city.city_id,country.country_name,country.iso from users \
             LEFT JOIN city on users.city = city.city_id \
             JOIN country on country.country_id=users.country WHERE users.id="+user['id']
        second_query="select brand.brand,fav_brand.bid,fav_brand.user_id from fav_brand JOIN brand on brand.bid=fav_brand.bid WHERE fav_brand.user_id="+user['id']
        
        third_query="select shipping_details.user_id,shipping_details.first_name, shipping_details.last_name, shipping_details.address1, shipping_details.address2, \
            shipping_details.postal_code,shipping_details.company_name,shipping_details.title,shipping_details.flag,shipping_details.MI, \
            shipping_details.region,shipping_details.country,city.city_name,city.city_id,country.country_id,country.country_name,country.iso from shipping_details \
             LEFT JOIN city on shipping_details.city = city.city_id \
             JOIN country on country.country_id=shipping_details.country WHERE shipping_details.user_id="+user['id']

        fourth_query="select billing_details.user_id,billing_details.first_name, billing_details.last_name, billing_details.address1, billing_details.address2, \
            billing_details.postal_code,billing_details.company_name,billing_details.title,billing_details.MI, \
            billing_details.region,billing_details.city,city.city_name,city.city_id,country.country_id,country.country_name,country.iso from billing_details \
             LEFT JOIN city on billing_details.city = city.city_id \
             JOIN country on country.country_id=billing_details.country WHERE billing_details.user_id="+user['id']


        fifth_query="select billing_details.user_id,billing_details.first_name, billing_details.last_name, billing_details.address1, billing_details.address2, \
        country.country_id,billing_details.postal_code, billing_details.company_name, billing_details.title, billing_details.MI,billing_details.region,country.iso,\
            city.city_name,city.city_id,country.country_name,billing_details.city from billing_details\
            LEFT JOIN city on billing_details.city = city.city_id \
            JOIN country on country.country_id=billing_details.country WHERE billing_details.user_id="+user['id']

            


        result=connectDB(first_query,second_query,third_query,fourth_query)
        return result
        
if __name__ == '__main__':
    app.run()


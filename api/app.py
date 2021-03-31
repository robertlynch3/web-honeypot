# api/app.py
# https://github.com/rml596/web-honeypot

from flask import request, Flask, Blueprint
from flask_restx import Api, Resource, fields
from functools import wraps
from time import time
from os import environ
import mysql.connector


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


dbconfig = {
        'user': 'root',
        'password': environ.get('MYSQL_ROOT_PASSWORD'),
        'host': environ.get('DATABASE_HOST'),
        'database': 'honeypot',
        'auth_plugin':'mysql_native_password'
    }

app=Flask(__name__)
blueprint=Blueprint('api', __name__, url_prefix='/api')
api=Api(blueprint, authorizations=authorizations, doc='/docs',version=1.0, title='Honeypot REST API', description='REST API to add events to the Honeypot database')
app.register_blueprint(blueprint)

post_login=api.model('login', {'ipAddress':fields.String(description='Source IP of attacker', required=True),
                             'userAgent': fields.String(description='User Agent', required=True),
                             'host': fields.String(description='host header', required=True),
                             'username': fields.String(description='Username used', required=True),
                             'password': fields.String(description='Password used', required=True)
                            })
post_load=api.model('load', {'ipAddress':fields.String(description='Source IP of attacker', required=True),
                             'userAgent': fields.String(description='User agent header', required=True),
                             'location': fields.String(description='Location header', required=True),
                             'host': fields.String(description='host header', required=True)
                            })


#adds decorators for the API Token, checks if the token exists. if it doesn't
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # checks to see if the token header is present in the header
        if 'X-API-KEY' in request.headers:
            token=request.headers["X-API-KEY"]
            # if the token is present, if the token is correct, the program continues
            # if the token is wrong, the user gets an error
            if token!=environ.get('API_TOKEN'):
                return {"Error": "Unauthorized Token"},401
        # if the token is not present the user receives an error.
        else:
            return {"Error": "Token missing."},401
        return f(*args, **kwargs)
    return decorated #Returns the arguments after confirming if the token is correct

@api.route('/load')
class Load(Resource):
    @api.doc(security='apikey', model=post_load) #documentation showing that this requeries a token
    @token_required #checks the token to confirm if it is valid or not
    @api.expect(post_load)
    def post(self):
        mydb = mysql.connector.connect(**dbconfig)
        #mydb = mysql.connector.connect(host="mysql", user='root', password='honeypotR00t', database="honeypot", auth_plugin='mysql_native_password')
        cursor=mydb.cursor(buffered=True,dictionary=True)
        
        #checks if the IP already exists
        cursor.execute("SELECT * FROM addresses WHERE ipAddress=\'{}\'".format(api.payload["ipAddress"]))
        if cursor.rowcount==0:
            #if the IP is not in the address table
            cursor.execute("INSERT INTO addresses (ipAddress) VALUES (\'{}\')".format(api.payload["ipAddress"]))
        #inserts into the load table. loads date as POSIX time
        cursor.execute("INSERT INTO loads (ipAddress, userAgent, location, date, host) VALUES (\'{}\', \'{}\', \'{}\',{}, \'{}\') ".format(api.payload["ipAddress"], api.payload["userAgent"], api.payload["location"], int(time()), api.payload["host"]))
        mydb.commit()
        cursor.close()
        mydb.close()

        return "Success",200
        
@api.route('/login')
class Login(Resource):
    @api.doc(security='apikey', model=post_login) #documentation showing that this requeries a token
    @token_required #checks the token to confirm if it is valid or not
    @api.expect(post_login)
    def post(self):
        mydb = mysql.connector.connect(**dbconfig)
        cursor=mydb.cursor(buffered=True,dictionary=True)
        
        #checks if the IP already exists
        cursor.execute("SELECT * FROM addresses WHERE ipAddress=\'{}\'".format(api.payload["ipAddress"]))
        if cursor.rowcount==0:
            #if the IP is not in the address table
            cursor.execute("INSERT INTO addresses (ipAddress) VALUES (\'{}\')".format(api.payload["ipAddress"]))
        #inserts into the load table. loads date as POSIX time
        cursor.execute("INSERT INTO login_attempts (ipAddress, username, password, userAgent, date, host) VALUES (\'{}\', \'{}\', \'{}\', \'{}\',{}, \'{}\')".format(api.payload["ipAddress"], api.payload["username"], api.payload["password"], api.payload["userAgent"], int(time()), api.payload["host"]))
        mydb.commit()
        cursor.close()
        mydb.close()

        return "Success",200



if __name__=="__main__":
    app.run(host="0.0.0.0", port=environ.get('PORT'))
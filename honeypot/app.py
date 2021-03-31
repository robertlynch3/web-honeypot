# honeypot/app.py
# https://github.com/rml596/web-honeypot


from flask import Flask, render_template, flash, request, redirect, url_for
from time import time
from os import environ
import mysql.connector



dbconfig = {
        'user': 'root',
        'password': environ.get('MYSQL_ROOT_PASSWORD'),
        'host': environ.get('DATABASE_HOST'),
        'database': 'honeypot',
        'auth_plugin':'mysql_native_password'
    }


app = Flask(__name__, template_folder="templates")

#creates a secret key for sessions, if this was a real app this would need to be secure. This just allows Flask to track
# sessions. It is used in login() when the app Flashes "Incorrect Credentials" (it does so by session)
app.secret_key='secret'

#redirects index to login
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #if you are running through a reverse proxy and please add the header `X-Forwarded-For`
        if 'X-Forwarded-For' in request.headers:
            remoteIP=request.headers['X-Forwarded-For']
        else:
            remoteIP=request.remote_addr
        post(ipAddress=remoteIP, host=request.headers.get('host'), username=username, password=password, userAgent=request.user_agent)
        flash("Incorrect Credentials",'danger')
        return render_template('login.html')
    else:
        #if you are running through a reverse proxy and please add the header `X-Forwarded-For`
        if 'X-Forwarded-For' in request.headers:
            remoteIP=request.headers['X-Forwarded-For']
        else:
            remoteIP=request.remote_addr
        get(ipAddress=remoteIP, host=request.headers.get('host'), userAgent=request.user_agent, location='index')
        return render_template('login.html')


#for any locations for /
@app.route('/<path:u_path>', methods=['GET', 'POST'])
def location(u_path):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #if you are running through a reverse proxy and please add the header `X-Forwarded-For`
        if 'X-Forwarded-For' in request.headers:
            remoteIP=request.headers['X-Forwarded-For']
        else:
            remoteIP=request.remote_addr
        post(ipAddress=remoteIP, host=request.headers.get('host'), username=username, password=password, userAgent=request.user_agent)
        flash("Incorrect Credentials",'danger')
        return render_template('login.html')
    else:
        #if you are running through a reverse proxy and please add the header `X-Forwarded-For`
        if 'X-Forwarded-For' in request.headers:
            remoteIP=request.headers['X-Forwarded-For']
        else:
            remoteIP=request.remote_addr
        get(ipAddress=remoteIP, host=request.headers.get('host'), userAgent=request.user_agent, location=u_path)
        return render_template('login.html')




#Static login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #if you are running through a reverse proxy and please add the header `X-Forwarded-For`
        if 'X-Forwarded-For' in request.headers:
            remoteIP=request.headers['X-Forwarded-For']
        else:
            remoteIP=request.remote_addr
        post(ipAddress=remoteIP, host=request.headers.get('host'), username=username, password=password, userAgent=request.user_agent)
        flash("Incorrect Credentials",'danger')
        return render_template('login.html')
    else:
        #if you are running through a reverse proxy and please add the header `X-Forwarded-For`
        if 'X-Forwarded-For' in request.headers:
            remoteIP=request.headers['X-Forwarded-For']
        else:
            remoteIP=request.remote_addr
        get(ipAddress=remoteIP, host=request.headers.get('host'), userAgent=request.user_agent, location='login')
        return render_template('login.html')



# Database component
def get(ipAddress, userAgent, location, host):
    if app.debug==True:
        return
    mydb = mysql.connector.connect(**dbconfig)
    #mydb = mysql.connector.connect(host="mysql", user='root', password='honeypotR00t', database="honeypot", auth_plugin='mysql_native_password')
    cursor=mydb.cursor(buffered=True,dictionary=True)
    
    #checks if the IP already exists
    cursor.execute("SELECT * FROM addresses WHERE ipAddress=\'{}\'".format(ipAddress))
    if cursor.rowcount==0:
        #if the IP is not in the address table
        cursor.execute("INSERT INTO addresses (ipAddress) VALUES (\'{}\')".format(ipAddress))
    #inserts into the load table. loads date as POSIX time
    cursor.execute("INSERT INTO loads (ipAddress, userAgent, location, date, host) VALUES (\'{}\', \'{}\', \'{}\',{}, \'{}\') ".format(ipAddress, userAgent, location, int(time()), host))
    mydb.commit()
    cursor.close()
    mydb.close()

def post(ipAddress, host, username, password, userAgent):
    if app.debug==True:
        return
    #mydb = mysql.connector.connect(host="mysql",user='root', password='honeypotR00t', database="honeypot", auth_plugin='mysql_native_password')
    mydb = mysql.connector.connect(**dbconfig)
    cursor=mydb.cursor(buffered=True,dictionary=True)
    
    #checks if the IP already exists
    cursor.execute("SELECT * FROM addresses WHERE ipAddress=\'{}\'".format(ipAddress))
    if cursor.rowcount==0:
        #if the IP is not in the address table
        cursor.execute("INSERT INTO addresses ipAddress VALUES \'{}\'".format(ipAddress))
    #inserts into the load table. loads date as POSIX time
    cursor.execute("INSERT INTO login_attempts (ipAddress, username, password, userAgent, date, host) VALUES (\'{}\', \'{}\', \'{}\', \'{}\',{}, \'{}\') ".format(ipAddress, username, password, userAgent, int(time()), host))
    mydb.commit()
    
    ### insert code to count how many times an IP has tried to login
    ###         then if it is past x amount of times, REST API to your firewall to block the address

    cursor.close()
    mydb.close()


if __name__=="__main__":
    app.run(host="0.0.0.0", port=environ.get('PORT'))
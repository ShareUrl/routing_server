from flask import Flask, render_template,request,json
from flaskext.mysql import MySQL
import string,random

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'Bucket'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/<url>")
def sendData(url):
    print url
    return render_template('navigate.html')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

@app.route("/url/<hashUrl>")
def sendUrl(hashUrl):
    query = "select tags from book where value=%s"
    args = (hashUrl)
    cursor.execute(query,args)
    # fetch all of the rows from the query
    data = cursor.fetchall()
    # print the rows
    #print data
    myData = ""
    for row in data:
        #log data
        #print row[0]
        myData = str(row[0])
    if len(myData) > 0:
        conn.commit()
        return  myData
    else:
        return "not cool"

@app.route('/createUrl',methods=['POST'])
def createUrl():
    data = request.get_data()
    val = id_generator()
    query = "INSERT INTO book(value,tags) VALUES(%s,%s);"
    args = (val,data)
    print val , data
    cursor.execute(query,args)
    happn = cursor.fetchall()
    if len(happn) is 0:
        conn.commit()
        return "successfully saved data"
    else:
        return json.dumps({'error':str(data[0])})

@app.errorhandler(404)
def page_not_found(e):
    # your processing here
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
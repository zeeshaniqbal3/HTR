from distutils.log import debug
from fileinput import filename
from flask import *
from flask_mysqldb import MySQL 
import easyocr 
app = Flask(__name__) 
from google.cloud import vision
import io
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/zeedeveloper/Desktop/HTR/hand-written-text-rec-84d1f61d78b3.json'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'z1122233n-'
app.config['MYSQL_DB'] = 'HTR'
mysql = MySQL(app)

@app.route('/contact', methods=['POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        # Create cursor
        cur = mysql.connection.cursor()
        
        # Execute query
        cur.execute("INSERT INTO response(name, email, subject, message) VALUES(%s, %s, %s, %s)", (name, email, subject, message))
        
        # Commit to database
        mysql.connection.commit()
        
        # Close connection
        cur.close()
        
        return 'Thanks for your feedback!'
    
    return render_template('index.html') 
  
@app.route('/')  
def main():  
    return render_template("index.html") 
@app.route('/about')  
def about():  
    return render_template("about.html")  
@app.route('/contact')  
def contact():  
    return render_template("contact.html")   
  
@app.route('/', methods = ['POST']) 
def success():  
    if request.method == 'POST':  
         image_file = request.files['file']
        # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    content = image_file.read()
    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    annotations = response.text_annotations

    if annotations:
        # Extract the detected text
        text = annotations[0].description

    return render_template("index.html", name = text)  
  
if __name__ == '__main__':  
    app.run(port=81, debug=False)
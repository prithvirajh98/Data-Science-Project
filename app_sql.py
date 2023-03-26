
import numpy as np
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb



gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]





from flask import Flask, request, jsonify, render_template

import joblib






# Load the model from the file 
model = joblib.load('final_pickle_model.pkl')  
  
# Use the loaded model to make predictions 



app = Flask(__name__)


@app.route('/register')
def home():
    return render_template('register.html')

        
@app.route('/register',methods=['POST'])
def register():
    

    int_features2 = [str(x) for x in request.form.values()]

    r1=int_features2[0]
    print(r1)
    
    r2=int_features2[1]
    print(r2)
    logu1=int_features2[0]
    passw1=int_features2[1]
        
    

    

   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root",'',"ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()


    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list1.append(str(row1[0]))
                      

                      
    print(gmail_list1)
    if logu1 in gmail_list1:
        return render_template('register.html',text="This Username is Already in Use ")

    else:

                  
              

# Prepare SQL query to INSERT a record into the database.
                  sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
                  val = (r1, r2)
   
                  try:
   # Execute the SQL command
                                       cursor.execute(sql,val)
   # Commit your changes in the database
                                       db.commit()
                  except:
   # Rollback in case there is any error
                                       db.rollback()

# disconnect from server
                  db.close()
                  return render_template('register.html',text="Succesfully Registered")


@app.route('/login')
def login(): 
    return render_template('login.html')         
                      


@app.route('/logedin',methods=['POST'])
def logedin():
    
    int_features3 = [str(x) for x in request.form.values()]
    print(int_features3)
    logu=int_features3[0]
    passw=int_features3[1]


    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root","","ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()

    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list.append(str(row1[0]))
                      

                      
    print(gmail_list)
    

    cursor1= db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2=cursor1.fetchall()

    for row2 in result2:
                      print(row2)
                      print(row2[0])
                      password_list.append(str(row2[0]))
                    
                      
    print(password_list)
    print(gmail_list.index(logu))
    print(password_list.index(passw))
    
    if gmail_list.index(logu)==password_list.index(passw):
        return render_template('index.html')
    else:
        return render_template('login.html',text='Use Proper Username and Password')
  
                                               


    
   


@app.route('/production')
def production(): 
    return render_template('index.html')


@app.route('/production/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [str(x) for x in request.form.values()]
    print(int_features)
    a=int_features

  


   
    temp = float(a[0])
    humidity=float(a[1])
    WindSpeed = float(a[2])
    Visibility =float(a[3])
    Pressure = float(a[4])
    so2=float(a[6])                       
    no2=float(a[7])
    Rainfall=float(a[5])
    pm10=float(a[8])
    pm2_5=float(a[9])
    

    data= {'Temperature':[temp],'Humidity':[humidity],'Wind Speed':[WindSpeed],'Visibility':[Visibility],'Pressure':[Pressure],'so2':[so2],'no2':[no2],'Rainfall':[Rainfall],'pm10':[pm10],'pm2_5':[pm2_5]} 
    df = pd.DataFrame(data)
      
# Print the output. 
    print(df )



    prediction=model.predict(df)
    prediction=int(prediction)


    

    if((prediction>=0) and (prediction<=50)):
        return render_template('index.html',prediction_text='Air Quality Index  is {}'.format(prediction),prediction_text1='Air Quality is Good')
        
        
    
    if((prediction>=51) and (prediction<=100)):
        return render_template('index.html',prediction_text='Air Quality Index   is {}'.format(prediction),prediction_text1='Air Quality is Moderate')
       
     
        
    if((prediction>=101) and (prediction<=150)):
        return render_template('index.html',prediction_text='Air Quality Index  is {}'.format(prediction),prediction_text1='Air Quality is Unhealthy')
       
       
        
    if((prediction>=151) and (prediction<=200)):
        return render_template('index.html',prediction_text='Air Quality Index   is {}'.format(prediction),prediction_text1='Air Quality is Unhealthy for Strong People')
        
        
    if(prediction>201):
        return render_template('index.html',prediction_text='Air Quality Index  is {}'.format(prediction),prediction_text1='Air Quality is Hazaradous')
       
        

       
    
if __name__ == "__main__":
    app.run(debug=False)

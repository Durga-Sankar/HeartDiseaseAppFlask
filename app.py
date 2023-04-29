from flask import Flask,jsonify,request
import pandas
import mysql.connector
from flask_cors import CORS
import joblib

# model = joblib.load("Randorm_Forest_Heart_Prediction.h5")

param=[]
# currentuser={
#     'name':'',
#     'email':'',
#     'password':''
# }

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/message", methods=['GET'])
def hello_world():
    return jsonify({'message':'It works'})

@app.route("/api/model" , methods=['POST'] )
def model_param():
   param=[]
   data = pandas.read_csv("testing (2)/testing/heart.csv")
   data = data.drop("target",axis=1)
   data = pandas.get_dummies(data,columns=['cp','restecg','slope','ca','thal'],drop_first=True)
   model_p={
   'age':request.json['age'],
   'trestbps':request.json['trestbps'],
   'chol':request.json['chol'],
   'thalach':request.json['thalach'],
   'oldpeak':request.json['oldpeak'],
   'sex_1':request.json['sex_1'],
   'cp_1':request.json['cp_1'],
   'cp_2':request.json['cp_2'],
   'cp_3':request.json['cp_3'],
   'fbs_1':request.json['fbs_1'],
   'restecg_1':request.json['restecg_1'],
   'restecg_2':request.json['restecg_2'],
   'exang_1':request.json['exang_1'],
   'Slope_1':request.json['Slope_1'],
   'Slope_2':request.json['Slope_2'],
   'ca_0':request.json['ca_0'],
   'ca_1':request.json['ca_1'],
   'ca_2':request.json['ca_2'],
   'ca_3':request.json['ca_3'],
   'thal_0':request.json['thal_0'],
   'thal_1':request.json['thal_1'],
   'thal_2':request.json['thal_2'],


    }
   param.append(model_p)
   data1=[[int(model_p['age']), int(model_p['trestbps']), int(model_p['chol']), int(model_p['thalach']), int(model_p['oldpeak']),
   int(model_p['sex_1']),int(model_p['cp_1']),int(model_p['cp_2']),int(model_p['cp_3']),int(model_p['fbs_1']),int(model_p['restecg_1']),int(model_p['restecg_2']),
    int(model_p['exang_1']),int(model_p['Slope_1']),int(model_p['Slope_2']),int(model_p['ca_0']),int(model_p['ca_1']),int(model_p['ca_2']),int(model_p['ca_3'])
    ,int(model_p['thal_0']),int(model_p['thal_1']),int(model_p['thal_2'])]]
   data1 = pandas.DataFrame(data1,columns=['age', 'sex', 'trestbps', 'chol', 'fbs', 'thalach', 'exang', 'oldpeak',
       'cp_1', 'cp_2', 'cp_3', 'restecg_1', 'restecg_2', 'slope_1', 'slope_2',
       'ca_1', 'ca_2', 'ca_3', 'ca_4', 'thal_1', 'thal_2', 'thal_3'])
   data = pandas.concat([data,data1])
   scaler = joblib.load('testing (2)/testing/scaler.save')
   data=scaler.fit_transform(data)
   req_data = data[-1]
   model=joblib.load('testing (2)/testing/GBmodel.h5')
   output=model.predict([req_data])



#    output=model.predict([[int(model_p['age']), int(model_p['trestbps']), int(model_p['chol']), int(model_p['thalach']), int(model_p['oldpeak']),
#    int(model_p['sex_1']),int(model_p['cp_1']),int(model_p['cp_2']),int(model_p['cp_3']),int(model_p['fbs_1']),int(model_p['restecg_1']),int(model_p['restecg_2']),
#    int(model_p['exang_1']),int(model_p['Slope_1']),int(model_p['Slope_2']),int(model_p['ca_0']),int(model_p['ca_1']),int(model_p['ca_2']),int(model_p['ca_3'])
#    ,int(model_p['thal_0']),int(model_p['thal_1']),int(model_p['thal_2'])]])
   return jsonify({'param':param},{'output':output.tolist()})
   

@app.route("/api/signin" , methods=['POST'] )
def signin():
    try:
        db=mysql.connector.connect(
        host="localhost",
        user='root',
        passwd='mysql@123',
        database="testdatabase"
        )
        mycursor=db.cursor()
        query = "insert into userdetails values(default,'"+ request.json['name'] +"','"+ request.json['email']+"','"+request.json['password']+"');"
        try:
            mycursor.execute(query)
            db.commit()
            # data=mycursor.fetchall()
            newuser={}
            newuser['name']=request.json['name']
            newuser['email']=request.json['email']
            newuser['password']=request.json['password']
            return jsonify(newuser)

        except mysql.connector.Error as err:
            print("Error occurred while fetching data:", err)
            return jsonify({'success':'false' , 'error':'true'})
    except mysql.connector.Error as err:
        print("Error occurred while connecting to the database:", err)
        return jsonify({'success':'false' , 'error':'true'})
    # currentuser['name']=request.json['name']
    # currentuser['email']=request.json['email']
    # currentuser['password']=request.json['password']
    # return jsonify(currentuser)

@app.route("/api/login" , methods=['POST'] )
def login():
    try:
        db=mysql.connector.connect(
        host="localhost",
        user='root',
        passwd='mysql@123',
        database="testdatabase"
        )
        mycursor=db.cursor()
        query = "select * from userdetails where email='"+request.json['email']+"';"
        try:
            mycursor.execute(query)
            data=mycursor.fetchall()

            # if (currentuser['email']==request.json['email'] and currentuser['password']==request.json['password']):
            #     return jsonify({'success':'true' , 'error':'false','currentuser':currentuser})
            # else:
            #     return jsonify({'success':'false' , 'error':'true'})

            if (data !=[]):
                currentuser={}
                currentuser['name']=data[0][1]
                currentuser['email']=data[0][2]
                currentuser['password']=data[0][3]
                return jsonify({'success':'true' , 'error':'false','currentuser':currentuser})
            else:
                return jsonify({'success':'false' , 'error':'true'})
        except mysql.connector.Error as err:
            print("Error occurred while fetching data:", err)
            return jsonify({'success':'false' , 'error':'true'})
    except mysql.connector.Error as err:
        print("Error occurred while connecting to the database:", err)
        return jsonify({'success':'false' , 'error':'true'})

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)

# from flask import Flask,jsonify,request
# from flask_cors import CORS
# import joblib
# model = joblib.load("Randorm_Forest_Heart_Prediction.h5")
# param=[]
# currentuser={
#     'name':'',
#     'email':'',
#     'password':''
# }


# app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# @app.route("/api/message", methods=['GET'])
# def hello_world():
#     return jsonify({'message':'It works'})
# @app.route("/api/model" , methods=['POST'] )
# def model_param():
#    param=[]
#    model_p={
#    'age':request.json['age'],
#    'trestbps':request.json['trestbps'],
#    'chol':request.json['chol'],
#    'thalach':request.json['thalach'],
#    'oldpeak':request.json['oldpeak'],
#    'sex_0':request.json['sex_0'],
#    'cp_0':request.json['cp_0'],
#    'sex_1':request.json['sex_1'],
#    'cp_1':request.json['cp_1'],
#    'cp_2':request.json['cp_2'],
#    'fbs_0':request.json['fbs_0'],
#    'restecg_0':request.json['restecg_0'],
#    'cp_3':request.json['cp_3'],
#    'fbs_1':request.json['fbs_1'],
#    'restecg_1':request.json['restecg_1'],
#    'exang_0':request.json['exang_0'],
#    'Slope_0':request.json['Slope_0'],
#    'restecg_2':request.json['restecg_2'],
#    'exang_1':request.json['exang_1'],
#    'Slope_1':request.json['Slope_1'],
#    'Slope_2':request.json['Slope_2'],
#    'ca_0':request.json['ca_0'],
#    'ca_1':request.json['ca_1'],
#    'ca_2':request.json['ca_2'],
#    'ca_3':request.json['ca_3'],
#    'thal_0':request.json['thal_0'],
#    'thal_1':request.json['thal_1'],
#    'thal_2':request.json['thal_2'],
#     }
#    param.append(model_p)
#    output=model.predict([[int(model_p['age']), int(model_p['trestbps']), int(model_p['chol']), int(model_p['thalach']), int(model_p['oldpeak']),
# #    int(model_p['sex_0']),int(model_p['cp_0']),int(model_p['cp_1']),int(model_p['cp_2']),int(model_p['fbs_0']),int(model_p['restecg_0']),int(model_p['restecg_1']),
# #    int(model_p['exang_0']),int(model_p['Slope_0']),int(model_p['Slope_1']),int(model_p['ca_0']),int(model_p['ca_1']),int(model_p['ca_2']),int(model_p['ca_3'])
#    int(model_p['sex_1']),int(model_p['cp_1']),int(model_p['cp_2']),int(model_p['cp_3']),int(model_p['fbs_1']),int(model_p['restecg_1']),int(model_p['restecg_2']),
#    int(model_p['exang_1']),int(model_p['Slope_1']),int(model_p['Slope_2']),int(model_p['ca_0']),int(model_p['ca_1']),int(model_p['ca_2']),int(model_p['ca_3'])
#    ,int(model_p['thal_0']),int(model_p['thal_1']),int(model_p['thal_2'])]])
#    return jsonify({'param':param},{'output':output.tolist()})


# @app.route("/api/signin" , methods=['POST'] )
# def signin():
#     currentuser['name']=request.json['name']
#     currentuser['email']=request.json['email']
#     currentuser['password']=request.json['password']
#     return jsonify(currentuser)

# @app.route("/api/login" , methods=['POST'] )
# def login():
#     if (currentuser['email']==request.json['email'] and currentuser['password']==request.json['password']):
#         return jsonify({'success':'true' , 'error':'false','currentuser':currentuser})
#     else:
#         return jsonify({'success':'false' , 'error':'true'})

# if __name__=='__main__':
#     app.run(debug=True)

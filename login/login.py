from flask import Flask
from flask import request, session ,redirect,url_for,flash,jsonify,render_template,url_for,request
import pymongo
import spacy




app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    #connect to data base
    myclient = pymongo.MongoClient('mongodb://192.168.0.44:27018')
    db_1 = myclient["List_user"]
    mycol = db_1["User"]

    message = ""
    res_data = {}
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        user = mycol.find_one({"username": f'{data["username"]}'})

        if user:
            user['_id'] = str(user['_id'])
            if user and user['password'] == data['password']:
                del user['password']
                message = f"user authenticated"
                code = 200
                status = "successful"
                res_data['username'] = user
                

            else:
                message = "wrong password"
                code = 401
                status = "fail"
                return jsonify({'status': status, "data": res_data, "message":message}), code 
        else:
            message = "invalid login details"
            code = 401
            status = "fail"
            return jsonify({'status': status, "data": res_data, "message":message}), code 

    except Exception as ex:
        message = f"{ex}"
        code = 500
        status = "fail"
    return jsonify({'status': status, "data": res_data, "message":message}), code 
    #return redirect(url_for('index')) 

@app.route('/process', methods=['POST'])
def process():
        
    nlp = spacy.load("en_core_web_sm")
    #Step 1 get the posted data
    postedData = request.get_json()

    #Step 2 is to read the data
    text1 = postedData["text1"]
    text2 = postedData["text2"]
    
    text1 = nlp(text1)
    text2 = nlp(text2)

    ratio = text1.similarity(text2)

    retJson = {"status":200, "ratio": ratio, "msg":"Similarity score calculated successfully"}
    
    return jsonify(retJson)


@app.route('/index')
def hello():
    
    return 'Welcome to my world'




######################################


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5002)
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
'''import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
import tensorflow.keras
from PIL import Image'''

cors = CORS(app, resources={r"/foo": {"origins":"*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

biodata = []
preferences = {}
interests = []
friends = []
incomingrequests = {}
outgoingrequests = {}








@app.route('/signup', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def signup():
    if request.method == "POST":

        data = request.get_json(force=True)
        username = data["username"]
        password = data["password"]
        firstname = data["firstname"]
        lastname = data["lastname"]
        email = data["email"]
        phoneno = data["phoneno"]
        gender = data["gender"]
        age = data["age"]
        occupation = data["occupation"]
        city = data["city"]
        state = data["state"]
        country = data["country"]

        pre = [int(data["p0"]), int(data["p1"]), int(data["p2"]), int(data["p3"]), int(data["p4"]), int(data["p5"]), int(data["p6"]), int(data["p7"]), int(data["p8"]), int(data["p9"])]
        data["interests"] = pre
        bio = [int(data["b0"]), int(data["b1"]), int(data["b2"]), int(data["b3"]), int(data["b4"]), int(data["b5"])]

        incomingrequests[username]=[]
        outgoingrequests[username]=[]
        preferences[username] = pre + bio
        data["friends"] = []

        for i in biodata:
            if username in i.values():
                print ("ERROR: Username already exists!!\n\n")
                return json.dumps({"type": "SIGNUP_ERROR","status":"201","error":"Couldnt sign in!!!"}), 201
        biodata.append(data)
        print (" the user name: ", username)
        print(data)
        return json.dumps({"payload":username, "status":200, "type":"SIGNUP_SUCCESS"}), 200

@app.route('/display', methods = ['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def display():
    if request.method == "GET":
        print(biodata)
    return "<h1>hi<\h1>"


@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        user = request.get_json(force=True)
        data = user['email']
        print (data)
        return "<h1>Success </h1>"
    if request.method == "GET":
        return "<h1>Hello, World! name </h1>"

@app.route('/user/<name>')
def user(name):
	return '<h1>Hello, {0}!</h1>'.format(name)

@app.route('/login', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login():
    if request.method == "POST":
        data = request.get_json(force=True)
        username = data["email"]
        password = data["password"]
        for i in biodata:
            if username in i.values():
                if password == i["password"]:
                    print('Success')
                    print (" the user name: ", username)
                    return json.dumps({"payload":username, "status":200, "type":"LOGIN_SUCCESS"}), 200
                else:
                    print('Wrong credentials')
            else:
                print('User does not exist')

    return json.dumps({"error":"Could not login in!!", "status":201, "type":"LOGIN_ERROR"}), 201

@app.route('/friendlist', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def friendlist():
    if request.method == "POST":
        data = request.get_json(force=True)
        for i in biodata:
            if data["username"] in i.values():

                print ("\n\n The friends are: ", i["friends"])
                return json.dumps({"payload":i["friends"], "status":200, "type":"FRIENDS_SUCCESS"}), 200


    return json.dumps({"payload":[], "status":201, "type":"FRIENDS_ERROR"}), 201



@app.route('/displayaccount', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def displayaccount():
    if request.method == "POST":
        data = request.get_json(Force=True)

        for i in biodata:
            if data["username"] in i.values():
                return json.dumps({"payload":i, "status":201, "type":"FRIENDS_ERROR"}), 201
    
    return json.dumps({"payload":[], "status":200, "type":"FRIENDS_ERROR"}), 200



@app.route('/editaccount', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def editaccount():
    if request.method == "POST":
        data = request.get_json(Force=True)

        pre = [int(data["p0"]), int(data["p1"]), int(data["p2"]), int(data["p3"]), int(data["p4"]), int(data["p5"]), int(data["p6"]), int(data["p7"]), int(data["p8"]), int(data["p9"])]
        bio = [int(data["b0"]), int(data["b1"]), int(data["b2"]), int(data["b3"]), int(data["b4"]), int(data["b5"])]

        for i in biodata:
            if data["username"] in i.values():
                i[pre[0]] = pre[0]
                i[pre[1]] = pre[1]
                i[pre[2]] = pre[2]
                i[pre[3]] = pre[3]
                i[pre[4]] = pre[4]
                i[pre[5]] = pre[5]
                i[pre[6]] = pre[6]
                i[pre[7]] = pre[7]
                i[pre[8]] = pre[8]
                i[pre[9]] = pre[9]

                i[bio[0]] = bio[0]
                i[bio[1]] = bio[1]
                i[bio[2]] = bio[2]
                i[bio[3]] = bio[3]
                i[bio[4]] = bio[4]
                i[bio[5]] = bio[5]

                print("Edited\n\n")
                return json.dumps({"status":200, "type":"EDIT_SUCCESS"}), 200


    print("Not edited\n\n\n")
    return json.dumps({"status":201, "type":"EDIT_FAILED"}), 201       




@app.route("/acceptfriend", methods = ["POST"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def friendaccept():
    if request.method == "POST":
        data = request.get_json(force=True)
        user = data["username"]
        friend = data["friendname"]


        for i in biodata:
            if user in i.values():
                print (user, "s friends are: ", i["friends"])
                if friend not in i["friends"]:
                    i["friends"].append(friend)
                    print ("\n\n\n", user, "s friends are: ", i["friends"])
                else:
                    print ("\n\n\n The friend already exists!!")
                    return json.dumps({"type":"ACCEPT_ERROR", "status":201}), 201

        for i in biodata:
            if friend in i.values():
                print (friend, "s friends are: ", i["friends"])
                i["friends"].append(user)
                print ("\n\n\n", user, "s friends are: ", i["friends"])


        #print (user, "s firends are: ", biodata[user])
    return "<h1> Might be working<\h1>"
    return json.dumps({"type":"ACCEPT_SUCCESS", "status":200, "payload":"LOGIN_ERROR"}), 201


@app.route('/sendrequest', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def sendrequest():
    data = request.get_json(force=True)
    user = data["username"]
    friendname = data["friendname"]
    


    for i in biodata:
        if user in i.values():
            if friendname not in outgoingrequests[user]:
                incomingrequests[friendname].append(user)
                outgoingrequests[user].append(friendname)
            else:
                print ("\n\n\n The friend already exists!!")
                return json.dumps({"type":"ACCEPT_ERROR", "status":201}), 201    

    print ("Sending a request...hopefully\n")

    print ("\n\n\n incomingrequests = ", incomingrequests)
    print ("\n\n\n outgoingrequests = ", outgoingrequests)

    return json.dumps({"type":"REQUEST_SUCCESS", "status":200}), 200


@app.route('/pendinginvites', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def pendinginvites():
    if request.method == "POST":
        data = request.get_json(force=True)
        user = data["username"]

        print(user)
    return json.dumps({"payload":incomingrequests[data["username"]], "status":200, "type":"INVITE_SUCCESS"}), 200


@app.route('/pendingoutgoing', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def pendingoutgoing():
    if request.method == "POST":
        data = request.get_json(force=True)

    return json.dumps({"payload":outgoingrequests[data["username"]], "status":200, "type":"OUTGOING_SUCCESS"}), 200



@app.route('/recommendedfriends', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def recommend():

    r={}
    data = request.get_json(force=True)
    user = data["username"]
    length=len(preferences[user])
    mypref=np.asarray(preferences[user])
    aa = mypref.reshape(1,length)
    otherusers=list(preferences.keys())

    print ("The other users are: ", otherusers, "\n\n\n\n")

    otherusers.remove(user)

    for i in biodata:
        if user in i.values():
            lis1 = i["friends"]
    for i in lis1:    
        otherusers.remove(i)

    for i in outgoingrequests[user]:
        otherusers.remove(i)

    for i in otherusers:
        otherpref=np.asarray(preferences[i])
        ba = otherpref.reshape(1,length)
        cos_lib = cosine_similarity(aa, ba)
        cosval=cos_lib[0][0]
        if cosval>0.4:
            r[i]=cosval
            print ("\n\nr = ", r.keys())
    recommend=[]
    key_list = list(r.keys())
    val_list=[]
    for i in r:
        val_list.append(float(r[i]))
    val_list.sort()
    recommend=sorted(r, key=r.__getitem__)

    


    print ("\n\n\n\n\n recomendations: \n\n\n", recommend)
    #except KeyError:
      #  print("wrong\n\n\n\n")
       # return json.dumps({"payload":[], "status":200, "type":"RECOMMEND_FAILURE"}), 200

    return json.dumps({"payload":recommend, "status":200, "type":"RECOMMEND_SUCCESS"}), 200


'''
@app.route('/pictures', methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def pictures():

    nparray = np.fromstring(request.data, np.uint8)
    image = cv2.imdecode(nparray, cv2.IMREAD_COLOR)

    cv2.imwrite("/home/ubuntu/hackathon/backend/")

    l=['Cars','Fashion','Food','Travel','Pets']
    np.set_printoptions(suppress=True)
    model = tensorflow.keras.models.load_model('keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


    image = image.resize((224, 224))
    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    i=0
    for x in np.nditer(prediction):

        if x>0.9:
                print (l[i])
                return json.dumps({"payload":l[i], "status":200, "type":"PICTURE_SUCCESS"}), 200 
        else:
                i=i+1
                return json.dumps({"payload":[], "status":201, "type":"PICTURE_FAIL"}), 201

    c0'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")

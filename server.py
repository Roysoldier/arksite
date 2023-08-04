from flask import Flask, jsonify, request, render_template, session, make_response
from os import urandom,path,remove
from lib import sqlitewrap, myLogger,sign
import traceback
import re
import datetime
from werkzeug.utils import secure_filename
from random import randint
import sys
import yaml
import yamlordereddictloader
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import json
import hashlib

ROOT_PATH = path.dirname(path.abspath(__file__)).strip() + "/"

CONFIG = {}

LOCK = threading.Lock()

lien =  r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[\w\-\./?#=&]+'

mydb = sqlitewrap.SqliteWrap(ROOT_PATH + "db/auth.db")

logger = myLogger.MyLogger(path=ROOT_PATH + "logs/messages.log")

debug = False

local = False

res,err = mydb.update_row("users",f"user = 'Noan'",f"level = '1'")
USERS = {}

###############################################
# Appel de fonction
###############################################

# Définition du nom de mon application Flask
APP_FLASK = Flask(__name__)

APP_FLASK.permanent_session_lifetime = datetime.timedelta(days=1)

# Rechargement des pages WEB automatiquement dès qu'on les change
APP_FLASK.config["TEMPLATES_AUTO_RELOAD"] = True
APP_FLASK.config["SESSION_COOKIE_HTTPONLY"] = False
APP_FLASK.config["REMEMBER_COOKIE_HTTPONLY"] = True
APP_FLASK.config["SESSION_COOKIE_SAMESITE"] = "Strict"
APP_FLASK.config['UPLOAD_FOLDER'] = "./static/data"

# Génération d'un secret de connexion utile à Falsk
APP_FLASK.secret_key = urandom(12)


@APP_FLASK.route('/', methods=['GET'])
@APP_FLASK.route('/index.html', methods=['GET'])
def index():
    try:
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=name,debug=debug)
        res,err = mydb.read_row("users",f"user = '{cook}'")
        if isConnect:
            render = {"login":isConnect,"pseudo":name,'img':res[0][8],"level":res[0][7]}
        else:
            render = {"login":isConnect}
        return render_template('index.html',render=render)
    except:
        logger.log("Erreur inconnue dans index.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/dino.html', methods=['GET'])
def dino():
    try:
       
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook=name
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=name,debug=debug)
        res,err = mydb.read_rows("dino",["id","name","level","nbr","stat","prix","img","type"])

        ires,ierr = mydb.read_row("users",f"user = '{cook}'")
        if isConnect:
            render = {"login":isConnect,"pseudo":name,"dino":res,'img':ires[0][8],"level":ires[0][7]}
        else:
            render = {"login":isConnect,"dino":res}

        return render_template('dino.html',render=render)
    except:
        logger.log("Erreur inconnue dans dino.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/objet.html', methods=['GET'])
def objet():
    try:
       
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook=name
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=name,debug=debug)
        res,err = mydb.read_rows("objet",["id","name","grade","nbr","stat","prix","img","type"])
        #print(res,err)
        ires,ierr = mydb.read_row("users",f"user = '{cook}'")
        if isConnect:
            render = {"login":isConnect,"pseudo":name,"dino":res,'img':ires[0][8],"level":ires[0][7]}
        else:
            render = {"login":isConnect,"dino":res}

        return render_template('objet.html',render=render)
    except:
        logger.log("Erreur inconnue dans objet.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/schema.html', methods=['GET'])
def schema():
    try:
       
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook=name
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=name,debug=debug)
        res,err = mydb.read_rows("schema",["id","name","grade","nbr","stat","prix","img","type"])
        #print(res,err)
        ires,ierr = mydb.read_row("users",f"user = '{cook}'")
        if isConnect:
            render = {"login":isConnect,"pseudo":name,"dino":res,'img':ires[0][8],"level":ires[0][7]}
        else:
            render = {"login":isConnect,"dino":res}

        return render_template('schema.html',render=render)
    except:
        logger.log("Erreur inconnue dans schema.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")


@APP_FLASK.route('/presd.html', methods=['GET'])
def presd(id):
    try:
       
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            ares,aerr = mydb.read_row("users",f"hashcook = '{cook}'")
            name = ares[0][1]
        cook = name
        recup_pp(id)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=name,debug=debug)
        res,err = mydb.read_row("dino",f"id = {id}")
        cres, cerr = mydb.read_row("commentaire",f"channel = '{name}_{id}'")
        ires,ierr = mydb.read_row("users",f"user = '{cook}'")
        channel,all = trie_channel(name,id,'dino')
        if isConnect:
            render = {"login":isConnect,"pseudo":name,"dino":res[0], "commentaire":cres,"level":ares[0][7],"channel":channel,"all":all,"id":id,'img':ires[0][8]}
        else:
            render = {"login":isConnect,"dino":res[0]}
        return render_template('presd.html',render=render)
    except:
        logger.log("Erreur inconnue dans presd.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/preso.html', methods=['GET'])
def preso(id):
    try:
       
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            ares,aerr = mydb.read_row("users",f"hashcook = '{cook}'")
            name = ares[0][1]
        cook = name
        recup_pp(id)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=name,debug=debug)
        res,err = mydb.read_row("objet",f"id = {id}")
        cres, cerr = mydb.read_row("commentaire",f"channel = 'obj_{name}_{id}'")
        ires,ierr = mydb.read_row("users",f"user = '{cook}'")
        channel,all = trie_channel(name,id,'objet')
        #print(channel)
        if isConnect:
            render = {"login":isConnect,"pseudo":name,"dino":res[0], "commentaire":cres,"level":ares[0][7],"channel":channel,"all":all,"id":id,'img':ires[0][8]}
        else:
            render = {"login":isConnect,"dino":res[0]}
        return render_template('preso.html',render=render)
    except:
        logger.log("Erreur inconnue dans presd.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")



@APP_FLASK.route('/press.html', methods=['GET'])
def press(id):
    try:
      
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            ares,aerr = mydb.read_row("users",f"hashcook = '{cook}'")
            name = ares[0][1]
        cook = name
        recup_pp(id)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=name,debug=debug)
        res,err = mydb.read_row("objet",f"id = {id}")
        cres, cerr = mydb.read_row("commentaire",f"channel = 'sch_{name}_{id}'")
        ires,ierr = mydb.read_row("users",f"user = '{cook}'")
        channel,all = trie_channel(name,id,'schema')
        
        if isConnect:
            render = {"login":isConnect,"pseudo":name,"dino":res[0], "commentaire":cres,"level":ares[0][7],"channel":channel,"all":all,"id":id,'img':ires[0][8]}
        else:
            render = {"login":isConnect,"dino":res[0]}
        return render_template('press.html',render=render)
    except:
        logger.log("Erreur inconnue dans press.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")


@APP_FLASK.route('/add.html', methods=['GET'])
def add():
    try:
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=name,debug=debug)
        ires,ierr = mydb.read_row("users",f"user = '{cook}'")
        if isConnect:
            render = {"login":isConnect,"pseudo":name,'img':ires[0][8],"level":ires[0][7]}
            return render_template('add.html',render=render)
        else:
            render = {"login":isConnect}
            return index()
    except:
        logger.log("Erreur inconnue dans add.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/signin.html', methods=['GET'])
def signin():
    try:
        if debug:
            logger.log("Requête signin.html", "DEBUG")
        #renvoie du code source signin.html au navigateur web après traitement
        return render_template('signin.html')
    except:
        logger.log("Erreur inconnue dans signin.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/signup.html', methods=['GET'])
def signup():
    try:
        if debug:
            logger.log("Requête signup.html", "DEBUG")
        #renvoie du code source signup.html au navigateur web après traitement
        return render_template('signup.html')
    except:
        logger.log("Erreur inconnue dans signup.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")


@APP_FLASK.route('/editprofil.html', methods=['GET'])
def editprofil():
    try:
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        ires,ierr = mydb.read_row("users",f"user = '{cook}'")
        print(ires)
        render = {"login":isConnect,"pseudo":cook,"img": f"{ires[0][8]}","level":ires[0][7],"tribu": f"{ires[0][9]}"}
        #print("render : ",render)
        if debug:
            logger.log("Requête editprofil.html", "DEBUG")
        #renvoie du code source editprofil.html au navigateur web après traitement
        if isConnect:
           return render_template('editprofil.html', render=render)
        else:
            return index()
    except:
        logger.log("Erreur inconnue dans editprofil.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

###############################################
# API
##############################################0

@APP_FLASK.route('/api/signout', methods = ['POST'])
def api_signout():
    try:
        cook = request.cookies.get('USER_ID',"")
        payload = request.json
        res,err = mydb.read_row("users",f"hashcook = '{cook}'")
        name = res[0][1]
        sign.sign_out(logger=logger,mydb=mydb,pseudo=name,debug=debug)
        logger.log(payload["message"],"INFO")
        return jsonify({"status":"ok","msg":'cool'})
    except:
        logger.log("Erreur inconnue dans api/signout", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    
@APP_FLASK.route('/api/comment', methods=['POST'])
def api_comment():
    try:
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        if isConnect:
            payload = request.json
            maxid,err= mydb.max_index('commentaire',"id")
            res,err = mydb.add_row("commentaire",[("id",maxid[0][0] + 1),("user",cook),("project",payload['id']),("content",payload['comment']),("img",res[0][8]),("channel",f"{payload['name']}"),("category",payload['cat'])])
            return jsonify({"status":"ok","msg":'opérationel'})
        else:
            return jsonify({"status":"nok","msg":'Merci de vous connecter'})  
    except:
        logger.log("Erreur inconnue dans api_commment", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    

@APP_FLASK.route('/api/getcomment', methods=['POST'])
def api_getcomment():
    try:
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
       
        if isConnect:
            payload = request.json
            recup_ppp(payload['id'])
            res,err = mydb.read_row("commentaire",f"channel = '{payload['id']}'")
            return jsonify({"status":"ok","msg":'opérationel',"data":res})
        else:
            return jsonify({"status":"nok","msg":'Merci de vous connecter',"data":[]})  
    except:
        logger.log("Erreur inconnue dans api_getcommment", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error',"data":[]})
    

@APP_FLASK.route('/api/denum', methods=['POST'])
def api_denum_dino():
    try:
        
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        payload = request.json
        res,err = mydb.read_row("dino",f"id = '{payload['id']}'")
        res,err = mydb.update_row("dino",f"id = '{payload['id']}'",f"nbr = '{int(res[0][3]) - 1}'")
        res,err = mydb.read_row("dino",f"id = '{payload['id']}'")
       
        if int(res[0][3]) <= 0:
            channel,all = trie_channel(name,payload['id'],'dino')
            for i in channel:
                res,err = mydb.delete_row('commentaire',('channel',i))
            res,err = mydb.delete_row('dino',('id',payload['id']))
            return jsonify({"status":"final","msg":'opérationel'})
        return jsonify({"status":"ok","msg":'opérationel'})
    except:
        logger.log("Erreur inconnue dans  api_denum_dino", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})


@APP_FLASK.route('/api/renum', methods=['POST'])
def api_renum_dino():
    try:
        
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        payload = request.json
        res,err = mydb.read_row("dino",f"id = '{payload['id']}'")
        res,err = mydb.update_row("dino",f"id = '{payload['id']}'",f"nbr = '{int(res[0][3]) + 1}'")
        return jsonify({"status":"ok","msg":'opérationel'})
    except:
        logger.log("Erreur inconnue dans  api_renum_obj", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    

@APP_FLASK.route('/api/denumobj', methods=['POST'])
def api_denum_obj():
    try:
        
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        payload = request.json
        res,err = mydb.read_row("objet",f"id = '{payload['id']}'")
        res,err = mydb.update_row("objet",f"id = '{payload['id']}'",f"nbr = '{int(res[0][3]) - 1}'")
        res,err = mydb.read_row("objet",f"id = '{payload['id']}'")
        if int(res[0][3]) <= 0:
            channel,all = trie_channel(name,payload['id'],'objet')
            for i in channel:
                res,err = mydb.delete_row('commentaire',('channel',i))
            res,err = mydb.delete_row('objet',('id',payload['id']))
            return jsonify({"status":"final","msg":'opérationel'})
        return jsonify({"status":"ok","msg":'opérationel'})
    except:
        logger.log("Erreur inconnue dans  api_denum_dobj", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})



@APP_FLASK.route('/api/renumobj', methods=['POST'])
def api_renum_obj():
    try:
        
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        payload = request.json
        res,err = mydb.read_row("objet",f"id = '{payload['id']}'")
        res,err = mydb.update_row("objet",f"id = '{payload['id']}'",f"nbr = '{int(res[0][3]) + 1}'")
        return jsonify({"status":"ok","msg":'opérationel'})
    except:
        logger.log("Erreur inconnue dans  api_renum_obj", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    

@APP_FLASK.route('/api/denumsch', methods=['POST'])
def api_denum_sch():
    try:
        
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        payload = request.json
        res,err = mydb.read_row("schema",f"id = '{payload['id']}'")
        res,err = mydb.update_row("schema",f"id = '{payload['id']}'",f"nbr = '{int(res[0][3]) - 1}'")
        res,err = mydb.read_row("schema",f"id = '{payload['id']}'")
        if int(res[0][3]) <= 0:
            channel,all = trie_channel(name,payload['id'],'schema')
            for i in channel:
                res,err = mydb.delete_row('commentaire',('channel',i))
            res,err = mydb.delete_row('shema',('id',payload['id']))
            return jsonify({"status":"final","msg":'opérationel'})
        return jsonify({"status":"ok","msg":'opérationel'})
    except:
        logger.log("Erreur inconnue dans  api_denum_sch", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})

@APP_FLASK.route('/api/renumsch', methods=['POST'])
def api_renum_sch():
    try:
        
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        payload = request.json
        res,err = mydb.read_row("shema",f"id = '{payload['id']}'")
        res,err = mydb.update_row("shema",f"id = '{payload['id']}'",f"nbr = '{int(res[0][3]) + 1}'")
        return jsonify({"status":"ok","msg":'opérationel'})
    except:
        logger.log("Erreur inconnue dans  api_renum_sch", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})


@APP_FLASK.route('/api/tribu', methods=['POST'])
def api_tribu():
    try:
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = request.cookies.get('USER_ID',"")
        #print("cook :",cook)
        payload = request.json
        res,err = mydb.update_row("users",f"user = '{name}'",f"tribu = '{payload['tribu']}'")
        logger.log("Tribu modifier", "INFO")
        return jsonify({"status":"ok","data":{'tribu':payload['tribu']}})
    except:
        logger.log("Erreur inconnue dans api_bio", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})


@APP_FLASK.route('/api/signup', methods=['POST'])
def api_signup():
    try:
        if debug:
            logger.log("Requête api_signup", "DEBUG")
            result = sign.signup(logger=logger,mydb=mydb,payload=request.json,debug=debug,bypass=False,verif=CONFIG['scheduler']['enable'],lock=LOCK,path=ROOT_PATH)
        return jsonify(result)
    except:
        logger.log("Erreur inconnue dans api_signup", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    
@APP_FLASK.route('/api/signin', methods=['POST'])
def api_signin():
    try:
       
        if debug:
            logger.log("Requête api_signin", "DEBUG")
        
        result,user = sign.signin(logger=logger,mydb=mydb,email=request.json['email'],pwd=request.json['password'],debug=debug)
        if user['auth']:
            binarykey = bytes(user['user'] + "nroydevencryptagecookie", "utf-8")
            hashcook = hashlib.sha256(binarykey).hexdigest()
            res,err = mydb.update_row("users",f"user = '{user['user']}'",f"hashcook = '{hashcook}'")

            resp = make_response(jsonify (result))  
            if not local:
                resp.set_cookie('USER_ID',hashcook,path="/",domain="nroydev.fr", httponly=True, secure=True)  
            else:
                resp.set_cookie('USER_ID',hashcook,path="/", httponly=True, secure=True)  
            
        return resp
    except:
        logger.log("Erreur inconnue dans api_signin", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    
@APP_FLASK.route('/uploader', methods = ['POST'])
def upload_file():
    try:
      
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]

        f = request.files['file']
        name = request.form['name-dino'].replace("'","£")
        level = request.form['level-dino']
        nbr = request.form['nbr-dino']
        stat = request.form['stat-dino'].replace("'","£")
        prix = request.form['prix-dino'].replace("'","£")
        sexe = request.form['sexe']
        description = request.form['story'].replace("'","£")
        type = request.form['type']
        if type == "Tribu":
            type = res[0][9]
        
        if f and name and level and nbr and stat and prix and sexe and description:
            f.save(path.join(APP_FLASK.config['UPLOAD_FOLDER'],f"{cook}_{f.filename}"))
            res,err = mydb.max_index('dino',"id")
            res,err = mydb.add_row("dino",{('id',res[0][0] + 1),('name',name),('level',level),('nbr',nbr),('stat',stat),('prix',prix),('img',f"{cook}_{f.filename}"),('sexe',sexe),('description',description),('type',type)})
            
        logger.log("Fichier uploader", "INFO")
    except:
        logger.log("Erreur inconnue dans upload_file", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
    return add()

@APP_FLASK.route('/objuploader', methods = ['POST'])
def objupload_file():
    try:
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]

        f = request.files['file']
        name = request.form['name-dino'].replace("'","£")
        level = request.form['level-dino']
        nbr = request.form['nbr-dino']
        stat = request.form['stat-dino'].replace("'","£")
        prix = request.form['prix-dino'].replace("'","£")
        type = request.form['type']
        if type == "Tribu":
            type = res[0][9]
        
        if f and name and level and nbr and stat and prix:
            f.save(path.join(APP_FLASK.config['UPLOAD_FOLDER'],f"{cook}_{f.filename}"))
            res,err = mydb.max_index('objet',"id")
            res,err = mydb.add_row("objet",{('id',res[0][0] + 1),('name',name),('grade',level),('nbr',nbr),('stat',stat),('prix',prix),('img',f"{cook}_{f.filename}"),('type',type)})
            #print(res,err)
        logger.log("Fichier uploader", "INFO")
    except:
        logger.log("Erreur inconnue dans objupload_file", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
    return add()

@APP_FLASK.route('/shuploader', methods = ['POST'])
def shupload_file():
    try:
      
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]

        f = request.files['file']
        name = request.form['name-dino'].replace("'","£")
        level = request.form['level-dino']
        nbr = request.form['nbr-dino']
        stat = request.form['stat-dino'].replace("'","£")
        prix = request.form['prix-dino'].replace("'","£")
        type = request.form['type']
        
        if f and name and level and nbr and stat and prix:
            f.save(path.join(APP_FLASK.config['UPLOAD_FOLDER'],f"{cook}_{f.filename}"))
            res,err = mydb.max_index('schema',"id")
            res,err = mydb.add_row("schema",{('id',res[0][0] + 1),('name',name),('grade',level),('nbr',nbr),('stat',stat),('prix',prix),('img',f"{cook}_{f.filename}"),('type',type)})
        logger.log("Fichier uploader", "INFO")
    except:
        logger.log("Erreur inconnue dans shjupload_file", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
    return add()


@APP_FLASK.route('/ppuploader', methods = ['POST'])
def ppupload_file():
    try:
 
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]
        cook = name
        res,err = mydb.read_row("users",f"user = '{cook}'")

        f = request.files['file']
        if f:
            #print(f)
            if res[0][8] != "circle-person.png":
                remove(f"./static/data/{res[0][8]}")
            f.save(path.join(APP_FLASK.config['UPLOAD_FOLDER'],f"{cook}_{f.filename}"))

            res,err = mydb.update_row("users",f"user = '{cook}'",f"img = '{cook}_{f.filename}'")
        logger.log("Fichier uploader", "INFO")
    except:
        logger.log("Erreur inconnue dans ppupload_file", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
    return editprofil()


@APP_FLASK.route('/uploaderchoice', methods = ['POST'])
def upload_choice():
    try:

        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]

        id = request.form['id']

    except:
        logger.log("Erreur inconnue dans upload_choice", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
    return presd(id)

@APP_FLASK.route('/uploaderchoiceobj', methods = ['POST'])
def upload_choiceobj():
    try:

        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]

        id = request.form['id']

    except:
        logger.log("Erreur inconnue dans upload_choiceobj", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
    return preso(id)

@APP_FLASK.route('/uploaderchoicesch', methods = ['POST'])
def upload_choicesch():
    try:
       
        cook = request.cookies.get('USER_ID',"")
        name = ""
        if cook != "":
            res,err = mydb.read_row("users",f"hashcook = '{cook}'")
            name = res[0][1]

        id = request.form['id']
    except:
        logger.log("Erreur inconnue dans upload_choicesch", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
    return press(id)
###############################################
# Fonctions
###############################################
def trie_channel(name,id,cat):
    name = []
    res,err = mydb.read_row("commentaire",f"project = '{id}'")
    for i in res:
        #print(i,i[6])
        if i[6] == cat:
            if i[5] not in name:
                name.append(i[5])
    return name, res


def recup_pp(proj):
    cres, cerr = mydb.read_row("commentaire",f"project = '{proj}'")
    for i in cres:
      res,err = mydb.read_row("users",f"user = '{i[1]}'")
      res,err = mydb.update_row("commentaire",f"user = '{i[1]}'",f"img = './static/data/{res[0][8]}'")  
    cres, cerr = mydb.read_row("commentaire",f"project = '{proj}'")
def recup_ppp(proj):
    cres, cerr = mydb.read_row("commentaire",f"channel = '{proj}'")
    for i in cres:
      res,err = mydb.read_row("users",f"user = '{i[1]}'")
      res,err = mydb.update_row("commentaire",f"user = '{i[1]}'",f"img = './static/data/{res[0][8]}'")  
    cres, cerr = mydb.read_row("commentaire",f"project = '{proj}'")
def check_account():
    try:
        logger.log("Check périodique", "INFO")
        with LOCK:
            with open(ROOT_PATH +  "account_verif.json","r") as f:
                tmp_account = json.load(f)
            to_remove = []
            for i,v in enumerate(tmp_account):
                if v['verif']:
                    logger.log(f"Création du compte : {v['pseudo']}, après validation", "INFO")
                    result = sign.signup(logger=logger,mydb=mydb,payload=v,debug=debug,bypass=True,verif=False,lock=LOCK,path=ROOT_PATH)
                    to_remove.append(i)
            to_remove.sort(reverse=True)
            for i in to_remove:
                del tmp_account[i]
            with open(ROOT_PATH +  "account_verif.json","w") as f:
                f.write(json.dumps(tmp_account, indent=4))

    except:
        logger.log("Erreur inconnue dans check_account", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
###############################################
# Main 
##############################################0
if __name__ == '__main__':
    try:
        with open(ROOT_PATH + "config.yaml", "r") as f:
            CONFIG = yaml.load(f, Loader=yamlordereddictloader.Loader)
    except IOError:
        logger.log("Erreur dans le fichier de config", "ERROR")
        sys.exit()
    debug = CONFIG.get('debug',False)
    local = CONFIG.get('local',False)
    logger.log("Création de la base de donnée", "INFO")
    mydb.create_table("users",[("id","INTEGER"),("user","TEXT"),("email","TEXT"),("mdp","TEXT"),("lastlog","INTEGER"),("connected","INTEGER"),("hashcook","TEXT"),("level","TEXT"),('img','TEXT'),("tribu","TEXT")])
    mydb.create_table("dino",[("id","INTEGER"),("name","TEXT"),("level","TEXT"),("nbr","TEXT"),("stat","TEXT"),("prix","TEXT"),("img","TEXT"),("sexe","TEXT"),("description","TEXT"),("type","TEXT")])
    mydb.create_table("objet",[("id","INTEGER"),("name","TEXT"),("grade","TEXT"),("nbr","TEXT"),("stat","TEXT"),("prix","TEXT"),("img","TEXT"),("type","TEXT")])
    mydb.create_table("schema",[("id","INTEGER"),("name","TEXT"),("grade","TEXT"),("nbr","TEXT"),("stat","TEXT"),("prix","TEXT"),("img","TEXT"),("type","TEXT")])
    mydb.create_table("commentaire",[("id","INTEGER"),("user","TEXT"),("project","TEXT"),("content","TEXT"),('img',"TEXT"),("channel","TEXT"),("category","TEXT")])
    if CONFIG['scheduler']['enable']:
        scheduler = BackgroundScheduler()
        job = scheduler.add_job(check_account, 'interval', minutes=CONFIG['scheduler']['interval'])
        scheduler.start()
    #logger.log("Démarrage du serveur flask", "INFO")
    APP_FLASK.run(ssl_context=(ROOT_PATH + 'ssl/cert.cer',ROOT_PATH + 'ssl/key.key'),host = CONFIG['network']['ip'], port = CONFIG['network']['port'])
    #APP_FLASK.run(host = CONFIG['network']['ip'], port = CONFIG['network']['port'])
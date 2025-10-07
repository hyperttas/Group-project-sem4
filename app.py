from flask import render_template, jsonify, request, Flask, session, redirect, url_for
from flask_session import Session
import os
from werkzeug.utils import secure_filename
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import mysql.connector


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_DIR"] = "./sessions"

Session(app)

mydb = mysql.connector.connect(
  #host="localhost",
  host=os.environ.get('DB_URL'),
  user=os.environ.get('DB_USERNAME'),
  password=os.environ.get('DB_PASS'),
  auth_plugin="caching_sha2_password",
)

ALLOWED_EXTENSIONS_SCRIPTS = {"py", "sig"}
ALLOWED_EXTENSIONS_TASKS = {"json"}

MAX_FILE_SIZE = 5 * 1024 * 1024
SCRIPTS_FOLDER = 'scripts'
TASKS_FOLDER = 'tasks'

app.config["SCRIPTS_FOLDER"] = SCRIPTS_FOLDER
os.makedirs(SCRIPTS_FOLDER, exist_ok=True)
app.config["TASKS_FOLDER"] = TASKS_FOLDER
os.makedirs(TASKS_FOLDER, exist_ok=True)

def allowed_file_scripts(filename: str) -> bool:
    if request.content_length <= MAX_FILE_SIZE:
        if  "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS_SCRIPTS:
            return True
    return False

def allowed_file_tasks(filename: str) -> bool:
    if request.content_length <= MAX_FILE_SIZE:
        if  "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS_TASKS:
            return True
    return False

def valid_task(data):
    if len(data) == 2 and "script_name" in data and "payload" in data:
        for i in data["payload"]:
            for j in i:
                if not type(j) is int:
                    return False
        return True
    return False

def check_signature(script, signature):
    with open("public_key.pem", "rb") as f:
        pem_data = f.read()
    public_key = serialization.load_pem_public_key(pem_data)

    try:
        public_key.verify(
            signature,
            script,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except:
        return False
    

@app.route('/', methods=['GET'])
def home():
    if session:
        return render_template("home.html")

    return render_template ("No_access.html")

@app.route('/login', methods=['GET'])
def login_get():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get("password")

    try:
        db_cursor = mydb.cursor()
        db_cursor.execute("USE cybergrouppr")
        user = db_cursor.execute("Select * from Users where username = %s;", (username,))
        user = db_cursor.fetchone()
        mydb.commit()
        db_cursor.close()
        if user:
            if password == user[2]:
                
                session["username"] = user[1]
                session["role"] = user[3]
                
                return redirect(url_for("home"))
            else:
                return jsonify({"status": "error", "message": "Invalid credentials"}), 401
        else:
            return jsonify({"status": "error", "message": "User do not exists"}), 401
    except mysql.connector.Error as err:
        db_cursor.close()
        return jsonify({"status": "error", "message": "Database error"}), 500

@app.route('/logout', methods=['GET'])
def logout_get():
    session.clear()
    return redirect(url_for("login_get"))

@app.route('/upload_script', methods=['GET'])
def upload_script_get():
    if session:
        if session["role"] in ["admin", "uploader"]:
            return render_template("upload_script.html")
    
    return render_template ("No_access.html")

@app.route('/upload_script', methods=['POST'])
def upload_script_post():
    if session:
        if session["role"] in ["admin", "uploader"]:
            files = request.files.getlist("script")

            if len(files) != 2:
                return jsonify({"Error": 'Upload exactly script and signature'}), 400

            for i in files:
                if not allowed_file_scripts(i.filename):
                    return jsonify({"Error": 'Invalid file size (below 5MB) or type (only .py or .sig allowed)!'}), 400
            
            
            if files[0].filename[-4:] == '.sig':
                script_file = files[1]
                signature = files[0]
            else:
                script_file = files[0]
                signature = files[1]
            
            script_file_bytes = script_file.read()
            signature_bytes = signature.read()

            script_file.seek(0)
            signature.seek(0)

            if not check_signature(script_file_bytes, signature_bytes):
                return jsonify({"Error": 'Invalid file!'}), 400

            filename = secure_filename(script_file.filename)
            save_path = os.path.join(app.config["SCRIPTS_FOLDER"], filename)
            script_file.save(save_path)

            return jsonify({"message": 'Files uploaded successfully!'}), 200
        
    return jsonify({"Error": 'Unaythorized access!'}), 400

@app.route('/upload_task', methods=['GET'])
def upload_task_get():
    if session:
        if session["role"] in ["admin", "uploader"]:
            return render_template("upload_task.html")
        
    return render_template ("No_access.html")

@app.route('/upload_task', methods=['POST'])
def upload_task_post():
    if session:
        if session["role"] in ["admin", "uploader"]:
            file = request.files.get("task")
            content = file.read().decode('utf-8')

            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                print("Invalid JSON syntax:", e)
                return jsonify({"Error": 'Invalid file size type (only .json allowed)!'}), 400
            
            if not allowed_file_tasks(file.filename):
                return jsonify({"Error": 'Invalid file size (below 5MB) or type (only .json allowed)!'}), 400
            
            if not valid_task(data):
                return jsonify({"Error": 'Invalid file format!'}), 400

            file.seek(0)
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["TASKS_FOLDER"], filename)
            file.save(save_path)

            return jsonify({"message": 'Files uploaded successfully!'}), 200
        
    return jsonify({"Error": 'Unaythorized access!'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
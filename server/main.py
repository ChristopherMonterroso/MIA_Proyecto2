from flask import Flask, jsonify, request
from flask_cors import CORS
from lib.command_Execute import *
import boto3
from dotenv import load_dotenv
app = Flask(__name__)
CORS(app)
load_dotenv()

aws_key = os.getenv("ACCESS_KEY")
aws_id = os.getenv("ACCESS_ID")
bucket_name = os.getenv("BUCKET_NAME")
@app.route("/commands/mkdisk", methods=["POST"])
def mkdisk():
    print("Command mkdisk")
    tokens = request.json["tokens"]
    
    response = command_mkdisk(tokens)
    return jsonify(response)

@app.route("/commands/rmdisk", methods=["POST"])
def rmdisk():
    print("Command rmdisk")
    tokens = request.json["tokens"]
    
    response = command_rmdisk(tokens)
    return jsonify(response)

@app.route("/commands/fdisk", methods=["POST"])
def fdisk():
    print("Command fdisk")
    tokens = request.json["tokens"]
    response = command_fdisk(tokens)
    print(response)
    return jsonify(response)

@app.route("/commands/mount", methods=["POST"])
def mount():
    print("Command mount")
    tokens = request.json["tokens"]
    response = command_mount(tokens)
    return jsonify(response)

@app.route("/commands/unmount", methods=["POST"])
def unmount():
    print("Command unmount")
    tokens = request.json["tokens"]
    response = command_unmount(tokens)
    return jsonify(response)

@app.route("/commands/rep", methods=["POST"])
def rep():
    print("Command rep")
    tokens = request.json["tokens"]
    response = command_rep(tokens, aws_id, aws_key, bucket_name)
    print(response)
    return jsonify(response)

@app.route("/reports/all", methods=["GET"])
def all_reports():
    
    s3 = boto3.client('s3', aws_access_key_id=aws_id, aws_secret_access_key=aws_key)            

    reportes = []
    # Lista los objetos en el bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    try:
        for obj in response['Contents']:
            reportes.append(obj['Key'])
    except KeyError:
        pass
    
    data ={
        "error":"false",
        "status":"200",
        "message":"Reportes extraidos con exito",
        "reports":reportes
    }
    return jsonify(data)
@app.route("/prueba", methods=["GET"])
def prueba():

    return jsonify({"message":aws_id+" "+aws_key+" "+bucket_name})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

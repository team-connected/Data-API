# Import required dependencies
from flask import Flask, jsonify, abort, make_response, request
from pymongo import MongoClient
from bson.json_util import dumps
import json
import uuid
import os
import pyfiglet

# Example URI: 'mongodb://host1,host2,host3', replicaSet='rs0'
conUri = os.getenv("conUri", "localhost:27017")
db_name = os.getenv("db_name", "EPD")

#Print some usefull information to console
ascii_banner = pyfiglet.figlet_format("UMC Data-API")
print(ascii_banner)
print("Starting API Server")
print("API Server Version: V1.0")
print("Developed by: Haydn Felida, Jeroen Verkerk, Sam Zandee, Shaniah Arrias, Maarten Mol. (All rights reserved)")

#Setup MongoDB Client
client = MongoClient(conUri)
db = client[db_name]

#Define app with Flask
app = Flask(__name__)

#Define error function for JSON error response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "notFound"}), 404)

#Define the root
@app.route("/")
def index():
    return "Please use the V1 API! Developed by: Haydn Felida, Jeroen Verkerk, Sam Zandee, Shaniah Arrias, Maarten Mol. (All rights reserved)"

#Define GET PATIENTS
@app.route("/api/v1/patient/", methods=['GET'])
def get_patients():
    try:
        patient = db.Patient.find().sort([( '$natural', -1 )] )
        return dumps(patient), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET NURSES
@app.route("/api/v1/nurse/", methods=['GET'])
def get_nurses():
    try:
        nurse = db.Nurse.find().sort([( '$natural', -1 )] )
        return dumps(nurse), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET DEVICES
@app.route("/api/v1/device/", methods=['GET'])
def get_devices():
    try:
        device = db.Device.find()
        return dumps(device), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET METRICS from a PATIENT
@app.route('/api/v1/metric/patient=<value>', methods=['GET'])
def get_metrics(value):
    try:
        if db.Patient.count_documents({ "_id" : value }, limit = 1) == 1:
            metrics = db.Patient.find_one({ "_id" : value },{"metrics":1})
            metric = db.Metric.find({"_id":{"$in":metrics["metrics"]}}).sort([( 'timestamp', -1 )] )
            return dumps(metric), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"getMetrics" : "userNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET PATIENT
@app.route('/api/v1/patient/<field>=<value>', methods=['GET'])
def get_patient(field, value):
    try:
        if db.Patient.count_documents({ field : value }, limit = 1) == 1:
            patient = db.Patient.find({ field : value })
            return dumps(patient), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"getPatient" : "patientNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET METRIC
@app.route('/api/v1/metric/<field>=<value>', methods=['GET'])
def get_metric(field, value):
    try:
        if db.Metric.count_documents({ field : value }, limit = 1) == 1:
            metric = db.Metric.find({ field : value })
            return dumps(metric), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"getMetric" : "metricNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET NURSE
@app.route('/api/v1/nurse/<field>=<value>', methods=['GET'])
def get_nurse(field, value):
    try:
        if db.Nurse.count_documents({ field : value }, limit = 1) == 1:
            nurse = db.Nurse.find({ field : value })
            return dumps(nurse), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"getNurse" : "nurseNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET DEVICE
@app.route('/api/v1/device/<field>=<value>', methods=['GET'])
def get_device(field, value):
    try:
        if db.Device.count_documents({ field : value }, limit = 1) == 1:
            device = db.Device.find({ field : value })
            return dumps(device), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"getDevice" : "deviceNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define CREATE PATIENT
@app.route('/api/v1/patient/', methods=['POST'])
def create_patient():
    try:
        data = json.loads(request.data)
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        street = data['street']
        city = data['city']
        location = data['location']
        uid = uuid.uuid4().hex
        if db.Patient.count_documents({ 'email': email }, limit = 1) == 0:
            status = db.Patient.insert_one({
                "_id" : uid,
                "firstname" : firstname,
                "lastname" : lastname,
                "email" : email,
                "street" : street,
                "city" : city,
                "location" : location,
                "metrics" : [ ]
            })
            return jsonify({"createPatient" : "success"}), 201, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"createPatient" : "patientEmailDuplicate"}), 403, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define CREATE NURSE
@app.route('/api/v1/nurse/', methods=['POST'])
def create_nurse():
    try:
        data = json.loads(request.data)
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        department = data['department']
        uid = uuid.uuid4().hex
        if db.Nurse.count_documents({ 'email': email }, limit = 1) == 0:
            status = db.Nurse.insert_one({
                "_id" : uid,
                "firstname" : firstname,
                "lastname" : lastname,
                "email" : email,
                "department" : department
            })
            return jsonify({"createNurse" : "success"}), 201, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"createNurse" : "nurseEmailDuplicate"}), 403, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define CREATE DEVICE
@app.route('/api/v1/device/', methods=['POST'])
def create_device():
    try:
        data = json.loads(request.data)
        name = data['name']
        type = data['type']
        sn = data['sn']
        status = data['status']
        uid = uuid.uuid4().hex
        if db.Device.count_documents({ 'sn': sn }, limit = 1) == 0:
            status = db.Device.insert_one({
                "_id" : uid,
                "name" : name,
                "type" : type,
                "sn" : sn,
                "status" : status
            })
            return jsonify({"createDevice" : "success"}), 201, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"createDevice" : "deviceSerialNumberDuplicate"}), 403, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define CREATE METRIC
@app.route('/api/v1/metric/patient=<id>', methods=['POST'])
def create_metric(id):
    try:
        data = json.loads(request.data)

        # Do not require the following fields:
        if "bloeddruk" in data:
            bloeddruk = data['bloeddruk']
            device_bloeddruk = data['device_bloeddruk']
        else:
            bloeddruk = 0
            device_bloeddruk = ' '
        
        if "gewicht" in data:
            gewicht = data['gewicht']
            device_gewicht = data['device_gewicht']
        else:
            gewicht = 0
            device_gewicht = ' '
        
        if "temperatuur" in data:
            temperatuur = data['temperatuur']
            device_temperatuur = data['device_temperatuur']
        else:
            temperatuur = 0
            device_temperatuur = ' '

        if "pijnscore" in data:
            pijnscore = data['pijnscore']
        else:
            pijnscore = 0

        if "comment" in data:
            comment = data['comment']
        else:
            comment = ""

        # Require these fields
        timestamp = data['timestamp']
        nurse_id = data['nurse_id']
        
        uid = uuid.uuid4().hex
        if db.Patient.count_documents({ '_id': id }, limit = 1) == 1 and db.Nurse.count_documents({ '_id': nurse_id }, limit = 1) == 1:
            status = db.Metric.insert_one({
                "_id" : uid,
                "bloeddruk" : bloeddruk,
                "gewicht" : gewicht,
                "temperatuur" : temperatuur,
                "pijnscore" : pijnscore,
                "device_bloeddruk" : device_bloeddruk,
                "device_gewicht" : device_gewicht,
                "device_temperatuur" : device_temperatuur,
                "timestamp" : timestamp,
                "nurse_id" : nurse_id,
                "comment" : comment
            })
            newValues = { "metrics": uid }
            db.Patient.update_one({ "_id" : id }, { "$push" : newValues })
            return jsonify({"createMetric" : uid}), 201, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"createMetric" : "patientOrNurseNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define UPDATE PATIENT
@app.route('/api/v1/patient/id=<value>', methods=['PUT'])
def update_patient(value):
    try:
        if db.Patient.count_documents({ "_id" : value }, limit = 1) == 1:
            data = json.loads(request.data)
            newValues = {}
            if "firstname" in data:
                firstname = data['firstname']
                newValue = { "firstname": firstname }
                newValues.update(newValue)
            if "lastname" in data:
                lastname = data['lastname']
                newValue = { "lastname": lastname }
                newValues.update(newValue)
            if "email" in data:
                email = data['email']
                newValue = { "email": email }
                newValues.update(newValue)
            if "street" in data:
                street = data['street']
                newValue = { "street": street }
                newValues.update(newValue)
            if "city" in data:
                city = data['city']
                newValue = { "city": city }
                newValues.update(newValue)
            if "location" in data:
                location = data['location']
                newValue = { "location": location }
                newValues.update(newValue)           
            db.Patient.update_one({ "_id" : value }, { "$set" : newValues })
            return jsonify({"updatePatient" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"updatePatient" : "patientNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define UPDATE NURSE
@app.route('/api/v1/nurse/id=<value>', methods=['PUT'])
def update_nurse(value):
    try:
        if db.Nurse.count_documents({ "_id" : value }, limit = 1) == 1:
            data = json.loads(request.data)
            newValues = {}
            if "firstname" in data:
                firstname = data['firstname']
                newValue = { "firstname": firstname }
                newValues.update(newValue)
            if "lastname" in data:
                lastname = data['lastname']
                newValue = { "lastname": lastname }
                newValues.update(newValue)
            if "email" in data:
                email = data['email']
                newValue = { "email": email }
                newValues.update(newValue)
            if "department" in data:
                department = data['department']
                newValue = { "department": department }
                newValues.update(newValue)           
            db.Nurse.update_one({ "_id" : value }, { "$set" : newValues })
            return jsonify({"updateNurse" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"updateNurse" : "nurseNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define UPDATE METRIC
@app.route('/api/v1/metric/id=<id>', methods=['PUT'])
def update_metric(id):
    try:
        if db.Metric.count_documents({ "_id" : id }, limit = 1) == 1:
            data = json.loads(request.data)
            newValues = {}
            if "bloeddruk" in data:
                bloeddruk = data['bloeddruk']
                newValue = { "bloeddruk": bloeddruk }
                newValues.update(newValue)
            if "gewicht" in data:
                gewicht = data['gewicht']
                newValue = { "gewicht": gewicht }
                newValues.update(newValue)
            if "temperatuur" in data:
                temperatuur = data['temperatuur']
                newValue = { "temperatuur": temperatuur }
                newValues.update(newValue)
            if "device_bloeddruk" in data:
                device_bloeddruk = data['device_bloeddruk']
                newValue = { "device_bloeddruk": device_bloeddruk }
                newValues.update(newValue)
            if "device_gewicht" in data:
                device_gewicht = data['device_gewicht']
                newValue = { "device_gewicht": device_gewicht }
                newValues.update(newValue)
            if "device_temperatuur" in data:
                device_temperatuur = data['device_temperatuur']
                newValue = { "device_temperatuur": device_temperatuur }
                newValues.update(newValue)
            if "pijnscore" in data:
                pijnscore = data['pijnscore']
                newValue = { "pijnscore": pijnscore }
                newValues.update(newValue)
            if "timestamp" in data:
                timestamp = data['timestamp']
                newValue = { "timestamp": timestamp }
                newValues.update(newValue)
            if "device_id" in data:
                device_id = data['device_id']
                newValue = { "device_id": device_id }
                newValues.update(newValue)
            if "nurse_id" in data:
                nurse_id = data['nurse_id']
                newValue = { "nurse_id": nurse_id }
                newValues.update(newValue)
            if "value" in data:
                value = data['value']
                newValue = { "value": value }
                newValues.update(newValue)
            if "comment" in data:
                comment = data['comment']
                newValue = { "comment": comment }
                newValues.update(newValue)        
            db.Metric.update_one({ "_id" : id }, { "$set" : newValues })
            return jsonify({"updateMetric" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"updateMetric" : "metricNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define UPDATE DEVICE
@app.route('/api/v1/device/sn=<value>', methods=['PUT'])
def update_device(value):
    try:
        if db.Device.count_documents({ "sn" : value }, limit = 1) == 1:
            data = json.loads(request.data)
            newValues = {}
            if "name" in data:
                name = data['name']
                newValue = { "name": name }
                newValues.update(newValue)
            if "type" in data:
                type = data['type']
                newValue = { "type": type }
                newValues.update(newValue)
            if "sn" in data:
                new_sn = data['new_sn']
                newValue = { "sn": new_sn }
                newValues.update(newValue)
            if "status" in data:
                status = data['status']
                newValue = { "status": status }
                newValues.update(newValue)
            db.Device.update_one({ "sn" : value }, { "$set" : newValues })
            return jsonify({"updateDevice" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"updateDevice" : "deviceNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define DELETE METRIC with ID
@app.route('/api/v1/metric/patient=<id>/id=<value>', methods=['DELETE'])
def delete_metric(id, value):
    try:
        if db.Metric.count_documents({ "_id" : value }, limit = 1) == 1 and db.Patient.count_documents({ "_id" : id }, limit = 1) == 1:
            db.Workouts.delete_one({ "_id" : value })
            newValues = { "metrics": value }
            db.Patient.update_one({ "_id" : id }, { "$pull" : newValues })
            return jsonify({"deleteMetric" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"deleteMetric" : "patientOrMetricNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define DELETE DEVICE with SN
@app.route('/api/v1/device/sn=<value>', methods=['DELETE'])
def delete_device(value):
    try:
        if db.Device.count_documents({ "sn" : value }, limit = 1) == 1:
            db.Device.delete_one({ "sn" : value })
            return jsonify({"deleteDevice" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"deleteDevice" : "deviceNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define DELETE NURSE with ID
@app.route('/api/v1/nurse/id=<value>', methods=['DELETE'])
def delete_nurse(value):
    try:
        if db.Nurse.count_documents({ "_id" : value }, limit = 1) == 1:
            db.Nurse.delete_one({ "_id" : value })
            return jsonify({"deleteNurse" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"deleteNurse" : "nurseNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define DELETE PATIENT with ID
@app.route('/api/v1/patient/id=<value>', methods=['DELETE'])
def delete_patient(value):
    try:
        if db.Patient.count_documents({ "_id" : value }, limit = 1) == 1:
            db.Patient.delete_one({ "_id" : value })
            return jsonify({"deletePatient" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"deletePatient" : "patientNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define main APP
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
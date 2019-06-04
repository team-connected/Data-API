#Import required dependencies
from flask import Flask, jsonify, abort, make_response, request
from pymongo import MongoClient
from bson.json_util import dumps
import json
import uuid
import os

#db_ip = os.getenv("db_ip", "Maarten-NB")
#db_port = os.getenv("db_port", "27017")
# Example URI: 'mongodb://host1,host2,host3', replicaSet='rs0'
conUri = os.getenv("conUri", "maarten-nb:27017")
db_name = os.getenv("db_name", "MAF")

#Print some usefull information to console
print("Starting API Server")
print("API Server Version: V1.0")
print("Developed by: Maarten Mol (All rights reserved)")

#Setup MongoDB Client
#client = MongoClient(db_ip + ":" + db_port)
client = MongoClient(conUri)
db = client[db_name]

#Define app with Flask
app = Flask(__name__)

#Define error function for JSON error response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

#Define the root
@app.route("/")
def index():
    return "Please use the V1 API! Developed by: Maarten Mol (All rights reserved)"

#Define GET PATIENTS
@app.route("/api/v1/patient", methods=['GET'])
def get_patients():
    try:
        patient = db.Patient.find()
        return dumps(patient), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET NURSES
@app.route("/api/v1/nurse", methods=['GET'])
def get_nurses():
    try:
        nurse = db.Nurse.find()
        return dumps(nurse), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET DEVICES
@app.route("/api/v1/device", methods=['GET'])
def get_devices():
    try:
        device = db.Device.find()
        return dumps(nurse), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define GET METRICS from a PATIENT
@app.route('/api/v1/metric/email=<email>', methods=['GET'])
def get_metrics(email):
    try:
        if db.Patient.count_documents({ "email" : email }, limit = 1) == 1:
            metrics = db.Patient.find_one({ "email" : email },{"metrics":1})
            metric = db.Metric.find({"_id":{"$in":metrics["metrics"]}})
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
@app.route('/api/v1/patient', methods=['POST'])
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
                "location" : location
            })
            return jsonify({"createPatient" : "success"}), 201, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"createPatient" : "patientEmailDuplicate"}), 403, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define CREATE NURSE
@app.route('/api/v1/nurse', methods=['POST'])
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
@app.route('/api/v1/device', methods=['POST'])
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
@app.route('/api/v1/metric/patient=<email>', methods=['POST'])
def create_metric(email):
    try:
        data = json.loads(request.data)
        metric_type = data['metric_type']
        timestamp = data['timestamp']
        device_id = data['device_id']
        nurse_id = data['nurse_id']
        value = data['value']
        comment = data['distance']
        uid = uuid.uuid4().hex
        if db.Patient.count_documents({ 'email': email }, limit = 1) == 1 and db.Nurse.count_documents({ '_id': nurse_id }, limit = 1) == 1:
            status = db.Metric.insert_one({
                "_id" : uid,
                "metric_type" : metric_type,
                "timestamp" : timestamp,
                "device_id" : device_id,
                "nurse_id" : nurse_id,
                "value" : value,
                "comment" : comment
            })
            newValues = { "metrics": uid }
            db.Patient.update_one({ "email" : email }, { "$push" : newValues })
            return jsonify({"createMetric" : "success"}), 201, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"createMetric" : "patientOrNurseNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define UPDATE PATIENT
@app.route('/api/v1/patient/email=<value>', methods=['PUT'])
def update_patient(value):
    try:
        if db.Patient.count_documents({ "email" : value }, limit = 1) == 1:
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
            db.Patient.update_one({ "email" : value }, { "$set" : newValues })
            return jsonify({"updatePatient" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"updatePatient" : "patientNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define UPDATE NURSE
@app.route('/api/v1/nurse/email=<value>', methods=['PUT'])
def update_nurse(value):
    try:
        if db.Nurse.count_documents({ "email" : value }, limit = 1) == 1:
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
            db.Nurse.update_one({ "email" : value }, { "$set" : newValues })
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
            if "metric_type" in data:
                metric_type = data['metric_type']
                newValue = { "metric_type": metric_type }
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
@app.route('/api/v1/metric/patient=<email>/id=<value>', methods=['DELETE'])
def delete_metric(email, value):
    try:
        if db.Metric.count_documents({ "_id" : value }, limit = 1) == 1 and db.Patient.count_documents({ "email" : email }, limit = 1) == 1:
            db.Workouts.delete_one({ "_id" : value })
            newValues = { "metrics": value }
            db.Patient.update_one({ "email" : email }, { "$pull" : newValues })
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

#Define DELETE NURSE with EMAIL
@app.route('/api/v1/nurse/email=<value>', methods=['DELETE'])
def delete_nurse(value):
    try:
        if db.Nurse.count_documents({ "email" : value }, limit = 1) == 1:
            db.Nurse.delete_one({ "email" : value })
            return jsonify({"deleteNurse" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"deleteNurse" : "nurseNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define DELETE PATIENT with EMAIL
@app.route('/api/v1/patient/email=<value>', methods=['DELETE'])
def delete_patient(value):
    try:
        if db.Patient.count_documents({ "email" : value }, limit = 1) == 1:
            db.Patient.delete_one({ "email" : value })
            return jsonify({"deletePatient" : "success"}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"deletePatient" : "patientNotFound"}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return dumps({'error' : str(e)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

#Define main APP
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
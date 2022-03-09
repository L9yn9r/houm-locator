from datetime import datetime, date, time, timedelta
from tabnanny import check
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from jinja2 import Undefined

import pandas as pd

from werkzeug.security import generate_password_hash, check_password_hash

import logic, utils , json
app = Flask(__name__)

app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = 'mongodb://localhost/pythonmongodb'

mongo = PyMongo(app)


class response_object(object):

    def __init__(self, idHoumer, idHoumProperty,  totalTime, latitude, longitude):

        self.idHoumer = idHoumer
        self.idHoumProperty = idHoumProperty
        self.totalTime = totalTime
        self.latitude = latitude
        self.longitude = longitude
        


## Registra la posición actual de Houmer  070322
@app.route('/setactualposition', methods=['POST'])
def set_actualposition():
    # Receiving Data
    idHoumer = request.json['idHoumer']
    latitud = request.json['latitud']
    longitud = request.json['longitud']
    altitude = request.json["altitude"]
    reportdate = datetime.strptime(request.json['reportdate'], "%Y-%m-%dT%H:%M:%S.000Z")
    now = datetime.now()
    id_houm_property= ""

    if idHoumer and longitud and latitud:
        prop_id = ""
        counter =  0
        houmer_loc = (latitud, longitud)

        ## Take the actual date to select db from date
        from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        from_date = datetime.strptime(str(from_date), "%Y-%m-%d %H:%M:%S")
        to_date = datetime.strptime(str( from_date + timedelta(hours=23, minutes=59)), "%Y-%m-%d %H:%M:%S")
  
        ## insert actual position in houmerlocations
        id = mongo.db.houmerlocations.insert( {'idHoumer' : idHoumer , 'latitud': latitud, 'longitud': longitud, 'altitude' : altitude, 'reportdate' : reportdate})

        ## take all houm properties for verify is houmer is into it  
        houm_props = mongo.db.houmproperties.find()    

        ## verify if houm is in property
        id_houm_property = logic.verifyIsInProperty(houmer_loc, houm_props)

        ## select actual houmer
        check_in_db_old = mongo.db.houmerinhome.find_one({'idHoumer' : idHoumer ,  "createdAt": { '$gte': from_date ,  '$lte': to_date}})      
        print("ELEMENTO ENCONTRADO", id_houm_property)
        
        
        print(check_in_db_old)#, check2)     

        # if houmer aren't in houm property
        if id_houm_property == "":
           
      
            if (check_in_db_old !=  None):
                print("Actualizar en db que ha salido")
                idhoumprop = check_in_db_old["idHoumProperty"]
                enter_date = check_in_db_old["inHoum"]
                time_counter = reportdate - enter_date
                counter = check_in_db_old["counter"] + 1
                id = mongo.db.houmerinhome.update_one({'idHoumer' : idHoumer , 'idHoumProperty': idhoumprop,  "inout" : True,
                                                       "createdAt": { '$gte': from_date ,  '$lte': to_date}},
                                                      {'$set': { "outHoum" : reportdate, "counter": counter, #"totalminutes" : utils.get_mins(str(time_counter)),  
                                                                "inout" : False, 'updatedAt' : now}})
       
            
        else:

            check_in_db = mongo.db.houmerinhome.find_one({'idHoumer' : idHoumer , 'idHoumProperty': id_houm_property,  "inout": True , 
                                                          "createdAt": { '$gte': from_date ,  '$lte': to_date}})

            checkout_in_db = mongo.db.houmerinhome.find_one({'idHoumer' : idHoumer , 'idHoumProperty': id_houm_property,  "inout": False , 
                                                          "createdAt": { '$gte': from_date ,  '$lte': to_date}})      

            if (check_in_db ==  None and checkout_in_db == None):
                
                id = mongo.db.houmerinhome.insert({'idHoumer' : idHoumer , 'idHoumProperty': id_houm_property, 
                                                   'latitud': latitud, 'longitud': longitud,
                                                   'inHoum': reportdate, "counter": 0, "totalminutes" : "0" ,                                                     
                                                   'outHoum': None,  "inout" : True, 'createdAt' : now})
                
            elif(check_in_db !=  None and checkout_in_db == None): 

                enter_date = check_in_db["inHoum"]
                actual_mins = check_in_db["totalminutes"]
                time_counter = reportdate - enter_date
                if(check_in_db["outHoum"]):
                    total_time =  int(utils.get_mins(str(time_counter))) + int(actual_mins)
                    inHoum = reportdate
                else:
                    total_time =  int(utils.get_mins(str(time_counter)))
                    inHoum = enter_date

                counter = check_in_db["counter"] + 1
                id = mongo.db.houmerinhome.update_one({'idHoumer' : idHoumer , 'idHoumProperty': id_houm_property ,  "inout": True,
                                                        "createdAt": { '$gte': from_date ,  '$lte': to_date} }, 
                                                      { '$set':  {"counter": counter, "totalminutes" : total_time ,  'inHoum': inHoum,
                                                        "inout" : True, 'updatedAt' : now}})            

                                             
            elif (check_in_db ==  None and checkout_in_db != None):
                  

                id = mongo.db.houmerinhome.update_one({'idHoumer' : idHoumer , 'idHoumProperty': id_houm_property ,  "inout": False ,
                                                    "createdAt": { '$gte': from_date ,  '$lte': to_date}}, 
                                                    {'$set':  { 'inHoum': reportdate,  "inout" : True, 'updatedAt' : now}})        

          
        response = jsonify({
            '_id': str(id),
            'idHoumer': idHoumer,
            'longitud': longitud,
            'latitud': latitud,
            'altitude' :  altitude,
            'reportdate' : reportdate
        })
        response.status_code = 201
        
        return response

    else:
        return not_found()


@app.route('/location', methods=['POST'])
def set_position():
    # Receiving Data
    idHoumer = request.json['idHoumer']
    latitud = request.json['latitud']
    longitud = request.json['longitud']
    altitude = request.json["altitude"]
    #entrydate = request.json
    reportdate = datetime.datetime.strptime(request.json['reportdate'], "%Y-%m-%dT%H:%M:%S.000Z")

    if idHoumer and longitud and latitud:

        houm_props = mongo.db.houmproperties.find()
        # response = json_util.con(json_util.dumps(houm_props))
        # return response
        ##print(response)
        prop_id = ""
        houmer_loc = (latitud, longitud)
        for prop in houm_props:
                # print(prop.get("idHoumProperty"))
                idh = prop.get("idHoumProperty")
                hlat = prop.get('latitud')
                hlon = prop.get('longitud')                   
                print(idh, hlat, hlon) 

                actualprop = (hlat, hlon)
                
                checkHoum = logic.IsInProp(houmer_loc, actualprop)
            
                if checkHoum : 
                    print ("Houmer " , idHoumer, " en Propiedad : " , idh ," ", prop.get("address"))
                    prop_id = idh
                    break
        if prop_id == "":
            print ("Houmer fuera de Propiedades ")
        
        return "ok" 

    else:
        return not_found()


## Registra la posición actual de Houmer
@app.route('/houmerposition', methods=['POST'])
def set_houmerposition():
    # Receiving Data
    idHoumer = request.json['idHoumer']
    latitud = request.json['latitud']
    longitud = request.json['longitud']
    altitude = request.json["altitude"]
    reportdate = datetime.datetime.strptime(request.json['reportdate'], "%Y-%m-%dT%H:%M:%S.000Z")

    if idHoumer and longitud and latitud:

        id = mongo.db.houmerlocations.insert( {'idHoumer' : idHoumer , 'latitud': latitud, 'longitud': longitud, 'altitude' : altitude, 'reportdate' : reportdate})
        response = jsonify({
            '_id': str(id),
            'idHoumer': idHoumer,
            'longitud': longitud,
            'latitud': latitud,
            'altitude' :  altitude,
            'reportdate' : reportdate
        })
        response.status_code = 201
        
        return response

    else:
        return not_found()


## Registra una nueva propiedad de HOUM
@app.route('/houmproperty', methods=['POST'])
def set_houmproperties():
    # Receiving Data
    idHoumProperty = request.json['idHoumProperty']
    latitud = request.json['latitud']
    longitud = request.json['longitud']
    altitude = request.json["altitude"]
    address = request.json["address"]
    phone =  request.json["phone"]
    createdAt = datetime.now()##datetime.datetime.strptime(request.json['createdAt'], "%Y-%m-%dT%H:%M:%S.000Z")


    if idHoumProperty and longitud and latitud:

        id = mongo.db.houmproperties.insert( {'idHoumProperty' : idHoumProperty , 
                                              'latitud': latitud, 
                                              'longitud': longitud, 
                                              'altitude' : altitude, 
                                              'address' : address,
                                              'phone' : phone,
                                              'createdAt' : createdAt})
        response = jsonify({
                                '_id': str(id),
                                'idHoumProperty': idHoumProperty,
                                'longitud': longitud,
                                'latitud': latitud,
                                'altitude' :  altitude,
                                'address' : address,
                                'phones' : phone, 
                                'createdAt' : createdAt
        })
        response.status_code = 201
        
        return response
        # return {"message" : "Localización Registrada Correctamente ...", 
        #         "Id" : str(id), "IdHoumer" : idHoumer, "Lat" : latitud , 
        #         "long" : longitud, "registeredAt" : reportdate} #response
    else:
        return not_found()



@app.route('/houmervisits', methods=['GET'])
def get_houmervisits():
     
    idHoumer  = request.args.get('id', type=str ,default='')
    actualdate  = request.args.get('date', type=str , default='') 

    asplidate = actualdate.split("-")

    actualdateformat = datetime(int(asplidate[0]), int(asplidate[1]), int(asplidate[2]))    

    from_date = datetime.strptime(str(actualdateformat), "%Y-%m-%d %H:%M:%S")
    to_date = datetime.strptime(str( from_date + timedelta(hours=23, minutes=59)), "%Y-%m-%d %H:%M:%S")
 
    houmer_visits = mongo.db.houmerinhome.find_one({'idHoumer' : idHoumer , "createdAt": { '$gte': from_date ,  '$lte': to_date}})

    response = json_util.dumps(houmer_visits)
    return Response(response, mimetype="application/json")



## Consulta las propiedades actuales de HOUM
@app.route('/houmproperties', methods=['GET'])
def get_houmProp():
    houm_props = mongo.db.houmproperties.find()
    response = json_util.dumps(houm_props)
    return Response(response, mimetype="application/json")



@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response



if __name__ == "__main__":
    app.run(debug=False, port=3000)

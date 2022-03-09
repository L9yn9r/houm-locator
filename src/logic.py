from geopy.geocoders import Nominatim 
import time
import math
from geopy.distance import geodesic


def IsInProp(houmerLoc , houmPropLoc):
    dist = geodesic(houmerLoc, houmPropLoc).meters

    if(dist < 100): # está en propiedad
        return True
    else : 
        return False    


def verifyIsInProperty (actual_houmer_loc, houm_props):
    prop_id =""
    for prop in houm_props:
            # print(prop.get("idHoumProperty"))
            idh = prop.get("idHoumProperty")
            hlat = prop.get('latitud')
            hlon = prop.get('longitud')                   
            print(idh, hlat, hlon) 

            actualprop = (hlat, hlon)
            
            checkHoum = IsInProp(actual_houmer_loc, actualprop)
        
            if checkHoum : 
                #print ("Houmer " , idHoumer, " en Propiedad : " , idh ," ", prop.get("address"))                
                prop_id = idh
                break
    return prop_id
        
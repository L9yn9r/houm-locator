#locator

Sistema de posicionamiento


La solución fue desarrollada con Python  y MongoDB
El proyecto puede ser contenerizado via docker o puede ejecutarse
directamente desde un IDE

Se deben crear las siguientes locaciones como simulación de las propiedades de Houm
con el siguiente servicio se pueden crear las propiedades
[POST] http://127.0.0.1:3000/houmproperty
y en el Body se envía cada una de las propiedades

# propiedad 2
{
"idHoumProperty": "PROPCLL147",
"latitud": "4.729462",
"longitud": "-74.045098",
"altitude": "",
"address": "Cl. 147 #17-95",
"phone": "111111",
"createdAt": {
"$date": 1646578858844
}

# propiedad 2
{
"idHoumProperty": "PROPCLL91",
"latitud": "4.676896",
"longitud": "-74.054778",
"altitude": "",
"address": "Cra. 18 #91-63",
"phone": "222222",
"createdAt": {
"$date": 1646578944123
}

# propiedad 3
{"idHoumProperty": "PROPCLL45",
"latitud": "4.632767",
"longitud": "-74.068435",
"altitude": "",
"address": "Cl. 45 #14-2",
"phone": "333333",
"createdAt": {
"$date": 1646579064938
}

# propiedad 4
{
"idHoumProperty": "PROPCLL53",
"latitud": "4.644155",
"longitud": "-74.083088",
"altitude": "",
"address": "UN Entrada Calle 53",
"phone": "444444",
"createdAt": {
"$date": 1646579219922
}

# Para Consultar propiedades Houm
[GET] http://127.0.0.1:3000/houmproperties


# Reportar Posición de Houmer

La aplicación movil cliente se debe reportar cada segundo 
para hacer la estimación del tiempo y movimientos con 
un formato igual al Body del Request para reportar posición

[POST] http://127.0.0.1:3000/setactualposition

{
  	"idHoumer" : "HOUMER070322" ,
	"latitud":  "4.729462",
	"longitud": "-74.055098",
  	"altitude" : "123",
  	"reportdate" : "2022-03-01T15:00:00.000Z"
}

# Para Counsultar Visitas del Houmer con su tiempo respectivo

[GET] http://127.0.0.1:3000/houmervisits?id=HOUMER08&date=2022-03-08

{
"_id": {
"$oid": "62282457e5a405706923a62a"
},
"idHoumer": "HOUMER08",
"idHoumProperty": "PROPCLL147",
"latitud": "4.729462",
"longitud": "-74.045098",
"inHoum": {
"$date": 1502637000000
},
"counter": 10,
"totalminutes": 45,
"outHoum": {
"$date": 1502623500000
},
"inout": true,
"createdAt": {
"$date": 1646779911552
},
"updatedAt": {
"$date": 1646780070245
}
}






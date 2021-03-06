# <a name="top"></a>Fiware Docker

* [Introducción](#introducción)
* [Orion](#orion)
    * [Crear entidad](#crear-entidad)
    * [Crear entidades](#crear-entidades)
    * [Modificar atributo](#modificar-atributo)
    * [Modificar atributos](#modificar-atributos)
    * [Modificar entidaades](#modificar-entidades)
    * [Obtener entidades](#obtener-entidades)
    * [Obtener atributos](#obtener-atributos)
    * [Suscripciones](#suscripciones)

## Introducción

El repositorio actual presenta los archivos necesarios para la instalacion de fiware haciendo uso de docker, docker-compose 
junto con toda la inforación necesaria para su correcto funcionamiento.

Este contiene la carpeta "orion-cygnus" la cual contiene los archivos de los contenedores de docker ademas de
la configuración de cygnus

Por otra parte presenta el script "docker-destroy-all.sh" con el cual se logran eliminar todos los contenedores existentes 
en caso de necesitarse hacerlo.

Por ultimo contiene un archivo JSON base de los protocolos de comunicacion con la plataforma

[Top](#top)

## Orion

el Context Broker (CB) es el encargado de obtener los datos de multiples fuentes, basado en peticiones http para las multiples operaciones que se requieren a la hora de obtener y almacenar los datos obtenidos, el cuerpo de los mensajes se basa en los formatos NGSI aunque para el caso actual solo se empleara en su version 2 para establecer un estandar. Cada objeto generado es conocido como una entidad, la cual puede poseer multiples atributos y se manipulan las peticiones ya mencionadas. Un ejemplo basico de una entidad se presenta a continuación:

```JSON
{
  "type": "Sensor",
  "id": "udea",
  "temp": {
    "value": 23.2,
    "type": "float"
  },
  "location": {
    "value": "6.2669533, -75.5691113",
    "type": "geo:point"
  }
}
``` 

Donde como se observa posee un tipo, el cual establece un estandar a partir del primer objeto de dicho tipo para determinar discrepancias y errores a futuro. El id Cumple la funcion de ser la llave primaria unica y caracteristica de la identidad y por ultimo los otros 2 terminos son los atributos de la entidad el cual presenta el valor y el tipo de dato almacenado.

Las operaciones basicas del Orion son:

### Crear entidad

Bajo una peticion de tipo POST con los siguientes encabezados:

``` JSON
Content-Type  : application/json
Fiware-ServicePath :  /Test
```

con el siguiente cuerpo

``` JSON
{
  "type": "Sensor",
  "id": "udea",
  "temp": {
    "value": 23.2,
    "type": "float"
  },
  "location": {
    "value": "6.2669533, -75.5691113",
    "type": "geo:point"
  }
}
```

se logra crear una entidad enviando la petición a la dirección: `ip_context_broker:1026/v2/entities` 
el codigo de respuesta indicado esta dado por 201

### Crear entidades

Bajo una peticion de tipo POST con los siguientes encabezados:

``` JSON
Content-Type  : application/json
Fiware-ServicePath :  /Test
```

con el siguiente cuerpo

``` JSON
{
	"actionType":"APPEND",
	"entities":[
	{
		"type": "Sensor",
		"id": "udea",
		"temp": {
    	"value": 23.2,
    	"type": "float"
		},
		"location": {
    	"value": "6.2669533, -75.5691113",
    	"type": "geo:point"
		}
	},
	{
		"type": "Sensor",
		"id": "casa",
		"temp": {
    	"value": 21.6,
    	"type": "float"
		},
		"location": {
    	"value": "6.2669544, -75.5691223",
    	"type": "geo:point"
		}
	}
]
}
```
se logra crear un lote de entidades enviando la petición a la dirección: `ip_context_broker:1026/v2/op/update` 
el codigo de respuesta indicado esta dado por 204


### Modificar atributo

Bajo una peticion de tipo PUT con los siguientes encabezados:

``` JSON
Content-Type  : application/json
Fiware-ServicePath :  /Test
```

con el siguiente cuerpo

``` JSON
{
	"type":"float",
	"value": 21.9
}
```

se logra editar el atributo `temp` de la entidad enviando la petición a la dirección: `ip_context_broker:1026/v2/entities/udea/attrs/temp` 
Donde udea es el id de la entidad y temp es el atributo a modificar,el codigo de respuesta indicado esta dado por 204


### Modificar atributos

Bajo una peticion de tipo POST con los siguientes encabezados:

``` JSON
Content-Type  : application/json
Fiware-ServicePath :  /Test
```

con el siguiente cuerpo


``` JSON
{
  "actionType": "UPDATE",
  "entities": [
    {
    "type": "Sensor",
    "id": "udea",
    "temp": {
        "value": 22.1,
        "type": "float"
    },
    "location": {
        "value": "6.2669533, -75.5691113",
        "type": "geo:point"
    }
  }
  ]
}
```
se logra editar toda una entidad enviando la petición a la dirección: `ip_context_broker:1026/v2/op/update` 
el codigo de respuesta indicado esta dado por 204

### Modificar entidades

Bajo una peticion de tipo POST con los siguientes encabezados:

``` JSON
Content-Type  : application/json
Fiware-ServicePath :  /Test
```

con el siguiente cuerpo

``` JSON
{
	"actionType":"UPDATE",
	"entities":[
	{
		"type": "Sensor",
		"id": "udea",
		"temp": {
    	"value": 26.7,
    	"type": "float"
		},
		"location": {
    	"value": "6.2669533, -75.5691113",
    	"type": "geo:point"
		}
	},
	{
		"type": "Sensor",
		"id": "casa",
		"temp": {
    	"value": 24.2,
    	"type": "float"
		},
		"location": {
    	"value": "6.2669544, -75.5691223",
    	"type": "geo:point"
		}
	}
]
}
```
se logra modificar varias entidades enviando la petición a la dirección: `ip_context_broker:1026/v2/op/update` 
el codigo de respuesta indicado esta dado por 204


### Obtener entidades

Bajo una peticion de tipo GET con los siguientes encabezados:

``` JSON
Fiware-ServicePath :  /Test
```
se logra observar el contenido de la entidad `casa`enviando la petición a la dirección: `ip_context_broker:1026/v2/entities/casa` 

el codigo de respuesta indicado esta dado por 200 y el contenido de la entidad en formato JSON

Al usar la direccion: `ip_context_broker:1026/v2/entities/` se retornan todas las entidades.

Por ultimo Orion soporta operaciones de filtrado descritas en la documentación propia de los desarrolladores: [filtros](https://fiware-orion.readthedocs.io/en/master/user/filtering/index.html)


### Obtener atributos

Bajo una peticion de tipo GET con los siguientes encabezados:

``` JSON
Fiware-ServicePath :  /Test
```
se logra observar el valor del atributo `temp` de la entidad `casa`enviando la petición a la dirección: `ip_context_broker:1026/v2/entities/casa/attrs/temp` 

el codigo de respuesta indicado esta dado por 200 y el valor del atributo se entrega en formato JSON


### suscripciones

Las subscripciones son necesarias para redirigir los datos destinados al Orion hacia el Cygnus de tal manera que estos queden registrados. Estas se hacen bajo una peticion de tipo POST con los siguientes encabezados:

``` JSON
Fiware-ServicePath :  /Test
```

con el siguiente cuerpo

``` JSON
{	
	"subject":{
		"entities": [
        {
            "type": "Sensor",
            "isPattern": "false",
            "id": "casa"
        },{
            "type": "Sensor",
            "isPattern": "false",
            "id": "udea"
        }
    ],
    "condition":{
		"attrs": ["temp"]    	
    }
	},
	"notification":{
		"http":{"url":"http://ip_context_broker:5050/notify"},
		"attrs": ["temp"],
		"attrsFormat":"legacy"
	},
	"expires": "2099-12-31T23:00:00.00Z",
	"throttling": 5
}
```
Para mas detalles sobre las suscripciones consulte la ducomentación propia: [suscripciones](http://fiware-orion.readthedocs.io/en/develop/user/walkthrough_apiv2/#subscriptions)


En caso de requerir documentación propia de los desarrolladores, se encuentra en el siguiente enlace:  [Orion Context Broker](http://fiware-orion.readthedocs.io/en/develop/user/walkthrough_apiv2/)

[Top](#top)


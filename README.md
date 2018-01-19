# <a name="top"></a>Fiware Docker

* [Introducción](#introducción)
* [Orion](#orion)
    * [Crear entidades](#crear-entidades)
    * [Modificar atributo](#modificar-atributo)
    * [Modificar atributos](#modificar-atributos)

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

### Crear entidades

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


### Modificar atributo



### Modificar atributos



[Top](#top)


# <a name="top"></a>Fiware Docker

* [Introducción](#Introducción)
* [Orion](#Orion)
    * [Crear entidades](#Crear entidades)
    * [Modificar atributo](#Modificar atributo)
    * [Modificar atributos](#Modificar atributos)

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

el Context Broker (CB) es el encargado de obtener los datos de multiples fuentes, basado en peticiones http para las multiples operaciones que se requieren a la hora de obtener y almacenar los datos obtenidos, el cuerpo de los mensajes se basa en los formatos NGSI en su version 2 para establecer un estandar. Cada objeto generado es conocido como una entidad, la cual puede poseer multiples atributos y se manipulan las peticiones ya mencionadas. Un ejemplo basico de una entidad se presenta a continuación:

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

[Top](#top)

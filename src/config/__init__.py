#-------------------------------------------------------------------------------
# Name:        Configuracion del aplicativo
# Purpose:     Empaquetar los ficheros configuradores.
#
# Author:      Aref
#
# Created:     19+3/9+3/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Paquete: Configuracion del aplicativo

Empaquetar los ficheros configuradores.


    Modulo: Cabecera del paquete configuracion del aplicativo

Genera la configuracion del aplicativo web y la hace llamable.
"""

import json, os

config = {} #configuracion llamable

ruta = os.path.dirname(os.path.abspath(__file__))
# entorno = "DES"
entorno = "PRD"

def init_config(forzar_entorno: str = entorno):
    """ Funcion encapsuladora: Inicializacion de la configuracion

    Funcion que actualiza el diccionario de configuraciones segun
    el entorno solicitado, o se ajusta si reconoce un entorno
    indebido.

    Parametros:
        forzar_entorno (str) ["PRD"] -- cadena que abrevia el
            nombre del entorno a utilizar al configurar
            actualizar la configuracion llamable

    Excepciones:
        RuntimeError (Ningun entorno valido encontrado para la
            configuracion) -- Si nunca se hallo un entorno valido
            a partir del solicitado
    """
    def update_config(cargador: dict):
        """ Funcion encapsulada: Actualizar configuracion

        Funcion que actualiza la configuracion llamable en base a un
        diccionario cargador. Si alguno de los elementos es una
        variable de entorno, llama la variable.

        Parametros:
            cargador (dict) -- diccionario con los valores para
                agregar a la configuracion
        """
        for l, e in cargador.items(): #llaves y elementos del cargador

          #condicional si el elemento a configurar es una variable de entorno
          if type(e) == str and e.startswith('$'): config[l] = os.getenv(e[1:])

          else: config[l] = e

    # Funcion: Configurar segun archivo
    def init_config_ruta(ruta_config: str):
        with open(ruta_config) as f: update_config(json.load(f))

    #ruta del JSON condicional al entorno elegido
    ruta_final = ruta + f'/config_{forzar_entorno.lower()}.json'

    #cambio condicional del entorno
    if forzar_entorno == "PRD": #entorno de produccion
        try: init_config_ruta(ruta_final)

        except FileNotFoundError:
            print("Archivo de produccion no encontrado\n" +
                    "Pasa a usar archivo de desarrollo")
            init_config(forzar_entorno = "DES")

    elif forzar_entorno == "DES": #entorno de desarrollo
        try: init_config_ruta(ruta_final)

        except FileNotFoundError:
            print("Archivo de desarrollo no encontrado\n")
            init_config(forzar_entorno = None)

    else: #carencia de entorno -> Error
        print("Ningun archivo para la configuracion")
        raise RuntimeError("Ningun entorno valido encontrado para la " +
                "configuracion")

    from ..utilidades.utilidades_os import corrifying_path

    #configuraciones independientes del entorno
    config["directorio_carga"] = corrifying_path(
            ruta + '/../archivos/al_cargar')
    config["entorno"] = forzar_entorno
    config["nombre_entorno"] = {
            "DES": "desarrollo",
            "PRD":"produccion"
        }[forzar_entorno]
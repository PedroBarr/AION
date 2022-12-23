#-------------------------------------------------------------------------------
# Name:        Conexion URI
# Purpose:     Recopilar funciones que permiten manejar la
#               configuracion de la base de datos.
#
# Author:      Aref
#
# Created:     19+3/9+3/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Conexion URI

Recopilar funciones que permiten manejar la configuracion de la
base de datos.

Recopila:
    Funcion Construccion URI
"""

import json, os

ruta = os.path.dirname(os.path.abspath(__file__)) + "\\db.json"

def constructor_uri() -> dict:
    """ Funcion: Construccion URI

    Funcion que construye un diccionario con los datos necesarios
    para reemplazar en una plantilla de una URI en base a un
    archivo JSON con las credenciales.

    En caso de no encontrar el archivo, lo genera con
    credenciales invalidas.

    Retorno:
        un diccionario con las credenciales para la URI (motor,
            host, puerto, nombre_bd, usuario, clave)
    """
    if not os.path.exists(ruta):
        with open(ruta, "w") as f: json.dump({}, f)
        print(f'Recuerda agregar el archivo {ruta} al .gitignore')

    with open(ruta) as f:
        db_config = json.load(f)
        for credencial in ["host", "nombre_bd", "usuario","clave", "motor"]:
            if credencial not in db_config:
                db_config[credencial] = ""
                with open(ruta, "w") as ff: json.dump(db_config, ff)

        if "puerto" not in db_config:
            db_config["puerto"] = 0
            with open(ruta, "w") as ff: json.dump(db_config, ff)

        return db_config
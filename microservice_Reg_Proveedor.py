#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request #import main Flask class and request object
import pika
import MySQLdb
import json
import sys
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import cgi


class Microservice:
   
    @staticmethod
    def microserviceLogic (nombre,apellido,celular,direccion,correo,pagina,telefono):

        try:

            db = MySQLdb.connect(host="35.199.86.113", user="root", passwd="root2018", db="microservice")        
            cur = db.cursor()
            fechaCreacion= time.strftime('%Y-%m-%d')
            cur.execute("INSERT INTO `microservice`.`proveedor` VALUES (null,2,'"+nombre+"','"+apellido+"','"+celular+"','"+direccion+"','"+correo+"','"+pagina+"','"+telefono+"','"+fechaCreacion+"','Activo')")
            db.commit()
            
        except IOError as e:
            db.rollback()
            db.close()
            return "Error BD: ".format(e.errno, e.strerror)
            
        db.close() 

        return {"id":str(cur.lastrowid)  ,"nombre": nombre+' '+apellido} 

		
app = Flask(__name__)
@app.route('/microservicio/reg_provedor',methods=['GET', 'POST'])

def registrar_provedor ():

    if request.method == "POST":

      req_data = request.get_json()
      nombre = req_data['nombre']
      apellido = req_data['apellido']
      celular = req_data['celular']
      direccion = req_data['direccion']
      correo = req_data['correo']
      pagina = req_data['pagina']
      telefono = req_data['telefono']
      
      data = Microservice.microserviceLogic(nombre,apellido,celular,direccion,correo,pagina,telefono)
      
      response = {} 
      response['proveedor_info'] = "Proveedor "+data["nombre"]+" persistido."
      response['msg'] = 'Hecho'

      return json.dumps(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5005)
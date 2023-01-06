from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from sqlalchemy import create_engine
import os
import shutil
import utils
from flask_mysqldb import MySQL
from pandas import ExcelWriter
from properties.properties_db import Properties
from enviroment.utils import init_properties
from properties.properties_db import Properties

yaml_path = './config/db_config.yaml'
yaml = init_properties(yaml_path)
Properties(yaml['db'])

app = Flask(__name__)

proper = Properties()

# Mysql Connection
app.config['MYSQL_HOST'] = proper.host
app.config['MYSQL_USER'] = proper.username
app.config['MYSQL_PASSWORD'] = proper.password
app.config['MYSQL_DB'] = proper.schema
mysql = MySQL(app)


#SERVICIO 1
#print(os.listdir("C:/Users/darcy.espinosa/Desktop/archivos/inbox"))
for file in os.listdir("C:/Users/darcy.espinosa/Desktop/inbox"): 
    if '.xlsx'in file:
        print(file)        
    path = (r"C:/Users/darcy.espinosa/Desktop/inbox" + "/" + file)
    #print(path)
    lectura = pd.read_excel(path)
    #print (("Hola",lectura))

    path2 = "C:/Users/darcy.espinosa/Desktop/trash/"
    file="C:/Users/darcy.espinosa/Desktop/inbox" + "/" + file

    path3 = "C:/Users/darcy.espinosa/Desktop/outbox/"
    if lectura.empty: 
        #print ("Archivo vacio")
        shutil.move(file, path2)
    else:
        shutil.move(file, path3)

# SERVICIO 2

db_data = 'mysql+mysqldb://' + proper.username + ':' + proper.username + '@' + proper.host + ':3306/'  + proper.schema + '?charset=utf8mb4'
engine = create_engine(db_data)


with app.app_context():
    cur = mysql.connection.cursor()
for file in os.listdir("C:/Users/darcy.espinosa/Desktop/outbox"):
    if '.xlsx'in file:
        path4 = "C:/Users/darcy.espinosa/Desktop/outbox/" + file
        df = pd.read_excel(path4)
        for item in df.iterrows():
            try:
                df.to_sql(proper.schema, engine, index=False, if_exists='append')
            except:
                print("Los datos ya están registrados")
        #shutil.move(file, path3)

# SERVICIO 3

data_xlsx = pd.read_sql_table(proper.schema, engine)

##print(data_xlsx)
writer = ExcelWriter('C:/Users/darcy.espinosa/Desktop/temporales/dataset.xlsx')
df.to_excel(writer, 'Hoja de datos', index=False)
writer.save()
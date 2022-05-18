import time
import streamlit as st
import datetime
import numpy as np
import pandas as pd
import pymysql
import os

def sql_connect():
    global db,cursor,host
    host='8.tcp.ngrok.io'
    port = 13020
    user='a11805'
    passwd='pccua11805'
    database='aiot'
    print('Connecting....')
    print('host:%s\nuser:%s\npassword:********\ndatabase:%s\n'%(host,user,database))
    db=pymysql.connect(host=host,user=user,passwd=passwd,database=database,port=port)
    os.system('clear')
    cursor=db.cursor()
    print('Connection succeed')

def select_data(title_name,table_name,number):
    sql = '''SELECT '''+title_name+''' FROM '''+table_name+''' ORDER BY `time` DESC LIMIT '''+number+''';'''
    #print(sql)
    cursor.execute(sql)
    result=cursor.fetchall()
    result = pd.DataFrame(result)
    return result

sql_connect()

sql = '''SELECT * FROM `test_streamlit` ORDER BY `test_streamlit`.`time` DESC;'''
cursor.execute(sql)
result=cursor.fetchone()


sensor = select_data('''`time`, `temperature`, `humidity`, `quality_Potted`, `quality_Reservoir`, `luminance`, `CO2`, `Potted`, `Reservoir`, `smoke`''','test_streamlit','2016')
sensor.columns=['時間','溫度','濕度','水質(盆栽)','水質(水池)','亮度','CO2','水溫','水溫(水池)','煙霧']

st.title('智慧溫室中控台')

col1, col2 ,col3  = st.columns(3)
col1.metric(label="溫度", value=str(result[1])+" °c",)
col2.metric(label="濕度", value=str(result[2])+" %",)
col3.metric(label="水質", value=str(result[3])+" ppm",)

if st.sidebar.button('燈'):
     sql = '''UPDATE `action_always` SET `light`='1' '''
     cursor.execute(sql)
     db.commit()
if st.sidebar.button('霧化器'):
     sql = '''UPDATE `action_always` SET `humidification`='1' '''
     cursor.execute(sql)
     db.commit()
if st.sidebar.button('換水'):
     sql = '''UPDATE `action_always` SET `water`='1' '''
     cursor.execute(sql)
     db.commit()
if st.sidebar.button('加水'):
     sql = '''UPDATE `stop` SET `stop`='3' '''
     cursor.execute(sql)
     db.commit()
if st.sidebar.button('抽水'):
     sql = '''UPDATE `stop` SET `stop`='1' '''
     cursor.execute(sql)
     db.commit()
if st.sidebar.button('施肥'):
     sql = '''UPDATE `action_always` SET `fertilizer`='1' '''
     cursor.execute(sql)
     db.commit()
if st.sidebar.button('停止'):
     sql = '''UPDATE `stop` SET `stop`='2' '''
     cursor.execute(sql)
     db.commit()       
line_time = sensor["時間"]

sensor_all = sensor
sensor_all.drop(columns = '時間',inplace=True)
sensor_all = pd.DataFrame(sensor_all)
sensor_all.set_index(pd.to_datetime(line_time,format="%Y-%m-%d %H:%M:%S"),inplace=True)
line_chart = st.line_chart(sensor_all)


col1, col2  = st.columns(2)
col3, col4  = st.columns(2)
col5, col6  = st.columns(2)
if col1.checkbox('溫度'):
    temperature = sensor['溫度']
    temperature = pd.DataFrame(temperature)
    temperature.set_index(pd.to_datetime(line_time,format="%Y-%m-%d %H:%M:%S"),inplace=True)
    line_chart = col1.line_chart(temperature,height = 200,use_container_width = False)
if col2.checkbox('濕度'):
    humidity = sensor['濕度']
    humidity = pd.DataFrame(humidity)
    humidity.set_index(pd.to_datetime(line_time,format="%Y-%m-%d %H:%M:%S"),inplace=True)
    line_chart = col2.line_chart(humidity,height = 200,use_container_width = False)    #折線圖
if col3.checkbox('水質(盆栽)'):
    quality_Potted = sensor['水質(盆栽)']
    quality_Potted = pd.DataFrame(quality_Potted)
    quality_Potted.set_index(pd.to_datetime(line_time,format="%Y-%m-%d %H:%M:%S"),inplace=True)
    line_chart = col3.line_chart(quality_Potted,height = 200,use_container_width = False)    #折線圖

if col4.checkbox('亮度'):
    quality_Reservoir = sensor['亮度']
    quality_Reservoir = pd.DataFrame(quality_Reservoir)
    quality_Reservoir.set_index(pd.to_datetime(line_time,format="%Y-%m-%d %H:%M:%S"),inplace=True)
    line_chart = col4.line_chart(quality_Reservoir,height = 200,use_container_width = False)    #折線圖

if col5.checkbox('CO2'):
    CO2 = sensor['CO2']
    CO2 = pd.DataFrame(CO2)
    CO2.set_index(pd.to_datetime(line_time,format="%Y-%m-%d %H:%M:%S"),inplace=True)
    line_chart = col5.line_chart(CO2,height = 200,use_container_width = False)    #折線圖

if col6.checkbox('水溫'):
    Potted = sensor['水溫']
    Potted = pd.DataFrame(Potted)
    Potted.set_index(pd.to_datetime(line_time,format="%Y-%m-%d %H:%M:%S"),inplace=True)
    line_chart = col6.line_chart(Potted,height = 200,use_container_width = False)    #折線圖

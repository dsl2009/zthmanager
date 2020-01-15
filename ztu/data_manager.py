#coding=utf-8
import pymysql
import json
import requests
import time

def login(user_name, password):
    db = pymysql.connect(host='localhost', user='root' , passwd='900504', db='nst_iot', port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'select * from kehu_tb where user_name=%s and password=%s'
    cursor.execute(sql,(user_name, password))
    reult = cursor.fetchall()
    if len(reult)>0:
        d = reult[0]
        data = {'company_id':d[0], 'company_name':d[1]}
        return {'status':200, 'data':data}
    else:
        return {'status':400, 'data':'user or password is wrong!'}


def update_manager(tel_num, user_name, pre, manager_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'update manager_tb set user_name=%s,user_auth=%s,user_tel=%s where id=%s'
    num = cursor.execute(sql, ( user_name, pre, tel_num, manager_id))
    db.commit()
    db.close()
    return {'status':200,'message':'ok'}

def add_manager(tel_num, user_name, pre):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql =  'insert into manager_tb(user_name, user_tel, user_auth) values ( %s,%s,%s)'
    num = cursor.execute(sql, ( user_name,  tel_num, pre))
    db.commit()
    db.close()
    if num == 0:
        return {'status':400,'message':'ok'}
    else:
        return {'status':200,'message':'ok'}

def delete_mananger(manager_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'delete  from manager_tb where user_tel=%s'
    cursor.execute(sql,(manager_id,))
    db.commit()
    db.close()
    return  {'status':200,'message':'ok'}


def get_device_by_company_web(company_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT a.id as company_id,b.id, b.router_mac,b.router_name,b.on_line,c.dev_mac,c.dev_name,c.color,c.id ' \
          'FROM manager_tb a, router_tb b, device_tb c ' \
          'WHERE a.company=%s AND a.id=b.admin_id AND b.router_mac=c.router_mac'
    cursor.execute(sql,(company_id,))
    results = cursor.fetchall()
    db.close()
    dts = []

    for x in results:
        key = str(x[1])+'_'+str(x[2])+'_'+str(x[3])+'_'+str(x[4])
        rel = -1
        for i in range(len(dts)):
            if dts[i].get(key,None) is not None:
                rel = i
        if rel==-1:
            dts.append({key:[{'dev_mac':x[5],'dev_name':x[6],'dev_color':x[7],'id':x[8]}]})
        else:
            dts[rel][key].append({'dev_mac':x[5],'dev_name':x[6],'dev_color':x[7],' id':str(x[8])})
    rts = []
    for k in dts:
        keys = list(k.keys())[0]
        dk = keys.split('_')
        rts.append({'id':str(dk[0]),'dev_mac':dk[1],'dev_name':dk[2],'online':dk[3],'devices':k[keys]})
    return rts


def get_manager_by_company(company_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT * from manager_tb where company=%s'
    cursor.execute(sql,(company_id,))
    results = cursor.fetchall()
    db.close()
    dts = []
    for x in results:
        dts.append({
            'id':x[0],
            'user_name':x[1],
            'user_tel':x[2],
            'user_auth':bool(x[3]),
            'add_time':x[-1]
        })
    return {'data':dts,'status':200}


def get_devices_history(dev_mac):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT status, time_sep from dev_history where dev_mac=%s limit 100'
    cursor.execute(sql,(dev_mac,))
    results = cursor.fetchall()
    db.close()
    dts = {'time_sep':[],'status':[]}
    for x in results:
        dts['status'].append(x[0]+10)
        dts['time_sep'].append(x[1])
    return dts




def get_history(dev_mac):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT status, time_sep from dev_history where dev_mac=%s limit 100'
    cursor.execute(sql,(dev_mac,))
    results = cursor.fetchall()
    db.close()
    data = []
    dts = {'data':[]}
    for x in results:
        data.append([int(x[1].timestamp()*1000),x[0]+10])
    if len(data)>2:
        for k in range(len(data)-2):
            dts['data'].append(data[k])
            dts['data'].append([data[k+1][0]-1000,data[k][1]])
    else:
        dts['data'] = data
    return dts
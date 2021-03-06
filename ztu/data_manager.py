#coding=utf-8
import pymysql
import json
import requests
import time
import datetime

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

def login_super(user_name, password):
    if user_name==password:
        data = {'user_id':2}
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

def add_super_manager(tel_num, user_name, auth):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql =  'insert into super_manager(user_name, user_tel, user_auth) values ( %s,%s,%s)'
    num = cursor.execute(sql, ( user_name,  tel_num, auth))
    db.commit()
    db.close()
    if num == 0:
        return {'status':400,'message':'ok'}
    else:
        return {'status':200,'message':'ok'}



def get_all_super_manager():
    name_dict = ['仅可以查看所有的设备','可以管理所有的设备']
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT * from super_manager'
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    dts = []
    for x in results:
        dts.append({
            'id':x[0],
            'user_name':x[1],
            'user_tel':x[2],
            'user_auth':name_dict[x[3]],
            'add_time':x[-1]
        })
    return {'data':dts,'status':200}


def update_kehu_super_manager(change_id, delete_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'update kehu_tb set super_manager=%s where super_manager=%s'
    cursor.execute(sql,(change_id, delete_id,))
    db.commit()
    db.close()


def delete_super_mananger(change_id, delete_id):
    if change_id:
        update_kehu_super_manager(change_id, delete_id)
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'delete  from super_manager where id=%s'
    cursor.execute(sql, (delete_id,))
    db.commit()
    db.close()
    return {'status': 200, 'message': 'ok'}


def bind_super_manager(super_id, kehu_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'update kehu_tb set super_manager=%s where kehu_id=%s'
    cursor.execute(sql, (super_id, kehu_id,))
    db.commit()
    db.close()




def update_router(change_id, delete_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'update router_tb set admin_id=%s where admin_id=%s'
    cursor.execute(sql,(change_id, delete_id,))
    db.commit()
    db.close()


def delete_mananger(change_id, delete_id):
    update_router(change_id, delete_id)
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'delete  from manager_tb where id=%s'
    cursor.execute(sql,(delete_id,))
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
    name_dict = ['仅可以管理自己添加的设备','可以管理所有的设备','仅可以查看所有的设备']
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
            'user_auth':name_dict[x[3]],
            'add_time':x[-1]
        })
    return {'data':dts,'status':200}

def get_kehu():
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT kehu_tb.id, kehu_tb.name, kehu_tb.tel, kehu_tb.user_name,kehu_tb.password, ,kehu_tb.add_time, kehu_tb.super_manager,' \
          'super_manager.user_name FROM kehu_tb LEFT JOIN super_manager ON kehu_tb.super_manager=super_manager.id'
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    dts = []
    for x in results:
        dts.append({
            'id':x[0],
            'user_name':x[1],
            'user_tel':x[2],
            'user_login_name':x[3],
            'user_login_password': x[4],
            'add_time':x[5],
            'super_id': x[6],
            'super_name': x[7],
        })
    return {'data':dts,'status':200}


def add_kehu(user_name,  user_tel, user_login_name, user_login_password):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql =  'insert into kehu_tb(name, tel, user_name, password) values ( %s,%s,%s,%s)'
    num = cursor.execute(sql, ( user_name,  user_tel, user_login_name, user_login_password))
    db.commit()
    db.close()
    if num == 0:
        return {'status':400,'message':'ok'}
    else:
        return {'status':200,'message':'ok'}

def update_kehu(user_name,  user_tel, user_login_name, user_login_password, kehu_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'update manager_tb set name=%s,tel=%s,user_login_name=%s , user_login_password=%s, where id=%s'
    num = cursor.execute(sql, ( user_name,  user_tel, user_login_name, user_login_password, kehu_id))
    db.commit()
    db.close()
    return {'status':200,'message':'ok'}


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
    data_nn = []
    dts = {'data':[],'labels':['关闭时间','运行时间','故障时间'],'times':[0,0,0]}
    if len(results)==0:
        return dts
    for x in results:
        data.append([int(x[1].timestamp()*1000),x[0]+10])
        data_nn.append([int(x[1].timestamp()), x[0]])
    data_nn.append([time.time(), data[-1][1]])
    for i in range(len(data) - 1):
        dts['data'].append(data[i])
        dts['data'].append([data[i + 1][0] , data[i][1]])
    dts['data'].append(data[-1])
    dts['data'].append([time.time()*1000, data[-1][1]])
    '''
    dts['data'] = data
    '''
    for i in range(1, len(data_nn)):
        if data_nn[i - 1][1] in [32, 64, 96]:
            dts['times'][1] += data_nn[i][0] - data_nn[i - 1][0]
        elif data_nn[i - 1][1] == 0:
            dts['times'][0] += data_nn[i][0] - data_nn[i - 1][0]
        else:
            dts['times'][2] += data_nn[i][0] - data_nn[i - 1][0]

    for i in range(3):
        dts['times'][i] = dts['times'][i] / 3600.0
    return dts

def get_history_times(dev_mac):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT status, time_sep from dev_history where dev_mac=%s limit 100'
    cursor.execute(sql,(dev_mac,))
    results = cursor.fetchall()
    db.close()
    data = []
    dts = {'data':[0,0,0],'labels':['关闭时间','运行时间','故障时间']}
    if len(results) == 0:
        return dts
    for x in results:
        data.append([int(x[1].timestamp()), x[0]])
    data.append([time.time(),data[-1][1]])
    for i in range(1,len(data)):
        if data[i-1][1] in [32, 64, 96]:
            dts['data'][1]+=data[i][0]-data[i-1][0]
        elif data[i-1][1]==0:
            dts['data'][0] += data[i][0] - data[i - 1][0]
        else:
            dts['data'][2] += data[i][0] - data[i - 1][0]
    for x in range(3):
        dts['data'][i] = dts['data'][i]/3600.0


    return dts
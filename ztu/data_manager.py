#coding=utf-8
import pymysql
import json
import requests

def login(user_name, password):
    db = pymysql.connect(host='localhost', user='root' , passwd='900504', db='nst_iot', port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'select * from kehu_tb where user_name=%s and password=%s'
    cursor.execute(sql,(user_name, password))
    reult = cursor.fetchall()
    if len(reult)>0:
        d = reult[0]
        data = {'company_id':d[0], 'company_name':d[1]}
        return json.dumps({'status':200, 'data':data})
    else:
        return json.dumps({'status':400, 'data':'user or password is wrong!'})


def update_manager(tel_num, user_name, pre, manager_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'update manager_tb set user_name=%s,user_auth=%s,user_tel=%s where id=%s'
    num = cursor.execute(sql, ( user_name, pre, tel_num, manager_id))
    db.commit()
    db.close()
    return {'status':200,'message':'ok'}



def is_auth(code):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'select * from manager_tb  WHERE wechat_code=%s'
    cursor.execute(sql,(code,))
    results = cursor.fetchone()
    db.close()
    if results is None:
        data = dict()
        data ['status'] = 400
        return data
    else:
        data = dict()
        data['user_id'] = results[0]
        data['user_auth'] = results[3]
        data['company'] = results[5]
        data['status'] = 200
        return data

def get_device_by_company(company_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT a.id as company_id,b.router_mac,b.router_name,b.on_line,c.dev_mac,c.dev_name,c.color ' \
          'FROM manager_tb a, router_tb b, device_tb c ' \
          'WHERE a.company=%s AND a.id=b.admin_id AND b.router_mac=c.router_mac'
    cursor.execute(sql,(company_id,))
    results = cursor.fetchall()
    db.close()
    dts = []

    for x in results:
        key = str(x[1])+'_'+str(x[2])+'_'+str(x[3])
        rel = -1
        for i in range(len(dts)):
            if dts[i].get(key,None) is not None:
                rel = i
        if rel==-1:
            dts.append({key:[{'dev_mac':x[4],'dev_name':x[5],'dev_color':x[6]}]})
        else:
            dts[rel][key].append({'dev_mac':x[4],'dev_name':x[5],'dev_color':x[6]})
    rts = []
    for k in dts:
        keys = list(k.keys())[0]
        rts.append({'router_mac':keys.split('_')[0],'router_name':keys.split('_')[1],'on_line':keys.split('_')[2],'devices':k[keys]})
    return rts





def get_device_by_user_id(user_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT a.router_mac, a.router_name, a.on_line,b.dev_mac,b.dev_name,b.color ' \
          'FROM router_tb a,device_tb b ' \
          'WHERE a.admin_id=%s AND a.router_mac=b.router_mac'
    cursor.execute(sql,(user_id,))
    results = cursor.fetchall()
    db.close()
    dts = []
    for x in results:
        key = str(x[0]) + '_' + str(x[1])+ '_' + str(x[2])
        rel = -1
        for i in range(len(dts)):
            if dts[i].get(key, None) is not None:
                rel = i
        if rel == -1:
            dts.append({key: [{'dev_mac': x[3], 'dev_name': x[4], 'dev_color': x[5]}]})
        else:
            dts[rel][key].append({'dev_mac': x[3], 'dev_name': x[4], 'dev_color': x[5]})
    rts = []
    for k in dts:
        keys = list(k.keys())[0]
        rts.append({'router_mac': keys.split('_')[0], 'router_name': keys.split('_')[1],
                    'on_line': keys.split('_')[2],'devices': k[keys]})
    return rts


def get_routers_by_company(company_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT a.id as company_id,b.router_mac,b.router_name FROM manager_tb a, router_tb b WHERE a.company=%s AND a.id=b.admin_id'
    cursor.execute(sql,(company_id,))
    results = cursor.fetchall()
    db.close()
    dts = []
    router_name = []
    router_mac = []
    for x in results:
        router_mac.append(x[1])
        router_name.append(x[2])
    return {'router_name': router_name, 'router_mac': router_mac}

def get_routers_by_user_id(user_id):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT router_mac, router_name FROM router_tb WHERE admin_id=%s'
    cursor.execute(sql,(user_id,))
    results = cursor.fetchall()
    db.close()
    dts = []
    router_name = []
    router_mac = []
    for x in results:
        router_mac.append(x[0])
        router_name.append(x[1])
    return {'router_name':router_name,'router_mac':router_mac}


def get_device_detail(mac):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor=db.cursor()
    sql = "select  * FROM device_tb WHERE dev_mac=%s"
    cursor.execute(sql,(mac,))
    des = cursor.description
    results = cursor.fetchall()
    db.close()
    a = {}
    for sel in results:
        for x in range(len(sel)):
            a[str(des[x][0])] = sel[x]
    return json.dumps(a,cls=CJsonEncoder)


def get_devices_by_gateway(mac):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor=db.cursor()
    sql = "select  * FROM device_tb WHERE router_mac=%s"
    cursor.execute(sql,(mac,))
    des = cursor.description
    results = cursor.fetchall()
    db.close()
    dd = []
    for sel in results:
        a = {}
        for x in range(len(sel)):
            a[str(des[x][0])] = sel[x]
        dd.append(a)
    return json.dumps(dd,cls=CJsonEncoder)

def get_devices_detail_gateway(mac):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor=db.cursor()
    sql = "SELECT dev_name, dev_mac,add_time FROM device_tb WHERE router_mac=%s"
    cursor.execute(sql,(mac,))
    des = cursor.description
    results = cursor.fetchall()
    db.close()
    dd = []
    for sel in results:
        a = {}
        for x in range(len(sel)):
            a[str(des[x][0])] = sel[x]
        dd.append(a)
    return json.dumps(dd,cls=CJsonEncoder)

def get_gateway_name(mac):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor=db.cursor()
    sql = "SELECT router_name FROM router_tb  WHERE router_mac=%s"
    cursor.execute(sql,(mac,))
    des = cursor.description
    results = cursor.fetchall()
    db.close()
    dd = []
    for sel in results:
        a = {}
        for x in range(len(sel)):
            a[str(des[x][0])] = sel[x]
        dd.append(a)
    return json.dumps(dd,cls=CJsonEncoder)

def get_devices_by_router(mac):
    db = pymysql.connect(host="localhost", user="root", passwd="900504", db="nst_iot", port=3306, charset='utf8')
    cursor=db.cursor()
    sql = "select  dev_mac FROM device_tb WHERE router_mac=%s"
    cursor.execute(sql,(mac,))
    des = cursor.description
    results = cursor.fetchall()
    db.close()
    dd = []
    for sel in results:
        dd.append(sel[0])
    return json.dumps(dd,cls=CJsonEncoder)

if __name__ == '__main__':
    send_ms('test','13286068506')


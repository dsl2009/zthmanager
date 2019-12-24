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
    sql = 'delete  from manager_tb where id=%s'
    cursor.execute(sql,(manager_id,))
    db.commit()
    db.close()
    return  {'status':200,'message':'ok'}



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






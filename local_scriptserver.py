from collections.abc import Callable, Iterable, Mapping
from typing import Any
from flask import Flask, jsonify, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import COMMASPACE, formatdate
import threading
import json
import time
from template import make_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import locale
import datetime

def send_ya_mail(msg_text: str, data: dict):
    login = 'avangardprint-nn@yandex.ru'
    password = 'K0r0basik'

    msg = MIMEMultipart()
    msg['Subject'] = Header(f'Новый заказ от {data["username"]}', 'utf-8')
    msg['From'] = login
    msg['To'] = login
    msg['Date'] = formatdate(localtime=True)
    template = MIMEText(make_template(data), 'html')
    msg.attach(template)

    print('connect to smt')
    s = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)
    

    # part1 = MIMEText(text, 'plain')
    # part2 = MIMEText(html, 'html')

    try:
        s.starttls()
        s.login(login, password)
        print(f'send mail to {login}')
        s.sendmail(msg['From'], login, msg.as_string())
    except Exception as ex:
        print(ex)
    finally:
        s.quit()

class msg_quetes(threading.Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        while True:
            try:
                mq = read_mq()
                for key, item in mq.items():
                    print(item)
                    send_ya_mail(item['msg'], item['data'])
                    delete_m_f_mq(key)
                    break
            except Exception as e:
                print(e)
            time.sleep(5)

def read_mq():
    with open('./mq.json', 'r') as mq_f:
        mq = json.load(mq_f)
        mq_f.close()
    return mq

def write_mq(msg, data):
    with open('./mq.json', 'r') as mq_f:
        mq = json.load(mq_f)
        mq_f.close()
    n = len(mq)
    mq[n] = {
        'msg' : msg,
        'data' : data
    }
    with open('./mq.json', 'w') as mq_f:
        mq = json.dump(dict(mq), mq_f, ensure_ascii=False, indent=4)
        mq_f.close()

def delete_m_f_mq(key):
    with open('./mq.json', 'r') as mq_f:
        mq = json.load(mq_f)
        mq_f.close()
    del mq[str(key)]
    with open('./mq.json', 'w') as mq_f:
        mq = json.dump(dict(mq), mq_f, ensure_ascii=False, indent=4)
        mq_f.close()

@app.route('/send_message', methods=['POST'])
def send_messege():
    try:
        print('start send process')
        data = request.form  
        username = data['username']
        tel = data['tel']
        email = data['email']
    except Exception as e:
        print(e)
    try:
        question = data['question']
        if question == '':
            question = 'Пользователь не писал никаих вопросов'    
    except:
        question = 'Пользователь не писал никаих вопросов'
    try:
        msg = f'Новый заказ от {formatdate(localtime=True)}. Номер телефона: {tel}, ФИО: {username}, email: {email}, Сообщение: {question}'
        msg_data = {'username':username, 'tel':tel, 'email':email, 'question':question}
        write_mq(msg, msg_data)
        return jsonify({'msg':'ok'}), 200
    except Exception as e:
        print(e)

if __name__ == '__main__':
    t1 = msg_quetes()
    t1.daemon = True
    t1.start()
    app.run(host='0.0.0.0', port=9999, debug=False, ssl_context=("cert.pem", "key.pem"))

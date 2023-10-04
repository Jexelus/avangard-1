from collections.abc import Callable, Iterable, Mapping
from typing import Any
from flask import Flask, jsonify, request
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import COMMASPACE, formatdate
import threading
import json
import time

app = Flask(__name__)

def send_ya_mail(msg_text: str, data: dict):
    login = 'epickgame.cannel@yandex.ru'
    password = 'Jexel1708.'

    msg = MIMEText(f'{msg_text}', 'plain', 'utf-8')
    msg['Subject'] = Header(f'Новый заказ от {data["username"]}', 'utf-8')
    msg['From'] = login
    msg['To'] = login
    msg['Date'] = formatdate(localtime=True)

    print('connect to smt')
    s = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)

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
    print('start send process')
    data = request.form  
    username = data['username']
    tel = data['tel']
    email = data['email']
    try:
        question = data['question']
    except:
        question = 'Пользователь не писал никаих вопросов'
    
    msg = f'Новый заказ от {formatdate(localtime=True)}. Номер телефона: {tel}, ФИО: {username}, email: {email}, Сообщение: {question}'
    msg_data = {'username':username, 'tel':tel, 'email':email}
    write_mq(msg, msg_data)
    return jsonify({'msg':'ok'}), 200

if __name__ == '__main__':
    t1 = msg_quetes()
    t1.daemon = True
    t1.start()
    app.run(host='localhost', port=9999, debug=False)
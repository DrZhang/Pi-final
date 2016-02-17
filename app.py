#encoding=utf8
import random,time
import RPi.GPIO as GPIO
from flask import Flask, make_response,g, request, render_template

app = Flask(__name__)

#内存数据库
dic={}
#柜数量限定
num=6
#控制引脚限定
pin={'E':21,'A':20,'B':16,'C':12}




@app.before_request
def before_request():
    g.db=dic
    pass

@app.teardown_request
def teardown_request(exception):
    pass


#ajax操作接口
#
#
#
@app.route('/ajax',methods=['GET'])
def ajax0():
    k=request.args.get('id',-1)
    vc=None
    vs=None
    if k in request.cookies:
        vc=int(request.cookies.get(k))
    if k in g.db:
        vs=g.db.get(k)        
    if vs is -1:
        token=onSave(k)
        r=make_response('{"state":%d}' %-1)
        r.set_cookie(k,str(token))
        return r
    elif vc == vs:
        onFetch(k)
        r=make_response('{"state":%d}' %1)
        r.set_cookie(k,'',expires=0)
        return r
    else:
        r=make_response('{"state":%d}' %-10)
        return r
        


def onSave(k):
    token=random.randint(1,1<<32)
    g.db[k]=token
    openBox(k)
    return token
    
def onFetch(k):
    g.db[k]=-1
    openBox(k)
    

#开门方法 
def openBox(k):
    s=pinmap[k]
    GPIO.output(pin['A'],s[0])
    GPIO.output(pin['B'],s[1])
    GPIO.output(pin['C'],s[2])
    GPIO.output(pin['E'],True)
    time.sleep(0.2)
    GPIO.output(pin['E'],False)
    


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    for i in range(1,num):
        dic[unicode(i)]=-1
        pinmap[unicode(i)]=bin(i)[2:]

    for key in pin.values:
        GPIO.setup(key,GPIO.OUT)

    app.run('192.168.1.107',8024)
    


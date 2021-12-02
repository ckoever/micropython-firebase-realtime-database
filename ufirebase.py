

import ujson
import usocket
import _thread
import time
import ussl


class rtdb:
  def put(PATH, DATA, DUMP=None, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.rtdb.put, [PATH, ujson.dumps(DATA), DUMP, str(id), cb])
    else:
      INTERNAL.rtdb.put(PATH, ujson.dumps(DATA), DUMP, str(id), cb)
  def patch(PATH, DATATAG, DUMP=None, bg=True, id=0, cb=None):
      if bg:
        _thread.start_new_thread(INTERNAL.rtdb.patch, [PATH, ujson.dumps(DATATAG), DUMP, str(id), cb])
      else:
        INTERNAL.rtdb.patch(PATH, ujson.dumps(DATATAG), DUMP, str(id), cb)
  def getfile(PATH, FILE, DUMP=None, bg=False, id=0, cb=None, limit=False):
      if bg:
        _thread.start_new_thread(INTERNAL.getfile, [PATH, FILE, DUMP, bg, str(id), cb, limit])
      else:
        INTERNAL.getfile(PATH, FILE, DUMP, bg, str(id), cb, limit)
  def get(PATH, DUMP, bg=False, cb=None, id=0, limit=False):
      if bg:
        _thread.start_new_thread(INTERNAL.rtdb.get, [PATH, DUMP, str(id), cb, limit])
      else:
        INTERNAL.rtdb.get(PATH, DUMP, str(id), cb, limit)
  def delete(PATH, DUMP=None, bg=True, id=0, cb=None):
      if bg:
        _thread.start_new_thread(INTERNAL.rtdb.delete, [PATH, DUMP, str(id), cb])
      else:
        INTERNAL.rtdb.delete(PATH, DUMP, str(id), cb)
  def addto(PATH, DATA, DUMP=None, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.rtdb.addto, [PATH, ujson.dumps(DATA), DUMP, str(id), cb])
    else:
      INTERNAL.rtdb.addto(PATH, ujson.dumps(DATA), DUMP, str(id), cb)
  class conf:
    def seturl(url):
      try:
          proto, dummy, host, path = url.split("/", 3)
      except ValueError:
          proto, dummy, host = url.split("/", 2)
          path = ""
      if proto == "http:":

          port = 80
      elif proto == "https:":
          port = 443
      else:
          raise ValueError("Unsupported protocol: " + proto)
      if ":" in host:
          host, port = host.split(":", 1)
          port = int(port)
      VAR.rtdb.url={"proto": proto, "host": host, "port": port}
    def setsecret(secret):
      VAR.rtdb.secret=secret
      VAR.rtdb.ruleurl=("https://"+VAR.rtdb.url+"/.firebaseio/.settings/rules.json?auth="+secret)
    def getrules(DUMP, bg=False, id=0, cb=None):
      if bg:
        _thread.start_new_thread(INTERNAL.rtdb.getrules, [DUMP, id, cb])
      else:
        INTERNAL.rtdb.getrules(DUMP, id, cb)
class auth:
  def selauth(email):
    if str(email) in VAR.auth.list:
      VAR.authct=email
      return 1
    else:
      raise OSError("{email} not signed in. Use auth.signin_ep to enable this feature.".format(email=email))
  def desauth():
    VAR.authct=None
    return 1
  def clear():
    VAR.auth.list={}
  def sign_in_ep(email, passwd, bg=False, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.auth.sign_in_ep, [email, passwd, str(id), cb])
    else:
      INTERNAL.auth.sign_in_ep(email, passwd, str(id), cb)
  def send_password_reset_email(DUMP, bg=False, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.auth.send_password_reset_email,[DUMP, str(id), cb])
    else:
      INTERNAL.auth.send_password_reset_email(DUMP, str(id), cb)
  def sign_up_ep(email, passwd, bg=False, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.auth.sign_up_ep, [email, passwd, str(id), cb])
    else:
      INTERNAL.auth.sign_up_ep(email, passwd, str(id), cb)
  def sign_in_anonym(DUMP, bg=False, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.auth.sign_in_anonym, [DUMP, str(id), cb])
    else:
      INTERNAL.auth.sign_in_anonym(DUMP, str(id), cb)
  def verify_password_reset_code(oobCode, DUMP, bg=False, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.auth.send_password_reset,[oobCode, DUMP, str(id), cb])
    else:
      INTERNAL.auth.send_password_reset(oobCode, DUMP, str(id), cb)
  def confirm_password_reset(oobCode, newpasswd, DUMP, bg=False, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.auth.confirm_password_reset,[oobCode, newpasswd, DUMP, str(id), cb])
    else:
      INTERNAL.auth.confirm_password_reset(oobCode, newpasswd, DUMP, str(id), cb)
  def change_email(newemail, DUMP, bg=False, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.auth.change_email,[newemail, DUMP, str(id), cb])
    else:
      INTERNAL.auth.change_email(newemail, DUMP, str(id), cb)
  def change_password(newpassword, DUMP, bg=False, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.auth.change_email,[newpassword, DUMP, str(id), cb])
    else:
      INTERNAL.auth.change_email(newpassword, DUMP, str(id), cb)

class VAR:
  class auth:
    list={}
    surl="identitytoolkit.googleapis.com"
  class rtdb:
    url=None
    secret=None
    ruleurl=None
  apikey=None
  socklist={}
  authct=None
  
class INTERNAL:
  def checksockav(id):
    try:
      while VAR.socklist["SS"+id]:
        time.sleep(2)
      VAR.socklist["SS"+id]=True
    except:
      VAR.socklist["SS"+id]=True
  def callback(cb):
    try:
      cb[0](*cb[1])
    except:
      try:
        cb[0](cb[1])
      except:
        raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
  def disconnect(id):
        VAR.socklist["SS"+id].close()
        VAR.socklist["SS"+id]=None
        VAR.socklist["S"+id]=None
  def connect(host, port, id):
    LOCAL_ADINFO=usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)[0]
    VAR.socklist["S"+id] = usocket.socket(LOCAL_ADINFO[0], LOCAL_ADINFO[1], LOCAL_ADINFO[2])
    VAR.socklist["S"+id].connect(LOCAL_ADINFO[-1])
    try:
      VAR.socklist["SS"+id] = ussl.wrap_socket(VAR.socklist["S"+id], server_hostname=VAR.rtdb.url["host"])
    except Exception as Exception:
      INTERNAL.disconnect(id)
      raise Exception  
  class rtdb:
    def put(PATH, DATA, DUMP, id, cb):
        INTERNAL.checksockav(id)
        INTERNAL.connect(VAR.rtdb.url["host"], VAR.rtdb.url["port"], id)
        LOCAL_SS=VAR.socklist["SS"+id]
        if VAR.authct:
          INTERNAL.auth.update(VAR.authct)
          LOCAL_SS.write(b"PUT /"+PATH+b".json?auth="+VAR.auth.list[VAR.authct]["idToken"]+b" HTTP/1.0\r\n")
        else:
          LOCAL_SS.write(b"PUT /"+PATH+b".json HTTP/1.0\r\n")
        LOCAL_SS.write(b"Host: "+VAR.rtdb.url["host"]+b"\r\n")
        LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
        LOCAL_SS.write(DATA)
        LOCAL_DATA=LOCAL_SS.read()
        try:
          LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])
          globals()[DUMP]=LOCAL_OUTPUT
        except:
          raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
        INTERNAL.disconnect(id)
        if cb:
          INTERNAL.callback(cb)
    def patch(PATH, DATATAG, DUMP, id, cb):
        INTERNAL.checksockav(id)
        INTERNAL.connect(VAR.rtdb.url["host"], VAR.rtdb.url["port"], id)
        LOCAL_SS=VAR.socklist["SS"+id]
        if VAR.authct:
          INTERNAL.auth.update(VAR.authct)
          LOCAL_SS.write(b"PATCH /"+PATH+b".json?auth="+VAR.auth.list[VAR.authct]["idToken"]+b" HTTP/1.0\r\n")
        else:
          LOCAL_SS.write(b"PATCH /"+PATH+b".json HTTP/1.0\r\n")
        LOCAL_SS.write(b"Host: "+VAR.rtdb.url["host"]+b"\r\n")
        LOCAL_SS.write(b"Content-Length: "+str(len(DATATAG))+"\r\n\r\n")
        LOCAL_SS.write(DATATAG)
        LOCAL_DATA=LOCAL_SS.read()
        try:
          LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])
          globals()[DUMP]=LOCAL_OUTPUT
        except:
          raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
        INTERNAL.disconnect(id)
        if cb:
          INTERNAL.callback(cb)
    def get(PATH, DUMP, id, cb, limit):
        INTERNAL.checksockav(id)
        INTERNAL.connect(VAR.rtdb.url["host"], VAR.rtdb.url["port"], id)
        LOCAL_SS=VAR.socklist["SS"+id]
        if VAR.authct:
          INTERNAL.auth.update(VAR.authct)
          LOCAL_SS.write(b"GET /"+PATH+b".json?auth="+VAR.auth.list[VAR.authct]["idToken"]+b" HTTP/1.0\r\n")
        else:
          LOCAL_SS.write(b"GET /"+PATH+b".json?shallow="+str(limit)+b" HTTP/1.0\r\n")
        LOCAL_SS.write(b"Host: "+VAR.rtdb.url["host"]+b"\r\n\r\n")
        LOCAL_DATA=LOCAL_SS.read()
        try:
          LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])
          globals()[DUMP]=LOCAL_OUTPUT
        except:
          raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
        INTERNAL.disconnect(id)
        if cb:
          INTERNAL.callback(cb)     
    def getfile(PATH, FILE, DUMP, bg, id, cb, limit):
        INTERNAL.checksockav(id)
        INTERNAL.connect(VAR.rtdb.url["host"], VAR.rtdb.url["port"], id)
        LOCAL_SS=VAR.socklist["SS"+id]

        if VAR.authct:
          INTERNAL.auth.update(VAR.authct)
          LOCAL_SS.write(b"GET /"+PATH+b".json?auth="+VAR.auth.list[VAR.authct]["idToken"]+b" HTTP/1.0\r\n")
        else:
            LOCAL_SS.write(b"GET /"+PATH+b".json?shallow="+str(limit)+b" HTTP/1.0\r\n")
        LOCAL_SS.write(b"Host: "+VAR.rtdb.url["host"]+b"\r\n\r\n")
        while not LOCAL_SS.readline()==b"\r\n":
          pass
        LOCAL_FILE=open(FILE, "wb")
        if bg:
          while True:
            LOCAL_LINE=LOCAL_SS.read(1024)

            if LOCAL_LINE==b"":
              break
            LOCAL_FILE.write(LOCAL_LINE)
            time.sleep_ms(1)
        else:
          while True:
            LOCAL_LINE=LOCAL_SS.read(1024)
            if LOCAL_LINE==b"":
              break
            LOCAL_FILE.write(LOCAL_LINE)
        LOCAL_FILE.close()
        LOCAL_DATA=LOCAL_SS.read()
        INTERNAL.disconnect(id)
        if cb:
          INTERNAL.callback(cb)
    def delete(PATH, DUMP, id, cb):
        INTERNAL.checksockav(id)
        INTERNAL.connect(VAR.rtdb.url["host"], VAR.rtdb.url["port"], id)
        LOCAL_SS=VAR.socklist["SS"+id]
        if VAR.authct:
          INTERNAL.auth.update(VAR.authct)

          LOCAL_SS.write(b"DELETE /"+PATH+b".json?auth="+VAR.auth.list[VAR.authct]["idToken"]+b" HTTP/1.0\r\n")
        else:

          LOCAL_SS.write(b"DELETE /"+PATH+b".json HTTP/1.0\r\n")
        LOCAL_SS.write(b"Host: "+VAR.rtdb.url["host"]+b"\r\n\r\n")
        LOCAL_DATA=LOCAL_SS.read()
        try:
          LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])
          globals()[DUMP]=LOCAL_OUTPUT
        except:
          raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
        INTERNAL.disconnect(id)
        if cb:
          INTERNAL.callback(cb)
    def addto(PATH, DATA, DUMP, id, cb):
        INTERNAL.checksockav(id)
        INTERNAL.connect(VAR.rtdb.url["host"], VAR.rtdb.url["port"], id)
        LOCAL_SS=VAR.socklist["SS"+id]

        if VAR.authct:
          INTERNAL.auth.update(VAR.authct)
          LOCAL_SS.write(b"POST /"+PATH+b".json?auth="+VAR.auth.list[VAR.authct]["idToken"]+b" HTTP/1.0\r\n")
        else:
            LOCAL_SS.write(b"POST /"+PATH+b".json"+b" HTTP/1.0\r\n")
        LOCAL_SS.write(b"Host: "+VAR.rtdb.url["host"]+b"\r\n")
        LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
        LOCAL_SS.write(DATA)
        LOCAL_DATA=LOCAL_SS.read()
        try:
          LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])

          globals()[DUMP]=LOCAL_OUTPUT
        except:
          raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
        INTERNAL.disconnect(id)
        if cb:
          INTERNAL.callback(cb)
    def getrules(DUMP, id, cb):
      INTERNAL.checksockav(id)
      INTERNAL.connect(VAR.rtdb.ruleurl, 443, id)
      LOCAL_SS=VAR.socklist["SS"+id]
      LOCAL_SS.write(b"GET "+VAR.rtdb.ruleurl+" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+VAR.rtdb.url["host"]+b"\r\n")
      LOCAL_DATA=LOCAL_SS.read()
      try:
        LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])
        globals()[DUMP]=LOCAL_OUTPUT
      except:
        raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
      INTERNAL.disconnect(id)
      if cb:
        INTERNAL.callback(cb)
    def setrules():
      pass
  class auth:
    def sign_in_ep(email, passwd, id, cb):
      DATA=ujson.dumps({"email":email,"password":passwd,"returnSecureToken":True})
      INTERNAL.checksockav(id)
      INTERNAL.connect(VAR.auth.surl, 443, id)
      LOCAL_SS=VAR.socklist["SS"+id]
      LOCAL_SS.write(b"POST /v1/accounts:signInWithPassword?key="+VAR.apikey+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: identitytoolkit.googleapis.com\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      
      LOCAL_DATA=LOCAL_SS.read()
      
      INTERNAL.disconnect(id)
      try:
        VAR.auth.list[str(email)]={"time": time.mktime(time.localtime()), "passwd": passwd, "idToken": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["idToken"], "expiresIn": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["expiresIn"]}

      except Exception as Exception:
        raise Exception
        raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
      if cb:
          INTERNAL.callback(cb)
    def update(email):
      if ((time.mktime(time.localtime()) - int(VAR.auth.list[str(email)]["time"])) > int(VAR.auth.list[str(email)]['expiresIn']) - 600):
        INTERNAL.auth.add(email, VAR.auth.list[str(email)]["passwd"])
    def send_password_reset_email(DUMP, id, cb):
      DATA=ujson.dumps({"requestType":"PASSWORD_RESET", "email":VAR.auth.list[VAR.authct]["email"]})
      INTERNAL.checksockav(id)
      INTERNAL.connect(VAR.auth.surl, 443, id)
      LOCAL_SS=VAR.socklist["SS"+id]
      LOCAL_SS.write(b"POST https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key="+VAR.apikey+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: identitytoolkit.googleapis.com\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      
      LOCAL_DATA=LOCAL_SS.read()
      
      INTERNAL.disconnect(id)
      LOCAL_DATA=LOCAL_SS.read()
      try:
        LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])
        globals()[DUMP]=LOCAL_OUTPUT
      except:
        raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
      if cb:
        INTERNAL.callback(cb)
    def sign_up_ep(email, passwd, id, cb):
      DATA=ujson.dumps({"email":email,"password":passwd,"returnSecureToken":True})
      INTERNAL.checksockav(id)
      INTERNAL.connect(VAR.auth.surl, 443, id)
      LOCAL_SS=VAR.socklist["SS"+id]
      LOCAL_SS.write(b"POST /v1/accounts:signUp?key="+VAR.apikey+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: identitytoolkit.googleapis.com\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      
      LOCAL_DATA=LOCAL_SS.read()
      
      INTERNAL.disconnect(id)
      try:
        VAR.auth.list[str(email)]={"time": time.mktime(time.localtime()), "passwd": passwd, "idToken": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["idToken"], "expiresIn": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["expiresIn"]}

      except Exception as Exception:
        raise Exception
        raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
      if cb:
          INTERNAL.callback(cb)
    def sign_in_anonym(id, cb):
      DATA=ujson.dumps({"returnSecureToken":True})
      INTERNAL.checksockav(id)
      INTERNAL.connect(VAR.auth.surl, 443, id)
      LOCAL_SS=VAR.socklist["SS"+id]
      LOCAL_SS.write(b"POST /v1/accounts:signUp?key="+VAR.apikey+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: identitytoolkit.googleapis.com\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      
      LOCAL_DATA=LOCAL_SS.read()
      
      INTERNAL.disconnect(id)
      try:
        VAR.auth.list[str(email)]={"time": time.mktime(time.localtime()), "passwd": passwd, "idToken": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["idToken"], "expiresIn": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["expiresIn"]}

      except Exception as Exception:
        raise Exception
        raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
      if cb:
          INTERNAL.callback(cb)
    def verify_password_reset_code(oobCode, DUMP, id, cb):
      DATA=ujson.dumps({"oobCode":oobCode})
      INTERNAL.checksockav(id)
      INTERNAL.connect(VAR.auth.surl, 443, id)
      LOCAL_SS=VAR.socklist["SS"+id]
      LOCAL_SS.write(b"POST https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key="+VAR.apikey+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: identitytoolkit.googleapis.com\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      
      LOCAL_DATA=LOCAL_SS.read()
      
      INTERNAL.disconnect(id)
      LOCAL_DATA=LOCAL_SS.read()
      try:
        LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])
        globals()[DUMP]=LOCAL_OUTPUT
      except:
        raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
      if cb:
        INTERNAL.callback(cb)
    
    def confirm_password_reset(oobCode, newpasswd, DUMP, id, cb):
      DATA=ujson.dumps({"oobCode":oobCode, "newPassword":newpasswd})
      INTERNAL.checksockav(id)
      INTERNAL.connect(VAR.auth.surl, 443, id)
      LOCAL_SS=VAR.socklist["SS"+id]
      LOCAL_SS.write(b"POST https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key="+VAR.apikey+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: identitytoolkit.googleapis.com\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      
      LOCAL_DATA=LOCAL_SS.read()
      
      INTERNAL.disconnect(id)
      LOCAL_DATA=LOCAL_SS.read()
      try:
        LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])
        globals()[DUMP]=LOCAL_OUTPUT
      except:
        raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
      if cb:
        INTERNAL.callback(cb)
    def change_email(newemail, DUMP, id, cb):
      DATA=ujson.dumps({"idToken":VAR.auth.list[VAR.authct]["idToken"],"email":newemail,"returnSecureToken":True})
      INTERNAL.checksockav(id)
      INTERNAL.connect(VAR.auth.surl, 443, id)
      LOCAL_SS=VAR.socklist["SS"+id]
      LOCAL_SS.write(b"POST /v1/accounts:signInWithPassword?key="+VAR.apikey+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: identitytoolkit.googleapis.com\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      
      LOCAL_DATA=LOCAL_SS.read()
      
      INTERNAL.disconnect(id)
      try:
        VAR.auth.list[str(email)]={"time": time.mktime(time.localtime()), "passwd": passwd, "idToken": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["idToken"], "expiresIn": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["expiresIn"]}

      except Exception as Exception:
        raise Exception
        raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
      if cb:
          INTERNAL.callback(cb)
    def change_password(newpassword, DUMP, id, cb):
      DATA=ujson.dumps({"idToken":VAR.auth.list[VAR.authct]["idToken"],"password":newpassword,"returnSecureToken":True})
      INTERNAL.checksockav(id)
      INTERNAL.connect(VAR.auth.surl, 443, id)
      LOCAL_SS=VAR.socklist["SS"+id]
      LOCAL_SS.write(b"POST /v1/accounts:signInWithPassword?key="+VAR.apikey+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: identitytoolkit.googleapis.com\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      
      LOCAL_DATA=LOCAL_SS.read()
      
      INTERNAL.disconnect(id)
      try:
        VAR.auth.list[str(email)]={"time": time.mktime(time.localtime()), "passwd": passwd, "idToken": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["idToken"], "expiresIn": ujson.loads(LOCAL_DATA.replace(b"\n", b"").splitlines()[-1])["expiresIn"]}

      except Exception as Exception:
        raise Exception
        raise OSError("parse error:\r\n  {val}".format(val=LOCAL_DATA))
      if cb:
          INTERNAL.callback(cb)

def setapikey(key):
  VAR.apikey=key


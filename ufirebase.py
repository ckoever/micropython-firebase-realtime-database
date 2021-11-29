

import ujson
import usocket
import _thread
import time
import ussl

class FIREBASE_VAR:
  URL=None
  URL_ADINFO=None
  APIKEY=None
  AUTH={}
  AUTHCT=None
  SLIST={}
  
class INTERNAL:
  class AUTH:
    def add(email, passwd, id, cb):
      DATA=ujson.dumps({"email":email,"password":passwd,"returnSecureToken":True})
      
      LOCAL_ADINFO=usocket.getaddrinfo("identitytoolkit.googleapis.com", 443, 0, usocket.SOCK_STREAM)[0]
      FIREBASE_VAR.SLIST["S"+id] = usocket.socket(LOCAL_ADINFO[0], LOCAL_ADINFO[1], LOCAL_ADINFO[2])
      FIREBASE_VAR.SLIST["S"+id].connect(LOCAL_ADINFO[-1])
      try:
        FIREBASE_VAR.SLIST["SS"+id] = ussl.wrap_socket(FIREBASE_VAR.SLIST["S"+id], server_hostname="identitytoolkit.googleapis.com")
      except Exception as Exception:
        FIREBASE_VAR.SLIST["S"+id].close()
        FIREBASE_VAR.SLIST["SS"+id]=None
        FIREBASE_VAR.SLIST["S"+id]=None
        raise Exception
      
      LOCAL_SS=FIREBASE_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"POST /v1/accounts:signInWithPassword?key="+FIREBASE_VAR.APIKEY+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: identitytoolkit.googleapis.com\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      
      LOCAL_DATA=LOCAL_SS.read()
      FIREBASE_VAR.AUTH[str(email)]={"time": time.mktime(time.localtime()), "passwd": passwd, "idToken": eval(LOCAL_DATA.splitlines()[-5].split()[-1].strip(b',')), "expiresIn": int(eval(LOCAL_DATA.splitlines()[-2].split()[-1].strip(b',')))}
      
      FIREBASE_VAR.SLIST["SS"+id].close()
      FIREBASE_VAR.SLIST["SS"+id]=None
      FIREBASE_VAR.SLIST["S"+id]=None
      
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
    def update(email):
      if ((time.mktime(time.localtime()) - int(FIREBASE_VAR.AUTH[str(email)]["time"])) > int(FIREBASE_VAR.AUTH[str(email)]['expiresIn']) - 600):
        INTERNAL.AUTH.add(email, FIREBASE_VAR.AUTH[str(email)]["passwd"])

  def connect(id):
    LOCAL_ADINFO=usocket.getaddrinfo(FIREBASE_VAR.URL_ADINFO["host"], FIREBASE_VAR.URL_ADINFO["port"], 0, usocket.SOCK_STREAM)[0]
    FIREBASE_VAR.SLIST["S"+id] = usocket.socket(LOCAL_ADINFO[0], LOCAL_ADINFO[1], LOCAL_ADINFO[2])
    FIREBASE_VAR.SLIST["S"+id].connect(LOCAL_ADINFO[-1])
    if FIREBASE_VAR.URL_ADINFO["proto"] == "https:":
      try:
        FIREBASE_VAR.SLIST["SS"+id] = ussl.wrap_socket(FIREBASE_VAR.SLIST["S"+id], server_hostname=FIREBASE_VAR.URL_ADINFO["host"])
      except Exception as Exception:
        FIREBASE_VAR.SLIST["S"+id].close()
        FIREBASE_VAR.SLIST["SS"+id]=None
        FIREBASE_VAR.SLIST["S"+id]=None
        raise Exception 
    else:
      FIREBASE_VAR.SLIST["SS"+id]=FIREBASE_VAR.SLIST["S"+id]
  def disconnect(id):
      FIREBASE_VAR.SLIST["SS"+id].close()
      FIREBASE_VAR.SLIST["SS"+id]=None
      FIREBASE_VAR.SLIST["S"+id]=None
        
  def put(PATH, DATA, id, cb):
      try:
        while FIREBASE_VAR.SLIST["SS"+id]:
          time.sleep(2)
        FIREBASE_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_VAR.SLIST["SS"+id]
      if FIREBASE_VAR.AUTHCT:
        INTERNAL.AUTH.update(FIREBASE_VAR.AUTHCT)
        LOCAL_SS.write(b"PUT /"+PATH+b".json?auth="+FIREBASE_VAR.AUTH[FIREBASE_VAR.AUTHCT]["idToken"]+b" HTTP/1.0\r\n")
      else:
        LOCAL_SS.write(b"PUT /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_VAR.URL_ADINFO["host"]+b"\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      LOCAL_DUMMY=LOCAL_SS.read()
      print(LOCAL_DUMMY)
      del LOCAL_DUMMY
      INTERNAL.disconnect(id)
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
  def patch(PATH, DATATAG, id, cb):
      try:
        while FIREBASE_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_VAR.SLIST["SS"+id]
      if FIREBASE_VAR.AUTHCT:
        INTERNAL.AUTH.update(FIREBASE_VAR.AUTHCT)
        LOCAL_SS.write(b"PATCH /"+PATH+b".json?auth="+FIREBASE_VAR.AUTH[FIREBASE_VAR.AUTHCT]["idToken"]+b" HTTP/1.0\r\n")
      else:
        LOCAL_SS.write(b"PATCH /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_VAR.URL_ADINFO["host"]+b"\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATATAG))+"\r\n\r\n")
      LOCAL_SS.write(DATATAG)
      LOCAL_DUMMY=LOCAL_SS.read()
      print(LOCAL_DUMMY)
      del LOCAL_DUMMY
      INTERNAL.disconnect(id)
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
  def get(PATH, DUMP, id, cb, limit):
      try:
        while FIREBASE_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_VAR.SLIST["SS"+id]
      if FIREBASE_VAR.AUTHCT:
        INTERNAL.AUTH.update(FIREBASE_VAR.AUTHCT)
        LOCAL_SS.write(b"GET /"+PATH+b".json?auth="+FIREBASE_VAR.AUTH[FIREBASE_VAR.AUTHCT]["idToken"]+b" HTTP/1.0\r\n")
      else:
        LOCAL_SS.write(b"GET /"+PATH+b".json?shallow="+str(limit)+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_VAR.URL_ADINFO["host"]+b"\r\n\r\n")
      LOCAL_DATA=LOCAL_SS.read()
      try:
        LOCAL_OUTPUT=ujson.loads(LOCAL_DATA.splitlines()[-1])
        globals()[DUMP]=LOCAL_OUTPUT
      except:
        print(LOCAL_DATA)
      INTERNAL.disconnect(id)
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")      
  def getfile(PATH, FILE, bg, id, cb, limit):
      try:
        while FIREBASE_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_VAR.SLIST["SS"+id]
      if FIREBASE_VAR.AUTHCT:
        INTERNAL.AUTH.update(FIREBASE_VAR.AUTHCT)
        LOCAL_SS.write(b"GET /"+PATH+b".json?auth="+FIREBASE_VAR.AUTH[FIREBASE_VAR.AUTHCT]["idToken"]+b" HTTP/1.0\r\n")
      else:
          LOCAL_SS.write(b"GET /"+PATH+b".json?shallow="+str(limit)+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_VAR.URL_ADINFO["host"]+b"\r\n\r\n")
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
      LOCAL_DUMMY=LOCAL_SS.read()
      del LOCAL_DUMMY
      INTERNAL.disconnect(id)
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
  def delete(PATH, id, cb):
      try:
        while FIREBASE_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_VAR.SLIST["SS"+id]
      if FIREBASE_VAR.AUTHCT:
        INTERNAL.AUTH.update(FIREBASE_VAR.AUTHCT)
        LOCAL_SS.write(b"DELETE /"+PATH+b".json?auth="+FIREBASE_VAR.AUTH[FIREBASE_VAR.AUTHCT]["idToken"]+b" HTTP/1.0\r\n")
      else:
        LOCAL_SS.write(b"DELETE /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_VAR.URL_ADINFO["host"]+b"\r\n\r\n")
      LOCAL_DUMMY=LOCAL_SS.read()
      print(LOCAL_DUMMY)
      del LOCAL_DUMMY
      INTERNAL.disconnect(id)
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
      
  def addto(PATH, DATA, DUMP, id, cb):
      try:
        while FIREBASE_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_VAR.SLIST["SS"+id]
      if FIREBASE_VAR.AUTHCT:
        INTERNAL.AUTH.update(FIREBASE_VAR.AUTHCT)
        LOCAL_SS.write(b"POST /"+PATH+b".json?auth="+FIREBASE_VAR.AUTH[FIREBASE_VAR.AUTHCT]["idToken"]+b" HTTP/1.0\r\n")
      else:
          LOCAL_SS.write(b"POST /"+PATH+b".json"+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_VAR.URL_ADINFO["host"]+b"\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      LOCAL_DUMMY=ujson.loads(LOCAL_SS.read().splitlines()[-1])
      print(LOCAL_DUMMY)
      del LOCAL_DUMMY
      INTERNAL.disconnect(id)
      if DUMP:
        s()[DUMP]=LOCAL_OUTPUT["name"]
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
    
def setURL(url):
    FIREBASE_VAR.URL=url
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

    FIREBASE_VAR.URL_ADINFO={"proto": proto, "host": host, "port": port}
    
def setAPIKEY(key):
  FIREBASE_VAR.APIKEY=key
def addAUTH(email, passwd, bg=False, id=0, cb=None):
  if str(email) in FIREBASE_VAR.AUTH:
    return 1
  else:
    if bg:
      _thread.start_new_thread(INTERNAL.AUTH.add, [email, passwd, str(id), cb])
      return 2
    else:
      INTERNAL.AUTH.add(email, passwd, str(id), cb)
      return 1
def selAUTH(email):
  if str(email) in FIREBASE_VAR.AUTH:
    FIREBASE_VAR.AUTHCT=email
    return 1
  else:
    return 0
def desAUTH():
  FIREBASE_VAR.AUTHCT=None
def remAUTH(email):
  if str(email) in FIREBASE_VAR.AUTH:
    FIREBASE_VAR.AUTH.pop(str(email))
    return 1
  else:
    return 0
def put(PATH, DATA, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.put, [PATH, ujson.dumps(DATA), str(id), cb])
    else:
      INTERNAL.put(PATH, ujson.dumps(DATA), str(id), cb)
def patch(PATH, DATATAG, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.patch, [PATH, ujson.dumps(DATATAG), str(id), cb])
    else:
      INTERNAL.patch(PATH, ujson.dumps(DATATAG), str(id), cb)
def getfile(PATH, FILE, bg=False, id=0, cb=None, limit=False):
    if bg:
      _thread.start_new_thread(INTERNAL.getfile, [PATH, FILE, bg, str(id), cb, limit])
    else:
      INTERNAL.getfile(PATH, FILE, bg, str(id), cb, limit)
def get(PATH, DUMP, bg=False, cb=None, id=0, limit=False):
    if bg:
      _thread.start_new_thread(INTERNAL.get, [PATH, DUMP, str(id), cb, limit])
    else:
      INTERNAL.get(PATH, DUMP, str(id), cb, limit)
def delete(PATH, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.delete, [PATH, str(id), cb])
    else:
      INTERNAL.delete(PATH, str(id), cb)
def addto(PATH, DATA, DUMP=None, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.addto, [PATH, ujson.dumps(DATA), DUMP, str(id), cb])
    else:
      INTERNAL.addto(PATH, ujson.dumps(DATA), DUMP, str(id), cb)

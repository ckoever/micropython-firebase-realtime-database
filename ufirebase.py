import ujson
import usocket
import ussl
import _thread
import time

class FIREBASE_GLOBAL_VAR:
    GLOBAL_URL=None
    GLOBAL_URL_ADINFO=None
    SLIST={}

class INTERNAL:
  def connect(id):
      LOCAL_ADINFO=usocket.getaddrinfo(FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"], FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["port"], 0, usocket.SOCK_STREAM)[0]
      FIREBASE_GLOBAL_VAR.SLIST["S"+id] = usocket.socket(LOCAL_ADINFO[0], LOCAL_ADINFO[1], LOCAL_ADINFO[2])
      FIREBASE_GLOBAL_VAR.SLIST["S"+id].connect(LOCAL_ADINFO[-1])
      if FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["proto"] == "https:":
          try:
            FIREBASE_GLOBAL_VAR.SLIST["SS"+id] = ussl.wrap_socket(FIREBASE_GLOBAL_VAR.SLIST["S"+id], server_hostname=FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"])
          except:
            print("ENOMEM, try to restart. If you make to many id's (sokets) simultaneously (bg=1 and id=x), try to use less or use a board with more ram!\nSome emulation software limits the RAM.")
            FIREBASE_GLOBAL_VAR.SLIST["S"+id].close()
            FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=None
            FIREBASE_GLOBAL_VAR.SLIST["S"+id]=None
            raise MemoryError
            
      else:
          FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=FIREBASE_GLOBAL_VAR.SLIST["S"+id]
  def disconnect(id):
      FIREBASE_GLOBAL_VAR.SLIST["SS"+id].close()
      FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=None
      FIREBASE_GLOBAL_VAR.SLIST["S"+id]=None
        
  def put(PATH, DATA, id, cb):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(2)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"PUT /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
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


  def patch(PATH, DATATAG, id, cb):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"PATCH /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATATAG))+"\r\n\r\n")
      LOCAL_SS.write(DATATAG)
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

  def get(PATH, DUMP, id, cb, limit):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"GET /"+PATH+b".json?shallow="+ujson.dumps(limit)+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
      LOCAL_OUTPUT=ujson.loads(LOCAL_SS.read().splitlines()[-1])
      INTERNAL.disconnect(id)
      globals()[DUMP]=LOCAL_OUTPUT
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
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"GET /"+PATH+b".json?shallow="+ujson.dumps(limit)+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
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
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"DELETE /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
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
      
  def addto(PATH, DATA, DUMP, id, cb):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"POST /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      LOCAL_OUTPUT=ujson.loads(LOCAL_SS.read().splitlines()[-1])
      INTERNAL.disconnect(id)
      if DUMP:
        globals()[DUMP]=LOCAL_OUTPUT["name"]
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
    
def setURL(url):
    FIREBASE_GLOBAL_VAR.GLOBAL_URL=url
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
        
    FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO={"proto": proto, "host": host, "port": port}

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

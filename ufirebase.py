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
            print("ENOMEM, try to restart. Do not make to many id's (sokets) simultaneously! (or use a board with more ram)")
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
        
  def put(PATH, DATA, id):
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


  def patch(PATH, DATATAG, id):
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

  def get(PATH, DUMP, id):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"GET /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
      LOCAL_OUTPUT=ujson.loads(LOCAL_SS.read().splitlines()[-1])
      INTERNAL.disconnect(id)
      globals()[DUMP]=LOCAL_OUTPUT
      
  def getfile(PATH, FILE, bg, id):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"GET /"+PATH+b".json HTTP/1.0\r\n")
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
      INTERNAL.disconnect(id)

  def delete(PATH, id):
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
      
  def addto(PATH, DATA, DUMP, id):
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
        globals()[DUMP]=LOCAL_OUTPUT
    
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

def put(PATH, DATA, bg=True, id=0):
    if bg:
      _thread.start_new_thread(INTERNAL.put, [PATH, ujson.dumps(DATA), str(id)])
    else:
      INTERNAL.put(PATH, ujson.dumps(DATA), str(id))

def patch(PATH, DATATAG, bg=True, id=0):
    if bg:
      _thread.start_new_thread(INTERNAL.patch, [PATH, ujson.dumps(DATATAG), str(id)])
    else:
      INTERNAL.patch(PATH, ujson.dumps(DATATAG), str(id))

def getfile(PATH, FILE, bg=False, id=0):
    if bg:
      _thread.start_new_thread(INTERNAL.getfile, [PATH, FILE, bg, str(id)])
    else:
      INTERNAL.getfile(PATH, FILE, bg, str(id))

def get(PATH, DUMP, bg=False, id=0):
    if bg:
      _thread.start_new_thread(INTERNAL.get, [PATH, DUMP, str(id)])
    else:
      INTERNAL.get(PATH, DUMP, str(id))
      
def delete(PATH, bg=True, id=0):
    if bg:
      _thread.start_new_thread(INTERNAL.delete, [PATH, str(id)])
    else:
      INTERNAL.delete(PATH, str(id))
    
def addto(PATH, DATA, DUMP=None, bg=True, id=0):
    if bg:
      _thread.start_new_thread(INTERNAL.addto, [PATH, ujson.dumps(DATA), DUMP, str(id)])
    else:
      INTERNAL.addto(PATH, ujson.dumps(DATA), DUMP, str(id))



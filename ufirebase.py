import ujson
import usocket
import ussl
import _thread
import time

class FIREBASE_GLOBAL_VAR:
    GLOBAL_URL=None
    GLOBAL_URL_ADINFO=None
    SOCKET=None
    SSOCKET=None

class INTERNAL:
  def connect():
      LOCAL_ADINFO=usocket.getaddrinfo(FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"], FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["port"], 0, usocket.SOCK_STREAM)[0]
      FIREBASE_GLOBAL_VAR.SOCKET = usocket.socket(LOCAL_ADINFO[0], LOCAL_ADINFO[1], LOCAL_ADINFO[2])
      FIREBASE_GLOBAL_VAR.SOCKET.connect(LOCAL_ADINFO[-1])
      if FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["proto"] == "https:":
          FIREBASE_GLOBAL_VAR.SSOCKET = ussl.wrap_socket(FIREBASE_GLOBAL_VAR.SOCKET, server_hostname=FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"])
      else:
          FIREBASE_GLOBAL_VAR.SSOCKET=FIREBASE_GLOBAL_VAR.SOCKET
  def disconnect():
      FIREBASE_GLOBAL_VAR.SSOCKET.close()
      FIREBASE_GLOBAL_VAR.SSOCKET=None
      FIREBASE_GLOBAL_VAR.SOCKET=None
        
  def put(PATH, DATA):
      while FIREBASE_GLOBAL_VAR.SSOCKET:
        time.sleep(1)
      FIREBASE_GLOBAL_VAR.SSOCKET=True
      INTERNAL.connect()
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"PUT /"+PATH+b".json HTTP/1.0\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(DATA)
      LOCAL_DUMMY=FIREBASE_GLOBAL_VAR.SSOCKET.read()
      del LOCAL_DUMMY
      INTERNAL.disconnect()


  def patch(PATH, DATA):
      while FIREBASE_GLOBAL_VAR.SSOCKET:
        time.sleep(1)
      FIREBASE_GLOBAL_VAR.SSOCKET=True
      INTERNAL.connect()
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"PATCH /"+PATH+b".json HTTP/1.0\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(DATA)
      LOCAL_DUMMY=FIREBASE_GLOBAL_VAR.SSOCKET.read()
      del LOCAL_DUMMY
      INTERNAL.disconnect()


  def get(PATH, DUMP):
      while FIREBASE_GLOBAL_VAR.SSOCKET:
        time.sleep(1)
      FIREBASE_GLOBAL_VAR.SSOCKET=True
      INTERNAL.connect()
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"GET /"+PATH+b".json HTTP/1.0\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
      LOCAL_OUTPUT=ujson.loads(FIREBASE_GLOBAL_VAR.SSOCKET.read().splitlines()[-1])
      INTERNAL.disconnect()
      globals()[DUMP]=LOCAL_OUTPUT
      
  def getfile(PATH, FILE, bg):
      while FIREBASE_GLOBAL_VAR.SSOCKET:
        time.sleep(1)
      FIREBASE_GLOBAL_VAR.SSOCKET=True
      INTERNAL.connect()
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"GET /"+PATH+b".json HTTP/1.0\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
      while not FIREBASE_GLOBAL_VAR.SSOCKET.readline()==b"\r\n":
        pass
      LOCAL_FILE=open(FILE, "wb")
      if bg:
        while True:
          LOCAL_LINE=FIREBASE_GLOBAL_VAR.SSOCKET.read(1024)
          if LOCAL_LINE==b"":
            break
          LOCAL_FILE.write(LOCAL_LINE)
          time.sleep_ms(1)
      else:
        while True:
          LOCAL_LINE=FIREBASE_GLOBAL_VAR.SSOCKET.read(1024)
          if LOCAL_LINE==b"":
            break
          LOCAL_FILE.write(LOCAL_LINE)

      LOCAL_FILE.close()
      INTERNAL.disconnect()

  def delete(PATH):
      while FIREBASE_GLOBAL_VAR.SSOCKET:
        time.sleep(1)
      FIREBASE_GLOBAL_VAR.SSOCKET=True
      INTERNAL.connect()
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"DELETE /"+PATH+b".json HTTP/1.0\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
      LOCAL_DUMMY=FIREBASE_GLOBAL_VAR.SSOCKET.read()
      del LOCAL_DUMMY
      INTERNAL.disconnect()
      
  def addto(PATH, DATA):
      while FIREBASE_GLOBAL_VAR.SSOCKET:
        time.sleep(1)
      FIREBASE_GLOBAL_VAR.SSOCKET=True
      INTERNAL.connect()
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"POST /"+PATH+b".json HTTP/1.0\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      FIREBASE_GLOBAL_VAR.SSOCKET.write(DATA)
      LOCAL_DUMMY=FIREBASE_GLOBAL_VAR.SSOCKET.read()
      del LOCAL_DUMMY
      INTERNAL.disconnect()
    
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

def put(PATH, DATA):
    _thread.start_new_thread(INTERNAL.put, [PATH, ujson.dumps(DATA)])


def patch(PATH, DATA):
    _thread.start_new_thread(INTERNAL.addto, [PATH, ujson.dumps(DATA)])

def getfile(PATH, FILE, bg=False):
    if bg:
      _thread.start_new_thread(INTERNAL.getfile, [PATH, FILE, bg])
    else:
      INTERNAL.getfile(PATH, FILE, bg)

def get(PATH, DUMP, bg=False):
    if bg:
      _thread.start_new_thread(INTERNAL.get, [PATH, DUMP])
    else:
      INTERNAL.get(PATH, DUMP)
      
def delete(PATH):
    _thread.start_new_thread(INTERNAL.delete, [PATH])
    
def addto(PATH, DATA):
    _thread.start_new_thread(INTERNAL.addto, [PATH, ujson.dumps(DATA)])

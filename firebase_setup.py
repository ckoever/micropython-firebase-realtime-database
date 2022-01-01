


import usocket
import ussl
import network
import sys
import os
import ujson
import machine

# Edit if needed
HOST = "raw.githubusercontent.com"
PORT = 443
REPO = "ckoever/micropython-firebase-realtime-database"
BRANCH = "beta"
PATH = "_components"

# Constants for the setup process
TXT_NOSUPPORT =\
"This script can only be run on an esp32 or esp8266."
TXT_UNTESTED =\
"This script has not been tested on this platform."
TXT_WELCOME =\
"Welcome to the micropython-firebase automatic setup script.\n\
This script makes it possible to download individual components of\n\
micropython-firebase in order to use the memory of micropython boards efficiently."
TXT_WLANCON =\
"Please connect to the internet."
TXT_AVPARTS =\
"Available parts:"


class setup:
  def __init__(self):
    if sys.platform == "esp32":
      self.initial_step()
    elif sys.platform == "esp8266":
      print(TXT_UNTESTED)
      self.initial_step()

    else:
      print(TXT_NOSUPPORT)
      
  def initial_step(self):
    print(TXT_WELCOME+"\n"+TXT_WLANCON)
    SSID = str(input("SSID str> "))
    PASSWD = str(input("PASSWORD str> "))
    self.connect_network(SSID, PASSWD)
    self.download_parts(self.get_parts())
    
  def download_parts(self, parts):
    file = open("test.py", "wb")
    for item in parts:
      print(item+"...")
      file.write(self.getfile(item))
    file.close()
    print("Finished")
    
  def get_parts(self):
    structure = ujson.loads(self.getfile(".structure").replace(b"\n", b""))
    selected = {}
    global parts
    parts = {}
    download_list = []
    print(TXT_AVPARTS)
    count = 1
    sel_number = "1"
    seek=0
    
    for part in structure.keys():
      selected[str(count)] = True if (count == 1) else False
      count+=1
    
    print("Enter the number of the component to toggle\nEnter 0 to finish")

    while sel_number != "0":
      if (sel_number in selected):
        selected[str(sel_number)] = False if selected[str(sel_number)] else True
        self.list_sel_parts(structure, selected)
      sel_number = input("n/0 int> ")
    
    count = 1
    for part in structure.keys():
      if selected[str(count)]:
        parts[part] = structure[part]
      count+=1
    
    for part in parts.keys():
      if not (parts[part][0] in download_list):
        download_list.append(parts[part][0])
      seek=download_list.index(parts[part][0])+1
      if not (parts[part][1] in download_list):
        download_list.insert(seek, parts[part][1])
      seek=download_list.index(parts[part][1])+1
      for item in parts[part][2]:
        if not (item in download_list):
          download_list.insert(seek, item)
      if not (parts[part][3] in download_list):
        download_list.append(parts[part][3])
      seek=download_list.index(parts[part][3])+1
      if not (parts[part][4] in download_list):
        download_list.insert(seek, parts[part][4])
      seek=download_list.index(parts[part][4])+1
      for item in parts[part][5]:
        if not (item in download_list):
          download_list.insert(seek, item)
    
    return download_list
  
  def list_sel_parts(self, structure, selected):
    count = 1
    for part in structure.keys():
      print("{E1}. [{E2}] {E3}".format(E1=count, E2="x" if selected[str(count)] else " ", E3=part))
      count+=1
  def connect_network(self, ssid, passwd):
    self.wlan=network.WLAN(network.STA_IF)
    self.wlan.active(True)
    self.wlan.connect(ssid, passwd)
    while not self.wlan.isconnected():
      machine.idle()

  def open_connection(self):
    CONADD = usocket.getaddrinfo(HOST, PORT, 0, usocket.SOCK_STREAM)[0]
    unsecureCON = usocket.socket(CONADD[0], CONADD[1], CONADD[2])
    unsecureCON.connect(CONADD[-1])
    self.CON = ussl.wrap_socket(unsecureCON, server_hostname=HOST)
    
  def close_connection(self):
    self.CON.close()
    
  def getfile(self, file):
    self.open_connection()
    self.CON.write(b"GET /{E1}/{E2}/{E3}/{E4} HTTP/1.0\r\n".format(E1=REPO, E2=BRANCH, E3=PATH, E4=file))
    self.CON.write(b"Host: {E1}\r\n\r\n".format(E1=HOST))
    data = self.CON.read().split(b"\r")[-1]
    self.close_connection()
    return data

setup()



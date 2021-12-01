



import machine
#HIGLY RECOMMENDED
machine.freq(240000000) #Max clk of the mcu
import os
import time
import network

#Connect to Wifi
GLOB_WLAN=network.WLAN(network.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect("[SSID]", "[PASSWD]")

#firebase example
import ufirebase as firebase

def callbackfunc():
  print("\nlolval_1: "+str(firebase.lolwhat["testval"]["somenumbers"])+
  "\nlolval_2: "+str(firebase.lolwhat["testval"]["something"])+
  "\nlolall: "+str(firebase.lolwhat))
  
def callbackfunc2():
  print(firebase.testtag)

def main():
  firebase.auth.selauth("[EMAIL]")
  firebase.rtdb.seturl("https://[RTDB].firebaseio.com/")

  #Put Tag1
  firebase.rtdb.put("testtag", "1234", bg=0)

  #Put Tag2
  firebase.rtdb.put("lolval/testval", {"somenumbers": [1,2,3], "something": "lol"}, bg=0)

  #Get Tag1
  firebase.rtdb.get("testtag", "var1", bg=0)
  print("testtag: "+str(firebase.var1))

  #Get Tag2+Tag1 as callback and background thread
  firebase.rtdb.get("lolval", "lolwhat", bg=1, cb=(callbackfunc, ()))
  firebase.rtdb.get("testtag", "testtag", bg=1, id=1, cb=(callbackfunc2, ()))
  print(end="Im getting lolval now")

  #Do something while thread runs in bg
  while 1:
    print(end=".")
    time.sleep(.100)
    try: 
      firebase.lolwhat
      break
    except:
      pass
      

  firebase.auth.desauth()
  firebase.rtdb.get("testtag", "var1", bg=0)
  print("testtag: "+str(firebase.var1))
  print(time.ticks_ms())
  
firebase.setapikey("[APIKEY]")
#Sign in with auth (bg in combination with cb higly recommended but not necessary)
firebase.auth.sign_in_ep("[EMAIL]", "[PASSWD]", id=0, cb=(main, ()), bg=True)

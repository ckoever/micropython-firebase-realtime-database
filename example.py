import os as MOD_OS
import network as MOD_NETWORK
import time as MOD_TIME

#Connect to Wifi
GLOB_WLAN=MOD_NETWORK.WLAN(MOD_NETWORK.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect("[SSID]", "[PASSWD]")

while not GLOB_WLAN.isconnected():
  pass

#firebase example
import ufirebase as firebase
firebase.setURL("https://[PROJECT_ID].firebaseio.com/")

#Put Tag1
firebase.put("testtag", "1234", bg=0)

#Put Tag2
firebase.put("lolval/testval", {"somenumbers": [1,2,3], "something": "lol"}, bg=0)

#Get Tag1
firebase.get("testtag", "var1", bg=0)
print("testtag: "+str(firebase.var1))

#Get Tag2
def callbackfunc():
  print("\nlolval_1: "+str(firebase.lolwhat["testval"]["somenumbers"])+
  "\nlolval_2: "+str(firebase.lolwhat["testval"]["something"])+
  "\nlolall: "+str(firebase.lolwhat))

firebase.get("lolval", "lolwhat", bg=1, cb=(callbackfunc, ()))
print(end="Im getting lolval now")

#Do something in this time
while 1:
  print(end=".")
  MOD_TIME.sleep(.100)
  try: 
    firebase.lolwhat
    break
  except:
    pass

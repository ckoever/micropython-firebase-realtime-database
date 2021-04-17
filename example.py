import os as MOD_OS
import network as MOD_NETWORK
import time as MOD_TIME

#Connect to Wifi
GLOB_WLAN=MOD_NETWORK.WLAN(MOD_NETWORK.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect("YOURSSID", "YOURPASSWD")

#firebase example
import ufirebase as firebase
firebase.setURL("https://YOURDATABASE")

#Put Tag1
firebase.put("testtag", "1234", bg=0)

#Put Tag2
firebase.put("lolval/testval", {"somenumbers": [1,2,3], "something": "lol"}, bg=0)

#Get Tag1
firebase.get("testtag", "var1", bg=0)
print(firebase.var1)

#Get Tag2
firebase.get("lolval", "lolwhat", bg=1)
print("Im Downloading...")
time.sleep(5) #Do something in this time
print("lolval_1: "+str(firebase.lolwhat["testval"]["somenumbers"])+
  "\nlolval_2: "+str(firebase.lolwhat["testval"]["something"])+
  "\nlolall: "+str(firebase.lolwhat))

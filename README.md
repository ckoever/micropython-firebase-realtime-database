# micropython-firebase-realtime-database
**Firebase implementation** based on [REST API](https://firebase.google.com/docs/reference/rest/database) optimized for the [ESP32 version of Micropython](https://github.com/micropython/micropython-esp32) based on [firebase-micropython-esp32](https://github.com/vishal-android-freak/firebase-micropython-esp32) from vishal-android-freak. It shouldn't be a problem to run it on other Micropython platforms.


### Commands that are implemented
```
- get (equal GET)
- getfile (equal GET)*
- put (equal PUT)
- patch (equal PATCH)
- addto (equal POST)
- delete (equal DELETE)
```
> *getfile writes the data to a file to avoid RAM overflow

### Required modules
```
ujson, usocket, ussl, _thread, time
```

### Preparations
1. Create a [Firebase Realtime Database](https://firebase.google.com/products/realtime-database). (Console>Add Project>Realtime Database>Create Database)

In the end it should look something like this:

![image](https://user-images.githubusercontent.com/77546092/114287154-f6071b00-9a64-11eb-9214-de75753a71c3.png)

2. Set rules to **public** * *(from now the data can be read and changed by anyone ⚠️)* *
_
```java
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```
3. Note the URL of the database
```
https://[PROJECT_ID].firebaseio.com/
```
## Example
### 1. Connect to Wifi

```python
import os
import network
wlan = network.WLAN(network.STA_IF)
if not wlan.active() or not wlan.isconnected():
  wlan.active(True)
  wlan.connect("SSID", "PASSWD")
  while not wlan.isconnected():
    pass
```

### 2. Set the URL of the database
```python
import ufirebase as firebase
firebase.setURL("https://[PROJECT_ID].firebaseio.com/")
```

### Get data from the database (optional run in the background)*
>*In this case you have to pay attention to the timing yourself, because the data needs time to be downloaded.
```python
firebase.get("testtag", "DATAvariable"[, bg=False])
print(DATAvariable) #None if no data found

firebase.getfile("testtag", "DATAfile.txt"[, bg=False])
myfile=open("DATAfile.txt")
print(myfile.read())
myfile.close()
```
### Upload data to the database (runs in the background)
```python
firebase.put("testtag", "testtdata")
firebase.put("testtag", {"tag1": "data1", "tag2": "data2"})

firebase.addto("testtag", "data1")
```
### Delete data from the database (runs in the background)
```python
firebase.delete("testag")
```
## Functionality
A thread is created for each command* entered. There is a kind of waiting loop for these commands, so **only one connection can be executed at a time**. So if you make 10 get commands, these are processed **one after the other**, which means that the _last command is executed much later_.
>*with the exception of get and getfile with bg = False

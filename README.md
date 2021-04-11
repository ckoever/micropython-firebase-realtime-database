# micropython-firebase-realtime-database
**Firebase implementation** based on [REST API](https://firebase.google.com/docs/reference/rest/database) optimized for the [ESP32 version of Micropython](https://github.com/micropython/micropython-esp32) based on [firebase-micropython-esp32](https://github.com/vishal-android-freak/firebase-micropython-esp32) from vishal-android-freak. It shouldn't be a problem to run it on other Micropython platforms. **A board with PSRAM is recommended.**


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
### Connect to Wifi
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
### Set the URL of the database
```python
import ufirebase as firebase
firebase.setURL("https://[PROJECT_ID].firebaseio.com/")
```
## Functions
### setURL
```python
firebase.setURL(URL)
```
Set the current Firebase URL.
### get
```python
firebase.get(PATH, DUMP, bg=False, id=0)
```
Takes the given storage location `PATH`, gets the data from there and stores it as `DUMP`. The data can later be read out by `firebase.[DUMP]`.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Recommended if you know what you are doing, only makes sense if the command is running in the background.
    - Example: 
    ```python
    firebase.get("testtag1", "VAR1", bg=True, id=0)
    firebase.get("testtag2", "VAR2", bg=True, id=1) #runs at the same time
    time.sleep(10) #Do some other things, or wait a bit, or use bg=False with id=0
    print("1:"+firebase.VAR1+" 2:"+firebase.VAR2)
    ```
### getfile
```python
firebase.get(PATH, FILE, bg=False, id=0)
```
Takes the given storage location `PATH`, gets the data from there and stores it as file at the location `FILE`. Recommeded to download larger amounts of data to avoid ram overflow.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Recommended if you know what you are doing, only makes sense if the command is running in the background.
    - Example: 
    ```python
    firebase.getfile("testlarge1", "FILE1.txt", id=0)
    firebase.getfile("testlarge2", "FILE2.txt", id=1) #runs at the same time
    time.sleep(20) #Do some other things, or wait a bit, or use bg=False with id=0
    LOCAL_FILE1=open("FILE1.txt")
    LOCAL_FILE2=open("FILE2.txt")
    print("1:"+LOCAL_FILE1.read()+" 2:"+LOCAL_FILE2.read())
    LOCAL_FILE1.close()
    LOCAL_FILE2.close()
    del LOCAL_FILE1
    del LOCAL_FILE2
    ```
### put
```python
firebase.put(PATH, DATA, bg=True, id=0)
```
Takes the given storage location `PATH` and uploads the given text `DATA` there.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Recommended if you know what you are doing, only makes sense if the command is running in the background.
    - Example: 
    ```python
    firebase.put("testtag1", "1", id=0)
    firebase.put("testtag2", "2", id=1) #runs at the same time
    ```
### patch
```python
firebase.patch(PATH, DATA, bg=True, id=0)
```
Takes the given storage location `PATH` and uploads the given text `DATA` there.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Recommended if you know what you are doing, only makes sense if the command is running in the background.
    - Example: 
    ```python
    firebase.patch("testtag1", "1", id=0)
    firebase.patch("testtag2", "2", id=1) #runs at the same time
    ```
### addto
```python
firebase.addto(PATH, DATA, bg=True, id=0)
```
Takes the given storage location `PATH` and uploads the given text `DATA` there.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Recommended if you know what you are doing, only makes sense if the command is running in the background.
    - Example: 
    ```python
    firebase.addto("testtag1", "1", id=0)
    firebase.addto("testtag2", "2", id=1) #runs at the same time
    ```
### delete
```python
firebase.addto(PATH, bg=True, id=0)
```
Takes the given storage location `PATH` deletes the data there.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Recommended if you know what you are doing, only makes sense if the command is running in the background.
    - Example: 
    ```python
    firebase.delete("testtag1", id=0)
    firebase.delete("testtag1", id=0) #runs at the same time
    ```
## Constants
### FIREBASE_GLOBAL_VAR.GLOBAL_URL
```python
firebase.FIREBASE_GLOBAL_VAR.GLOBAL_URL
```
Returns the current URL as string, do not change directly insted use `firebase.setURL(URL)`
### FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO
```python
firebase.FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO
```
Additional information needed by usocket as list.
### FIREBASE_GLOBAL_VAR.SLIST
```python
firebase.FIREBASE_GLOBAL_VAR.SLIST
```
Dict of sokets for background process.
## Examples
### Get data from the database
```python
firebase.get("testtag", "DATAvariable"[, bg=False, id=0])
print(firebase.DATAvariable) #None if no data found

firebase.getfile("testtag", "DATAfile.txt"[, bg=False, id=0])
myfile=open("DATAfile.txt")
print(myfile.read())
myfile.close()
```
### Upload data to the database
```python
firebase.put("testtag", "testtdata"[, bg=True, id=0])
firebase.put("testtag", {"tag1": "data1", "tag2": "data2"}"[, bg=True, id=0])

firebase.addto("testtag", "data1"[, bg=True, id=0])
```
### Delete data from the database
```python
firebase.delete("testag"[, bg=True, id=0])
```
## Functionality
A thread is created for each command* entered. There is a kind of waiting loop for these commands, so **only one connection can be executed at a time per id**. So if you make 4 get commands, these are processed **one after the other**, which means that the _last command is executed much later_ or if you make 4 get commands, half id=0, half id=1, these are processed **2*one after the other**, which means that the _last command is executed a bit earlier_ .
>*exception if bg = False

<meta name="google-site-verification" content="FTs6IR_lrQ_1XqCMMtQI_AUInQqW3qCF3H7TV1QgqUY" />

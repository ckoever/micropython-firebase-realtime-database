# [micropython-firebase-realtime-database](https://github.com/ckoever/micropython-firebase-realtime-database)
**Firebase implementation** based on [REST API](https://firebase.google.com/docs/reference/rest/database) optimized for the [ESP32 version of Micropython](https://github.com/micropython/micropython-esp32) based on [firebase-micropython-esp32](https://github.com/vishal-android-freak/firebase-micropython-esp32) from vishal-android-freak. It shouldn't be a problem to run it on other Micropython platforms. **A board with SPIRAM is recommended.**
[https://img.shields.io/badge/%20status-%F0%9F%9F%A1Further%20development%20on%20request-yellow]


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

### Preparations [YouTube Tutorial](https://www.youtube.com/watch?v=T35U8zwTe40)
1. Create a [Firebase Realtime Database](https://firebase.google.com/products/realtime-database). (Console>Add Project>Realtime Database>Create Database)

In the end it should look something like this:

![image](https://user-images.githubusercontent.com/77546092/114287154-f6071b00-9a64-11eb-9214-de75753a71c3.png)

2. Set rules to **public** * *(from now the data can be read and changed by everyone ⚠️)* *
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
### get --------------------------------------
```python
firebase.get(PATH, DUMP, bg=False, id=0, cb=None, limit=False)
```
Takes the given storage location `PATH`, gets the data from there and stores it as `DUMP`. The data can later be read out by `firebase.[DUMP]`.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Make sure the command runs in the background.
  - Set an callback function after getting the `DATA`. 
    - Example: 
    ```python
    def hereweare(name, id, varname):
      print("\nname: "+str(name)+", id: "+str(id)+", value: "+str(eval("firebase."+varname)))
    firebase.get("testtag1", "VAR1", bg=True, id=0, cb=(hereweare, ("testtag1", "0", "VAR1")))
    firebase.get("testtag2", "VAR2", bg=True, id=1, cb=(hereweare, ("testtag2", "1", "VAR2"))) #runs at the same time
    ```
  - Limit the depth of the data to 1 with `limit` ⚠️ ONLY USE True/False (not 1/0). 
    - Example:

    ![image](https://user-images.githubusercontent.com/77546092/115153400-f6f80800-a075-11eb-8c50-5814a96309df.png)
    ```python
    firebase.get("a", "VAR1")
    print(firebase.VAR1) 
    #returns {'testlarge2': 'KJIHGFEDCBA', 'lol': 'ok', 'a': {'-MY_ntFnAhiTYygcraC6': [2, 2], '-MY_novcmzHOyexwij8B': '2', '-MY_nlKoV7jcYbTJMpzT': '2'}, 'testlarge1': 'ABCDEFGHIJK', 'testtag1': 1, 'testtag2': 2}
    firebase.get("a", "VAR2", limit=True)
    print(firebase.VAR2)
    #returns {'testlarge2': True, 'lol': True, 'testtag2': True, 'testlarge1': True, 'testtag1': True, 'a': True} 
    ```
### getfile --------------------------------------
```python
firebase.getfile(PATH, FILE, bg=False, id=0, cb=None, limit=False)
```
Takes the given storage location `PATH`, gets the data from there and stores it as file at the location `FILE`. Recommeded to download larger amounts of data to avoid ram overflow.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Make sure the command runs in the background.
  - Set an callback function after getting the `DATA`. 
    - Example: 
    ```python
    def herewefile(name, id, filename):
       LOCAL_FILE=open(str(filename))
       print("\nname: "+str(name)+", id: "+str(id)+", value: "+str(LOCAL_FILE.read()))
       LOCAL_FILE.close()
    firebase.getfile("testlarge1", "FILE1.txt", id=0, bg=1, cb=(herewefile, ("testlarge1", "0", "FILE1.txt")))
    firebase.getfile("testlarge2", "FILE2.txt", id=1, bg=1, cb=(herewefile, ("testlarge2", "1", "FILE2.txt"))) #runs at the same time
    ```
  - Limit the depth of the data to 1 with `limit` ⚠️ ONLY USE True/False (not 1/0). 
### put --------------------------------------
```python
firebase.put(PATH, DATA, bg=True, id=0, cb=None)
```
Takes the given storage location `PATH` and uploads the given value `DATA` there.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Make sure the command runs in the background. (Example at get)
  - Set an callback function after getting the `DATA`. 
    - Example: 
    ```python
    firebase.put("testtag1", "1", id=0)
    firebase.put("testtag2", "2", id=1) #runs at the same time
    ```
### patch --------------------------------------
```python
firebase.patch(PATH, DATATAG, bg=True, id=0, cb=None)
```
Takes the given storage location `PATH` and patches the given key `DATATAG` there, without touching any other tag in the Database.
  - Example:
  ```python
  firebase.put("teststruct", {"tag1": "val1", "tag2": "val2"})
  firebase.patch("teststruct", {"tag1": "new1"}) #only tag 1 will be changed
  ```
  ![image](https://user-images.githubusercontent.com/77546092/114471016-30e98a00-9bf0-11eb-90ec-baec7f10e03c.png)
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Make sure the command runs in the background. (Example at get)
  - Set an callback function after patching the `DATA`. 
### addto --------------------------------------
```python
firebase.addto(PATH, DATA, DUMP=None, bg=True, id=0, cb=None)
```
Takes the given storage location `PATH` and adds the given value `DATA` there, the randomly generated tag can be optionally stored in the DUMP variable.
  - Example:
  ```python
  firebase.addto("testsensor", 128)
  firebase.addto("testsensor", 124)
  firebase.addto("testsensor", 120, DUMP="tagname")
  print(firebase.tagname) #returns '-MY7GTy4pp2LSpQp5775' (example)
  ```
  ![image](https://user-images.githubusercontent.com/77546092/114472221-1fa17d00-9bf2-11eb-804d-21e0ac425a87.png)
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Make sure the command runs in the background. (Example at get)
  - Retuns the tag under which the data was saved.
  - Set an callback function after adding the `DATA`. 
### delete --------------------------------------
```python
firebase.delete(PATH, bg=True, id=0, cb=None)
```
Takes the given storage location `PATH` deletes the data there.
  - Optional run in the background with the keyword `bg`.
  - Set socket id with the keyword `id`. This makes it possible to establish multiple connections to the server instead of just one. Make sure the command runs in the background. (Example at get)
  - Set an callback function after deleting the `DATA`. 
## Constants
### FIREBASE_GLOBAL_VAR.GLOBAL_URL
```python
firebase.FIREBASE_GLOBAL_VAR.GLOBAL_URL
```
Returns the current URL as string, do not change directly insted use `firebase.setURL(URL)`
### FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO --------------------------------------
```python
firebase.FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO
```
Additional information needed by usocket as list.
### FIREBASE_GLOBAL_VAR.SLIST --------------------------------------
```python
firebase.FIREBASE_GLOBAL_VAR.SLIST
```
Dict of sokets for background process.
## Simple examples
### Get data from the database
```python
firebase.get("testtag", "DATAvariable")
print(firebase.DATAvariable) #None if no data found

firebase.getfile("testtag", "DATAfile.txt")
myfile=open("DATAfile.txt")
print(myfile.read())
myfile.close()
```
### Upload data to the database --------------------------------------
```python
firebase.put("testtag", "testtdata")
firebase.put("testtag", {"tag1": "data1", "tag2": "data2"})

firebase.addto("testtag", "data1")
```
### Delete data from the database --------------------------------------
```python
firebase.delete("testtag")
```
## Functionality
A thread is created for each command* entered. There is a kind of waiting loop for these commands, so **only one connection can be executed at a time per id**. 

If you make 4 get commands, id=0, these are processed **one after the other**, which means that the last command is executed much later. 

If you make 4 get commands, half id=0, half id=1, these are processed **2*one after the other**, which means that the last command is executed a bit earlier.
>*exception if bg = False

<meta name="google-site-verification" content="FTs6IR_lrQ_1XqCMMtQI_AUInQqW3qCF3H7TV1QgqUY" />

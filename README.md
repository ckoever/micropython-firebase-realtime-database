# [micropython-firebase-realtime-database](https://github.com/ckoever/micropython-firebase-realtime-database)
**Firebase implementation** based on [REST API](https://firebase.google.com/docs/reference/rest/database) optimized for the [ESP32 version of Micropython](https://github.com/micropython/micropython-esp32) based on [firebase-micropython-esp32](https://github.com/vishal-android-freak/firebase-micropython-esp32) from vishal-android-freak. It shouldn't be a problem to run it on other Micropython platforms. **A board with SPIRAM is recommended.**

![status](https://img.shields.io/badge/%20status-%F0%9F%9F%A1%20Further%20development%20on%20request-yellow?style=for-the-badge)

### 🔴IMPORTANT❗
The beta branch adds support for firebase authentication. See [ufirebase.py class auth](https://github.com/ckoever/micropython-firebase-realtime-database/blob/beta/ufirebase.py#L85)
This is necessary when only specific "users" should be able to read and/or write to or from a specific realtime database path. See [Understand Firebase Realtime Database Security Rules](https://firebase.google.com/docs/database/security?hl=en#section-authentication). If you make your realtime database available for public, you should (i highly recommend it)  use authentication, so that the realtime database url alone, isn't the only GRAND KEY to access all information stored in the database. Use authentication instead.

The reason why i the beta branch with auth is not pushed to main is that documentation is missing/wrong so you need to take a look at the source code yourself to use the functions. 
examples:

main branch --> beta branch
```
get(...) --> rtdb.get(...)
seturl(...) --> rtdb.conf.seturl(...)
[...]
```

new functions in beta branch
```
rtdb.conf.setsecret(...)
auth.selauth(...)
auth.desauth(...)
auth.sign_in_ep(email, passwd, ...)
auth.send_password_reset_email(...)
auth.verify_password_reset_code(...)
[... and more]
```

as most of the new code in beta branch is created according to [this documentation](https://cloud.google.com/identity-platform/docs/reference/rest/v1/accounts), you can orient yourself on that.
Please also note that authentication is not completely implemented, so most features are missing.

ALSO...
copy the [ufirebase.py](https://github.com/ckoever/micropython-firebase-realtime-database/blob/beta/ufirebase.py) file to your board instead of the automated [firebase_setup.py](https://github.com/ckoever/micropython-firebase-realtime-database/blob/beta/firebase_setup.py) setup script.

### Commands that are implemented
```
Basic Commands
- get (equal GET)
- getfile (equal GET)*
- put (equal PUT)
- patch (equal PATCH)
- addto (equal POST)
- delete (equal DELETE)

General Authentication
- add/(de)select/remove
```
> *getfile writes the data to a file to avoid RAM overflow

### Required modules
```
ujson, usocket, ussl, _thread, time
```
**Authentication: FUNCTIONS RENAMED/WRONG**

1. Note the Web API Key (from https://console.firebase.google.com/project/YOUR_PROJECT_NAME_HERE/settings/general)
![image](https://user-images.githubusercontent.com/77546092/144001024-b594c6f9-4689-424e-813e-405d0aac5eb9.png)

2. Add user
![image](https://user-images.githubusercontent.com/8059266/143820492-d7411b2c-e153-4bcd-83aa-917d0cf2ad89.png)

3. Edit rules
https://firebase.google.com/docs/reference/security/database#variables

Example:
```java
{
  "rules": {
    ".read": "auth.uid == 'Pho[...]'",
    ".write": "auth.uid == 'Pho[...]'"
  }
}
```

4. Set Web API key from Step 1
```python
firebase.setAPIKEY(FIREBASE_PROJECT_API_KEY)
```

5. Add authentication/user
```python
firebase.addAUTH(EMAIL_ADDRESS, PASSWORD)
```

6. Select authentication/user to use
```python
firebase.selAUTH(EMAIL_ADDRESS, PASSWORD)
```

Full Sample
```python
FIREBASE_PROJECT_API_KEY = "abcd"
EMAIL_ADDRESS = "test@test.com"
PASSWORD = "TEST"
firebase.setAPIKEY(FIREBASE_PROJECT_API_KEY)
firebase.addAUTH(EMAIL_ADDRESS, PASSWORD)
firebase.selAUTH(EMAIL_ADDRESS, PASSWORD)
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
## Functionality
A thread is created for each command* entered. There is a kind of waiting loop for these commands, so **only one connection can be executed at a time per id**. 

If you make 4 get commands, id=0, these are processed **one after the other**, which means that the last command is executed much later. 

If you make 4 get commands, half id=0, half id=1, these are processed **2*one after the other**, which means that the last command is executed a bit earlier.
>*exception if bg = False

<meta name="google-site-verification" content="FTs6IR_lrQ_1XqCMMtQI_AUInQqW3qCF3H7TV1QgqUY" />

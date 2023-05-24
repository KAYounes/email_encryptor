# README
---

# Disclaimer
This app needs two email accounts and and their passwords as input to function properly. The app does not intentionally leak this data. Nor does is use it outside the scope of this project.

Use new accounts that you do not care about their scrutiy to avoid any mishaps.


# How to Run
There are three main part
1. RPC Server
2. Email Sender App
3. Inbox Reader App

First to use either apps the server should be running. To run the server run the following script.
```
>python rpc_server.py
```

If it is the first run then a ```data/``` directory was created with subfolders as well. Open the ```data/storage_files/email_1.dat``` and write the sender email on the first line and the password on the sendon line.
The same should be done for the recipient email at ```data/storage_files/email_2.dat```.

Now you while the server is running and the credentials of the sender and recipient are correct, the email sender app ```email_app.py``` and ```email_app_adv.py``` can be ran.

# Email Constrains
The email sender script is configures to work with the domain ```@eng.asu.edu.eg``` and using another domain will proberly need some configuration in the ```email_sender.py``` script.

The inbox reader script is configured to work with the gmail domain. And using another domain will require configuration. To use a gmail account the password of the gmail account is not the deafult password used for login. Since Google has disabled less-scure apps features, a password must be generated using the app password method provided by Google. Simply allow 2-Step Verification from the account, and after that you can add an app password. Use the genrated app password as the recipient password.
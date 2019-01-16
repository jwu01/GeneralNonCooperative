# GeneralNonCooperative --> Project02-The End
* Jeffrey Wu (Project b0$$)
* Damian Wasilewicz (DB management)
* Sajed Nahian (Back-end communication w Front)
* Thomas Lee (Beautification)

# General Coding
Our project is an interactive javascript coding academy. Users will be given exercises to complete. As more tasks are completed, others are unlocked and points are gained. Earning points will rise your ranking on our leaderboard, and using ipAPI the leaderboard will also represent the nationalities of the coders. Admin users have the ability to create problems.

## a video demo
[link here]
  
## How do you run our project?

### Create and run your own virtual environment
```
$ python3 -m venv General
$ . General/bin/activate
```
### Clone our repository
#### Using HTML:
```
$ git clone https://github.com/jwu01/GeneralNonCooperative.git
```
#### Using SSH:
```
$ git clone git@github.com:jwu01/GeneralNonCooperative.git
```
### Install requirements.txt (which installs passlib)
```
$ git install -r GeneralNonCooperative/requirements.txt
```
### CD into project directory and run Flask app
```
$ cd GeneralNonCooperative
$ python run app.py
```
### Open app in browser
http://127.0.0.1:5000/



## Dependencies
### Why Passlib?
Passlib allows us to encrypt passwords through hashing with the ability to later decrypt them. This was done to ensure the security of authentication. Once a user logs in, the password is decrypted. It is installed in the requirements.txt file.
Documentation: https://passlib.readthedocs.io/en/stable/

## API Keys
Avatar: No API Key
Documentation: http://avatars.adorable.io/#demo

ipAPI: No API Key
Documentation:https://ipapi.co/api/#introduction

Coutry Flags API: No API Key
Documentation: https://www.countryflags.io

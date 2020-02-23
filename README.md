# Online Sports Turf Playground Booking System
 An application developed using Python Flask. A simple framework for building complex web applications.
## Project Setup
```
$ pip install Flask
```
## Hello World Example
Create a file called hello.py
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
return "Hello World!"

if __name__ == "__main__":
app.run(host='0.0.0.0', port=4000)
```
Finally run the web app using this command:
```
$ python hello.py
```
## Modules 
 
The system comprises of 3 major modules with their sub-modules as follows:
```
1. Admin 
2. Manager 
3. Users Login 
```

## Functionality of each module 

### 1. Admin: 

- **Add Manager**: Admin can add turf location and manager of the respective turf
location.
- **Add Price List** : Admin can add price for the respective turfs.
- **Manage Turf** : Admin can manage turf by allocating turf 
- **View Booking** : Admin can view booking done and the user details.

### 2. Manager:

- **Login**: Manager can login with the credentials provided by user.
- **Check Rates**: Manager can check rates for the respective location turf.
- **View Request**: Manager can view request for turf bookings.
- **Confirm Booking**: Manager can confirm the booking of the turf
- **Bill Generation**: Manager can generate bills as per the rates.
- **Bookings History**: Manager can check previous booking history

### 3. Users Login:

- **Check Turf**: User can check for turf of nearby location and prices.
- **Check Availability**: User can see the availability of the respective turf which is selected by him.
- **Book Turf**: User can provide date, time and other personal details and he can also do payment.
- **Booking History**: User can see his previous booking history.

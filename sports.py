from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

user = {}
admin = {}
manager = {}

user = {
'user1' : 'password',
'user2' : 'password',
'user3' : 'password'
}
admin['admin'] = 'password'

manager = {
'manager1' : 'password',
'manager2' : 'password',
'manager3' : 'password'
}

app = Flask(__name__)

global active
global email
global visit
global location
global am   ##allocation of manager to a turf  manager:turf
global au,avail_turf   ##allocation of user to a turf  user:turf
global price


location=['Chennai','Bangalore','Coimbatore']
price={'Chennai':500}
am = {'manager1':'Chennai'}
au = {'user1':'Chennai'}
avail_turf = []

active = None
visit = 0       #for calculating the number of visits for a web page.

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    global active
    global email
    if request.form['choice'] == 'user':
        if request.form['username'] in user and user[request.form['username']] == request.form['password']:
            active = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return render_template('home_user.html',email=active)

    elif request.form['choice'] == 'admin':
        if request.form['username'] in admin and admin[request.form['username']] == request.form['password']:
            active = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return render_template('home_admin.html',email=active)

    elif request.form['choice'] == 'manager':
        if request.form['username'] in manager and manager[request.form['username']] == request.form['password']:
            active = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return render_template('home_manager.html',email=active)

@app.route('/home_admin', methods=["POST"])
def home_admin():
    global visit
    visit = visit + 1

    global location
    if request.form['submit_button'] == 'Add turf location':
        return render_template('add_location.html',l = ",".join(location))

    global am
    l = list(am.items())
    if request.form['submit_button'] == 'Allocate a manager':
        return render_template('allocate_manager.html',a = l)

    global price
    if request.form['submit_button'] == 'Add price list':
        return render_template('add_price.html',p = list(price.items()))

    if request.form['submit_button'] == 'View booking':         ###WORK - NOT YET FINISHED
        return render_template('view_booking.html')

    if request.form['submit_button'] == 'View visits':
        return render_template('visitors.html', v=visit)
    if request.form['submit_button'] == 'Log out':
        return logout()
    if request.form['submit_button'] == 'Contact':
        return render_template('contact.html')

@app.route('/add_location',methods=["POST"])
def add_location():
    global location
    if request.form['submit_button'] == 'Add':
        location.append(request.form['location'])
        return "After addition, the available locations are: " + ",".join(location) #list passing

@app.route('/allocate_manager',methods=["POST"])
def allocate_manager():
    global am
    if request.form['submit_button'] == 'Add':
        am[request.form['man']] = request.form['loc']
        return "After addition, the available locations are: " + str(list(am.items())) #dict passing

@app.route('/add_price',methods=["POST"])
def add_price():
    global price
    if request.form['submit_button'] == 'Add':
        price[request.form['loc']] = request.form['price']
        return "After addition, the available locations are: " + str(list(price.items()))

@app.route('/home_manager', methods=["POST"])
def home_manager():
    global visit
    visit = visit + 1

    if request.form['submit_button'] == 'View visits':
        return render_template('visitors.html', v=visit)
    if request.form['submit_button'] == 'Log out':
        return logout()
    if request.form['submit_button'] == 'Contact':
        return render_template('contact.html')

@app.route('/home_user', methods=["POST"])
def home_user():
    global visit
    visit = visit + 1

    global price
    if request.form['submit_button'] == 'Check turf':
        return render_template('check_turf.html', p=str(list(price.items())))

    global au,avail_turf
    for ch in location:  ## checks from locations & not in allocated!!
        if ch not in au.values():
            avail_turf.append(ch)
    if request.form['submit_button'] == 'Check availability':
        return render_template('check_availability.html',u=",".join(avail_turf))

    if request.form['submit_button'] == 'Book a turf':
        return render_template('book_turf.html')

    if request.form['submit_button'] == 'My history':
        return render_template('my_history.html')

    if request.form['submit_button'] == 'View visits':
        return render_template('visitors.html', v=visit)
    if request.form['submit_button'] == 'Log out':
        return logout()
    if request.form['submit_button'] == 'Contact':
        return render_template('contact.html')

@app.route('/book_turf',methods=["POST"])
def book_turf():
    global au,active
    if request.form['submit_button'] == 'Book':
        temp = request.form['loc']
        if active in au.keys():
            var = au[active]
            return "Only 1 booking at a time !! Already booked- "+ active +": "+var
        if temp not in au.values() and temp in location:
            au[active] = temp
            return "Booked: "+ active + ":" + temp
        else:
            return temp + " location not available !! Sorry "

@app.route('/contactexp', methods=["GET"])
def contactexp():
    return render_template('contactexp.html')

@app.route('/error')
def err():
    flash("Wrong password entered")
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    global active
    active = None
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=4000)
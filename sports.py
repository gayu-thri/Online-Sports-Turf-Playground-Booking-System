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
global location,viewreqs,booking_hist,viewbook
global am   ##allocation of manager to a turf  manager:turf
global au,avail_turf   ##allocation of user to a turf  user:turf
global price,reqs  ##request - user:turf

viewreqs = {}
viewbook = {}
location=['Chennai','Bangalore','Coimbatore']
price={'Chennai':500}
am = {'manager1':'Chennai'}
au = {'user1':'Chennai'}
avail_turf = []
reqs = {'user2':'Bangalore'}
booking_hist = []
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

    global manager
    if request.form['submit_button'] == 'Provide credentials & Add a manager':
        return render_template('add_manager.html',mavail = ",".join(manager.keys()))

    global am
    l = list(am.items())
    if request.form['submit_button'] == 'Allocate a manager':
        return render_template('allocate_manager.html',a = l)

    global price
    if request.form['submit_button'] == 'Add price list':
        return render_template('add_price.html',p = list(price.items()))

    global au,reqs
    if request.form['submit_button'] == 'View Booking':
        return render_template('view_booking.html',b= list(au.items()),r=list(reqs.items()))

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

@app.route('/add_manager',methods=["POST"])
def add_manager():
    global manager
    if request.form['submit_button'] == 'Add the manager':
        manager[request.form['muname']] = request.form['mpass']
        return "Successfully added manager with credentials: " + "Username- "+request.form['muname'] + "Password-" + request.form['mpass']

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

    if active in au.keys():
        rl = au[active]
    else:
        rl = None
    if active in reqs.keys():
        re = reqs[active]
    else:
        re = None
    if request.form['submit_button'] == 'My history':
        return render_template('my_history.html',out=rl,req=re)   ##out- booked , req-requested

    if request.form['submit_button'] == 'View visits':
        return render_template('visitors.html', v=visit)
    if request.form['submit_button'] == 'Log out':
        return logout()
    if request.form['submit_button'] == 'Contact':
        return render_template('contact.html')

@app.route('/book_turf',methods=["POST"])
def book_turf():
    global au,active,reqs
    if request.form['submit_button'] == 'Book':
        temp = request.form['loc']
        if active in au.keys():
            var = au[active]
            return "Only 1 booking at a time !! Already booked- "+ active +": "+var
        if temp not in au.values() and temp in location:
            reqs[active] = temp
            return "Requested for: "+ active + ":" + temp
        else:
            return temp + " location not available !! Sorry "


@app.route('/home_manager', methods=["POST"])
def home_manager():
    global visit
    visit = visit + 1

    if request.form['submit_button'] == 'Check rates':
        return render_template('check_rates.html')

    global reqs, am, viewreqs

    if request.form['submit_button'] == 'View Request':
        if active not in am.keys():
            return "You don't have a turf location alloted to you!! Hence no requests will be visible to you.. Contact admin"
        else:
            assigned_loc = am[active]
            for user,loc in reqs.items():
                if loc == assigned_loc:
                    viewreqs[user] = assigned_loc
            return render_template('view_request.html', v = list(viewreqs.items()))

    if request.form['submit_button'] == 'Confirm Booking':
        if active not in am.keys():
            return "You don't have a turf location alloted to you!! Hence no requests will be visible to you.. Contact admin"
        else:
            assigned_loc = am[active]
            for user,loc in reqs.items():
                if loc == assigned_loc:
                    viewreqs[user] = assigned_loc
            return render_template('confirm_booking.html',general=list(reqs.items()),mine=list(viewreqs.items()))

    global price
    if request.form['submit_button'] == 'Bill Generation':
        return render_template('bill_generation.html')

    global viewbook
    if request.form['submit_button'] == 'Booking History':  ###WORK - NOT YET FINISHED
        assigned_loc = am[active]
        for user,loc in au.items():
            if loc == assigned_loc:
                viewbook[user] = assigned_loc
        return render_template('booking_history.html',l=assigned_loc,u = list(viewbook.keys()))

    if request.form['submit_button'] == 'View visits':
        return render_template('visitors.html', v=visit)
    if request.form['submit_button'] == 'Log out':
        return logout()
    if request.form['submit_button'] == 'Contact':
        return render_template('contact.html')

@app.route('/generate_bill',methods=["POST"])
def generate_bill():
    usr = request.form['usr']
    if request.form['submit_button'] == 'Generate':
        if usr not in au.keys():
            return "The entered user ("+usr+") has no booking confirmed."
        else:
            lo = au[usr]
            pr = price[lo]
            return render_template('generate_bill.html',u = usr,l = lo, p = pr)


@app.route('/confirm',methods=["POST"])
def confirm():
    global au
    if request.form['submit_button'] == 'Confirm':
        usr = request.form['usr']
        loc = request.form['loc']
        if loc in au.values():
            return "Sorry!! Location "+ loc + " is already booked."
        else:
            au[usr] = loc
            return "Successfully booked "+ loc + " for the user: "+usr

@app.route('/rate', methods=["POST"])
def rate():
    global price
    if request.form['loc'] in price.keys():
        var = price[request.form['loc']]
        return "The price for the requested location "+ request.form['loc'] + " is :"+ str(var)
    else:
        return "Sorry!! The requested location is not available"

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
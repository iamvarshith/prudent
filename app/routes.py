from app.models import User
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session
from app import app, db, login_manager

from flask_login import login_user, current_user, logout_user, login_required

from app.paytm import checksum
import random
import requests
import json
import hashlib
from app import final_url


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(400)
def page_error(e):
    return render_template('400.html'), 400


@app.route('/')
@app.route('/home')
def home():
    return render_template('home_index.html')


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('test'))
    return render_template('login.html')


@app.route('/getotp', methods=['POST'])
def getotp(otp_entered=None):
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['mobile']
        otp = random.randint(100000, 999999)
        session['otp'] = otp
        print(otp)
        sentotp = str(otp)
        print(email)

        try:
            r = requests.post("https://api.mailgun.net/v3/wahhealthcare.com/messages",

                              auth=("api", "key-179896d154b2bdb3c6b6d0201268f295"),
                              data={"from": "Prudent <noreply@wahhealthcare.tech>",
                                    "to": [email],
                                    "subject": "OTP ",
                                    "template": "otp",

                                    "h:X-Mailgun-Variables": json.dumps({"test": sentotp})},
                              timeout=1.5
                              )

            if r.status_code == 200:
                return '1'

        except requests.Timeout:
            return '0'
        except requests.ConnectionError:
            return '0'

    return '0'

@app.route('/resendotp', methods=['POST'])
def resendotp(otp_entered=None):
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['mobile']

        otp = session['otp']
        print(otp)
        sendotp = str(otp)
        print(email)

        try:
            r = requests.post("https://api.mailgun.net/v3/wahhealthcare.com/messages",

                              auth=("api", "key-179896d154b2bdb3c6b6d0201268f295"),
                              data={"from": "Prudent <noreply@wahhealthcare.tech>",
                                    "to": [email],
                                    "subject": "OTP ",
                                    "template": "otp",

                                    "h:X-Mailgun-Variables": json.dumps({"test": sendotp})},
                              timeout=1.5
                              )

            if r.status_code == 200:
                return '1'

        except requests.Timeout:
            return '0'
        except requests.ConnectionError:
            return '0'

    return '0'



@app.route('/confirmotp', methods=['POST'])
def confirmotp():
    print(session['otp'])

    email = request.form['email']
    phone = request.form['mobile']
    otp_entered = request.form['otp']
    if otp_entered == str(session['otp']):
        user = User.query.filter_by(email=email).first() or User.query.filter_by(
            phone=phone).first()
        if user:
            login_user(user)
            print('You are this here')

        else:
            user = User(name='null', email=email, phone=phone, payment_txn=0000)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            print('You no here before')

        return jsonify({
            "redirect": 'true',
            "redirect_url": url_for('test')
        })
    else:
        print('booo')
        return '1'


@app.route('/covid_test', methods=['POST', 'GET'])
@login_required
def test():
    if current_user.status == 'True':
        details_dict = {
            'name': current_user.name,
            'payment_txn': current_user.payment_txn,
            'status': current_user.status,
            'address': current_user.address,
            'landmark': current_user.landmark,
            'appointment': current_user.Time_date

        }
        return render_template('details.html')
    return render_template('new_templata.html')


@app.route('/contact/userform', methods=['POST'])
def userform():
    name = str(request.form['name'])
    address = str(request.form['address'])
    landmark = str(request.form['landmark'])
    pincode = str(request.form['pincode'])
    test_type = str(request.form['test_type'])
    no_ofpatients = str(request.form['no_ofpatients'])
    date = str(request.form['date'])

    if current_user.is_authenticated:
        current_user.name = name
        current_user.type_of_test = test_type
        current_user.Time_date = date

        current_user.address = address
        current_user.landmark = landmark + pincode
        current_user.no_of_patients = no_ofpatients

        db.session.commit()
        return jsonify({
            "redirect": 'true',
            "redirect_url": url_for('payu')
        })

    return jsonify({
        "redirect": 'true',
        "redirect_url": url_for('login')
    })


# @app.route('/test2', methods=['GET', 'POST'])
# def test2():
#     mobile = request.form['verifycode']
#     data = request.form['lat']
#     print(mobile)
#
#     if len(data) == 6:
#
#         return ('1')
#     else:
#         return ('1')


@app.route('/getlocation', methods=['POST'])
def getlocation():
    lat = request.form['lat']
    long = request.form['long']
    key = "AIzaSyCbGJok2aHxBQQPAnUkPaWCc7rUst-ZGKg"
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}".format(lat, long, key)
    i = requests.get(url)
    j = i.json()
    k = j['results'][1]['formatted_address']
    print(k)
    address = k.split(',')

    pincode = address[-2].split()[-1]
    if len(address) >= 5:
        landmark = address[2]
    else:
        landmark = address[1]
    line1 = address[0:1]

    print(pincode)
    print(landmark)
    return jsonify({'line1': line1,
                    'pincode': pincode,
                    'landmark': landmark
                    })


@app.route("/payment")
@login_required
def payment():
    test_type = current_user.type_of_test
    if test_type == 'RT-PCR':
        price = 1
    elif test_type == 'Anti-DARS(antibody)':
        price = 1
    else:
        price = 1

    txn_amount = int(current_user.no_of_patients) * price
    orderid = hashlib.md5(str((random.randint(100000, 999999) + current_user.phone)).encode()).hexdigest()
    param_dict = {

        'MID': 'GoMEMW82764175165100',
        'ORDER_ID': str(orderid),
        'TXN_AMOUNT': str(txn_amount),
        'CUST_ID': str(current_user.name),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'DEFAULT',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': final_url+'/paytm/handlerequest/',

    }
    param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, '8Z58wwmtFAOhM1vm')

    session['param_dict'] = param_dict
    return render_template('transfor.html', param=param_dict)


@app.route("/paytm/handlerequest/", methods=['POST', 'GET'])
def handeler_paytm():
    form = request.form
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            Checksum = form[i]

    if checksum.verify_checksum(response_dict, '8Z58wwmtFAOhM1vm', Checksum):

        if request.form['STATUS'] == 'TXN_SUCCESS':
            current_user.payment_txn = request.form['ORDERID']
            current_user.status = 'True'
            db.session.commit()
            return render_template('postpayment.html', status=request.form['STATUS'])

        else:
            return render_template('postpayment.html', status=request.form['STATUS'])
    return request.form['STATUS']


@app.route('/payu', methods=['POST', "GET"])
def payu():
    test_type = current_user.type_of_test
    if test_type == 'RT-PCR':
        price = 1
    elif test_type == 'Anti-DARS(antibody)':
        price = 1
    else:
        price = 1

    txn_amount = int(current_user.no_of_patients) * price
    txnid = hashlib.md5(str((random.randint(100000, 999999) + current_user.phone)).encode()).hexdigest()

    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')

    param_dict = {
        'key': 'ZOwH3J89',
        'txnid': txnid,
        'amount': str(txn_amount),
        'productinfo': str(test_type),
        'firstname': current_user.name,
        'email': current_user.email,
        'phone': current_user.phone,
        'surl': final_url + '/payu/success',
        'furl': final_url + '/payu/gg',
        'hash': '',
        'service_provider': 'payu_paisa'

    }
    for i in hashVarsSeq:
        try:
            hash_string += str(param_dict[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += 'LpoLYPU8dV'
    hashh = hashlib.sha512(hash_string.encode()).hexdigest().lower()
    param_dict['hash'] = hashh
    return render_template('payu.html', param=param_dict)


@app.route('/payu/success', methods=['POST', 'GET'])
def payu_success():
    status = request.form["status"]
    firstname = request.form["firstname"]
    amount = request.form["amount"]
    txnid = request.form["txnid"]
    posted_hash = request.form["hash"]
    key = request.form["key"]
    productinfo = request.form["productinfo"]
    email = request.form["email"]
    salt = "LpoLYPU8dV"
    retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode()).hexdigest().lower()
    if hashh == posted_hash:
        current_user.payment_txn = request.form['txnid']
        current_user.status = 'Success'
        db.session.commit()
        pay_status = 1

    return render_template('postpayment.html', status=pay_status, transaction_id=txnid)


@app.route('/payu/gg', methods=['POST', 'GET'])
def payu_fail():
    current_user.payment_txn = request.form['txnid']
    current_user.status = 'Fail'
    db.session.commit()
    pay_status = 0
    return render_template('postpayment.html', status=pay_status, transaction_id=request.form['txnid'])


@app.route('/equipment', methods=['POST', 'GET'])
def equipment():
    if request.method == "POST":
        print(request.form['data'])
    return render_template('equipments.html')


@app.route('/contact')
def contact():
    return redirect(url_for('home', _anchor='contact'))


@app.route('/about')
def about():
    return redirect(url_for('home', _anchor='about'))

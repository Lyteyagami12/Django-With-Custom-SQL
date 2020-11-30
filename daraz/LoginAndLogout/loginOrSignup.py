from django.shortcuts import render, redirect
import random
import os
import hashlib
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
# from .models import people
from django.db import connection
from django import template


def user_login(request):
    print("i m log in")
    try:
        usr = request.session['username']
        return redirect('/home/profile')
    except:
        print("not logged in please log in")
    if request.method == 'POST':
        # email = request.POST.get('email')
        # print(email)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        msg = 'Enjoy Buying!'
        try:
            cur = connection.cursor()
            sql = "select USERNAME, KEY ,SALT, CUSTOMER_NAME, EMAIL,CUSTOMER_PHOTO,ADRESS,ZONE,CONTACT, CUSTOMER_ID from PEOPLE where USERNAME = %s"
            print(sql)
            print(username)
            cur.execute(sql,[username])
            result = cur.fetchone()
            dic_res = []
            # dbemail = None
            dbkey = None
            dbuser = None
            dbsalt = None
            name = None
            dbuser = result[0]
            dbkey = result[1]
            dbsalt = result[2]
            name = result[3]
            email = result[4]
            address = result[6]
            zone = result[7]
            contact = result[8]
            pid = result[9]
            img = 'uploads/products/10000069-2_28-fresho-capsicum-green.jpg'
            try:
                img = result[5]
            except:
                print('failed to load image!')
            print(img)
            request.session['img_url']=img
            # for r in result:
            #     dbuser = r[0]
            #     dbkey = r[1]
            #     dbsalt = r[2]
            #     name = r[3]

            print("from database:...")
            print("dbuser:" + dbuser)
            if dbuser == username:
                print("username verified")
                new_key =hashlib.pbkdf2_hmac(
                    'sha256',  # The hash digest algorithm for HMAC
                    password.encode('utf-8'),
                    dbsalt ,
                    100000, # 100,000 iterations of SHA-256
                    # dklen = 128
                )

                if new_key == dbkey:
                    print("success")
                    print("sql:" + sql)
                    # request.session.__setitem__('username',dbuser)
                    request.session['username'] = dbuser
                    request.session['name'] = name
                    request.session['email'] = email
                    request.session['address'] = address
                    request.session['zone'] = zone
                    request.session['contact'] = contact
                    # request.session['id'] = dbuser

                    # request.session.__setitem__('username',username)
                    print("success2")
                    print("usernameform session: " + request.session['username'])
                    return redirect('/home')
                    # return redirect('/home')
                else:
                    print("failed man!")
                    print("dbkey: ")
                    print(dbkey)
                    print("userkey: ")
                    print(new_key)
                    return redirect('/home')

            else:
                print("wrong username!")
                return redirect('/login')
        except:
            messages = "something went wrong! try again"
            print(messages)
            return render(request,'login.html',{'msg':messages})
    else:
        return render(request, 'login.html', {})


def signup(request):
    print("i m in signup")
    usr=None
    try:
        usr = request.session['username']
        user_logout(request)
    except:
        print("sign up please!")
        print("couldn't make it")
    if request.method == 'POST':
        id = random.randrange(start=1700000, step=1)
        print("id:" + str(id))
        name = request.POST.get('name')
        print(name)
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        email = request.POST.get('mail')
        gender = request.POST.get('gender')
        dob = request.POST.get('birthdate')
        adress = request.POST.get('adress')
        contact = request.POST.get('contact')
        zone = request.POST.get('zone')
        method = request.POST.get('paymentmethod')
        salt = os.urandom(32)
        # password = 'password123'
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,  # 100,000 iterations of SHA-256
            # dklen=128  #128 byte key
        )

        sql = "INSERT INTO PEOPLE(CUSTOMER_ID, CUSTOMER_NAME, USERNAME,GENDER, BIRTHDATE, KEY, ADRESS, CONTACT, ZONE, EMAIL, PAYMENT_METHOD,SALT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = connection.cursor()
            cursor.execute(sql, [id, name, username, gender, dob, key, adress, contact, zone, email, method,salt])
            connection.commit()
            cursor.close()
            return redirect('/home/login')
        except:
            return render(request,'signup1.html',{'message':'Something went wrong!'})
    else:
        return render(request, 'signup1.html', {})



def user_logout(request):
    try:
            # del request.session['username']
            # del request.session['name']
            request.session.delete('username')
            request.session.delete('name')
            # request.session.clear()
            print("logged out")
            # user = request.session['username']
            return redirect('/home/signup')

            # if user is None:
            #     print("log out success")

    except:
        print("something is wrong")
        return redirect('/home')


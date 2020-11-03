from django.shortcuts import render, redirect
import random
import os
import hashlib
from django.shortcuts import render, redirect
from .models import people
from django.db import connection
from django.contrib import  messages
from  django.contrib.auth import authenticate

#
# def user_login(request):
#     print("i m in login")
#     if request.method == 'POST':
#         password1 = request.POST.get('password')
#         username1 = request.POST.get('username')
#         print(username1)
#         try:
#             user = authenticate(request, username=username1, password = password1)
#         except:
#             print("failed")
#         print("done checking")
#         if user is not None:
#             print("success")
#             # user_login(request)
#             return redirect('signup/')
#         else:
#             messages.error(request,'invalid user login credentials')
#             print("failed")
#             return render(request,'login.html',{})
#
#     else:
#         return render(request,'login.html',{})

def user_login(request):
    print("i m log in")
    if request.method == 'POST':
        # email = request.POST.get('email')
        # print(email)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        cur = connection.cursor()
        sql = "select USERNAME, KEY ,SALT from PEOPLE where USERNAME = %s"
        print(sql)
        print(username)
        cur.execute(sql,[username])
        result = cur.fetchall()
        dic_res = []
        # dbemail = None
        dbkey = None
        dbuser = None
        dbsalt = None

        for r in result:
            dbuser = r[0]
            dbkey = r[1]
            dbsalt = r[2]

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
                return redirect('home/')
            else:
                print("failed man!")
                print("dbkey: ")
                print(dbkey)
                print("userkey: ")
                print(new_key)
                return redirect('home/')
        else:
            print("wrong username bro!")
            return redirect('login/')
    else:
        return render(request, 'login.html', {})


def test(request):
    return render(request,'hello.html',{})


def lol(request):
    return render(request, 'lol.html', {})


def signup(request):
    print("i m in signup")
    if request.method == 'POST':
        id = random.randrange(start=1700000, step=1)
        print(id)
        print("/n")
        name = request.POST.get('name')
        print(name)
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        email = request.POST.get('mail')
        gender = request.POST.get('gender')
        dob = request.POST.get('birthdate')
        adress = request.POST.get('adress')
        contact = (request.POST.get('contact'))
        zone = request.POST.get('zone')
        method = request.POST.get('paymentmethod')
        salt = os.urandom(32)  # Remember this
        # password = 'password123'
        key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
            # dklen=128  # Get a 128 byte key
        )
        # hashedpass = salt + key
        sql = "INSERT INTO PEOPLE(CUSTOMER_ID, CUSTOMER_NAME, USERNAME,GENDER, BIRTHDATE, KEY, ADRESS, CONTACT, ZONE, EMAIL, PAYMENT_METHOD,SALT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor = connection.cursor()
        cursor.execute(sql, [id, name, username, gender, dob, key, adress, contact, zone, email, method,salt])
        connection.commit()
        cursor.close()
        return render(request, 'signup1.html', {'title': name})
    else:
        return render(request, 'signup1.html', {})


def products(request):
    cur = connection.cursor()
    cur.execute("SELECT * FROM PRODUCTS")
    result = cur.fetchall()
    cur.close()

    dic_res = []
    for r in result:
        product_id = r[0]
        product_name = r[1]
        cat = r[2]
        product_photo = r[3]
        status = r[4]
        birthdate = r[5]
        ##password
        price = r[6]
        discount = r[7]
        quantity = r[8];
        description = r[9]
        shop = r[10]
        cur = connection.cursor()
        cur.execute("select SHOP_NAME from SHOPS where SHOP_ID = 'LOL'")
        resultt = cur.fetchall()
        shopName = ''
        dic_res = []
        for r1 in resultt:
            shopName = r1[0]

        row = {'product_id': product_id, 'shop': shopName, 'name': product_name, 'photo': product_photo,
               'satus': status, 'desc': description}
        dic_res.append(row)
    return render(request, 'index.html', {'products': dic_res})


def home(request):
    return render(request, 'index.html', {})


def sell(request):
    return render(request, 'sell.html',{})
# Create your views here.


def list_jobs(request):
    # cursor = connection.cursor()
    # sql = "INSERT INTO PEOPLE VALUES(%s,%s,%s,%s)"
    # cursor.execute(sql,['NEW_JOB_1','Something New 1',5000,9000])
    # connection.commit()
    # cursor.close()

    # cursor = connection.cursor()
    # sql = "SELECT * FROM JOBS"
    # cursor.execute(sql)
    # result = cursor.fetchall()

    cursor = connection.cursor()
    sql = "SELECT * FROM PEOPLE"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []

    for r in result:
        customer_id = r[0]
        customer_name = r[1]
        username = r[2]
        customer_photo = r[3]
        gender = r[4]
        birthdate = r[5]
        ##password
        address = r[7]
        contact = r[8];
        zone = r[9]
        email = r[10]
        role = r[11]
        payment = r[12]
        row = {'customer_id': customer_id, 'photo': customer_photo, 'customer_name': customer_name, 'gender': gender,
               'contact': contact, 'zone': zone, 'email': email, 'payment': payment}
        dict_result.append(row)

    # return render(request,'list_jobs.html',{'jobs' : Job.objects.all()})
    print("showing...")
    return render(request, 'list_jobs.html', {'people': dict_result})


def selllogin(request):
    if request.method == 'POST':
        zone = request.POST.get('zone')
        password = request.POST.get('password')
        sql = "select SHOP_ID from SHOPS where SHOPPASSWORD = %s"
        cur = connection.cursor()
        cur.execute(sql,[password])
        result = cur.fetchall()
        cur.close()
        dbid =None
        for r in result:
            dbid = r[0]
        print(dbid)
        if dbid is not None:
            print("success")
            return redirect('/saleLogin')
        else:
            print("failed bitch!")
            return redirect('/saleLogin')
    else:
        return render(request,'sellingLogin.html',{})

def sellsignup(request):
    if request.method == 'POST':
        shopid = random.randrange(start=110,step=1)
        username = request.POST.get('username')
        zone = request.POST.get('zone')
        pwd = request.POST.get('password')
        shopname = request.POST.get('name')
        shopcat = request.POST.get('cat')
        contact = request.POST.get('contact')
        sql = "INSERT INTO SHOPS(SHOP_ID, SHOP_NAME, ZONE, CONTACT_INFO, SHOPPASSWORD, SHOP_CAT, SHOP_USERNAME) VALUES (%s,%s,%s,%s,%s,%s,%s);"
        cur = connection.cursor()
        cur.execute(sql,[shopid,shopname,zone,contact,pwd,shopcat,username])
        connection.commit()
        cur.close()
        return redirect('saleLogin/')
    else:
        return render(request, 'sellsignup.html',{})

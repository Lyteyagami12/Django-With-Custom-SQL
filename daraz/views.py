from django.shortcuts import render, redirect
import random
import os
import hashlib
from django.shortcuts import render, redirect
from .models import people
from django.db import connection


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
        contact = int(request.POST.get('contact'))
        zone = request.POST.get('zone')
        method = request.POST.get('paymentmethod')
        salt = os.urandom(32)  # Remember this
        # password = 'password123'
        key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128  # Get a 128 byte key
        )
        hashedpass = salt + key
        sql = "INSERT INTO PEOPLE(CUSTOMER_ID, CUSTOMER_NAME, USERNAME,GENDER, BIRTHDATE, PASSWORD, ADRESS, CONTACT, ZONE, EMAIL, PAYMENT_METHOD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor = connection.cursor()
        cursor.execute(sql, [id, name, username, gender, dob, hashedpass, adress, contact, zone, email, method])
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


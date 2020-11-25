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

def selllogin(request):
    try:
        name = request.session['shopname']
        return redirect('/saleproduct')
    except:
        print()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        sql = "select SHOP_NAME, SHOP_ID from SHOPS where SHOPPASSWORD = %s"
        cur = connection.cursor()
        cur.execute(sql,[password])
        result = cur.fetchall()
        shopname =None
        cur.close()
        dbid =None
        for r in result:
            dbid = r[1]
            shopname = r[0]
        print(dbid)
        if dbid is not None:
            print("success")
            request.session['shopusername'] = username
            request.session['shopname'] = shopname
            request.session['shopstatus'] = True
            # return render(request,'saleProducts.html',{})
            return redirect('/saleproduct')
        else:
            print("failed bitch!")
            return redirect('/saleLogin')
    else:
        return render(request,'sellingLogin.html',{})

def sellsignup(request):

    if request.method == 'POST':
        shopid = random.randrange(start=110, step=1)
        username = request.POST.get('username')
        zone = request.POST.get('zone')
        pwd = request.POST.get('password')
        shopname = request.POST.get('name')
        shopcat = request.POST.get('cat')
        contact = request.POST.get('contact')
        sql = "INSERT INTO SHOPS(SHOP_ID, SHOP_NAME, ZONE, CONTACT_INFO, SHOPPASSWORD, SHOP_CAT, SHOP_USERNAME) VALUES (%s,%s,%s,%s,%s,%s,%s);"
        cur = connection.cursor()
        cur.execute(sql, [shopid, shopname, zone, contact, pwd, shopcat, username])
        connection.commit()
        cur.close()
        return redirect('/home/sell/saleLogin')
        # return redirect('saleLogin/')
    else:
        return render(request, 'sellsignup.html',{})


def profile(request):
    username = None
    try:
        username = request.session['username']
    except:
        return redirect('/home/login')
    print("i m in profile")
    print(username)
    sql = "select CUSTOMER_NAME, EMAIL, CONTACT, ZONE from PEOPLE where USERNAME = %s"
    result = None
    try:
            cur = connection.cursor()
            cur.execute(sql,[username])
            result = cur.fetchall()
            cur.close()
    except:
        print("Log in please!")
        return redirect('/login')
    dict_result = None
    for r in result:
        name = r[0]
        email = r[1]
        contact = r[2]
        adress = r[3]
        dict_result = {'name':name,'email':email,'contact':contact,'adress':adress}

    return render(request,'Profile.html',dict_result)


def saleLogout(request):
    try:
            # shopuser = request.session['shopusername']
        # if shopuser is not None:
            request.session.delete('shopusername')
            request.session.delete('shopname')
            request.session.delete('shopstatus')

            # del request.session['shopusername']
            print("logged out")
            # user = request.session['username']
            return redirect('/home/sell/')
            # if user is None:
            #     print("log out success")
        # else:
            return redirect('/home/sell')
    except:
        print("something is wrong")
        return redirect('/home/sell')

def sale(request):
    shopn= None
    try:
        shopn = request.session['shopname']
        status = request.session['shopstatus']

    except:
        print("shop not found!")
        return redirect('/home/sell')
    if request.method == 'POST':
        print("i m in sales...")
        id = random.randrange(start=100, step=1)
        catid = random.randrange(start=200, step=1)
        name = request.POST.get('name')
        cat = request.POST.get('cat')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        specs = request.POST.get('specs')
        brand = request.POST.get('brand')
        discount = request.POST.get('discount')

        # photo = request.POST.get('filename')
        # print(photo)
        # name = str(id) + ".jpg"
        # img = request.FILES['propic',False]
        # img_extension = os.path.splitext(img.name)[1]
        # user_folder = 'static/images'
        # if not os.path.exists(user_folder):
        #     os.mkdir(user_folder)

        # img_save_path = user_folder + 'propic' + str(id) + img_extension
        # img_save_path = user_folder + 'pro_pic'+img_extension
        # img_url = '/static/images/' + 'propic' + str(id) + img_extension
        # request.session['pro_img_url'] = img_url
        # with open(img_save_path, 'wb') as f:
        #     for chunk in img.chunks():
        #         f.write(chunk)

        sql = "UPDATE PEOPLE SET USERNAME = %s , EMAIL = %s, ADRESS = %s , CONTACT= %s,CUSTOMER_PHOTO= %s WHERE CUSTOMER_ID = %s"
        # cursor.execute(sql, [username, email, Address, contact, img_url, dbid])

        cur = connection.cursor()
        usrname = request.session['shopusername']
        print("shopusername: "+ usrname)
        cur.execute("SELECT SHOP_NAME, SHOP_ID FROM SHOPS where SHOP_USERNAME = %s",[usrname])
        res = cur.fetchall()
        shopid = None
        shop =  None
        for r in res:
            shop = r[0]
            shopid = r[1]

        # shopname = shopname[0]

        sqlforshopid = "SELECT SHOP_ID FROM SHOPS WHERE SHOP_NAME = %s"
        try:
            # cur.execute(sqlforshopid, [shopname])

            # res = cur.fetchall()
            # shopid= None
            # for r in res:
            #     shopid = r[0]

            print("db_shop_id: " + str(shopid))
            sql = "INSERT INTO CATAGORIES(CAT_ID, CAT_NAME, QUANTITY) VALUES (%s,%s,%s)"

            sql1 = "INSERT INTO PRODUCTS(PRODUCT_ID,BRAND, PRODUCT_NAME, PRODUCT_PHOTO, DISCOUNT, CAT_ID,STATUS, PRICE, QUANTITY, DESCRIPTION, SHOP_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, [catid, cat, quantity])
            cur.execute(sql1, [id,brand, name, 'static/images/cart.png',discount, catid, 'Available', price, quantity, specs, shopid])
            connection.commit()
            cur.close()
        except:

            return render(request,'saleProducts.html',{'message':'SOMETHING IS WRONG! TRY AGAIN PLEASE!','name':shop})
        # cur1 = connection.cursor()
        # return redirect('/sold')
        return render(request, 'saleProducts.html',{'sale':'SELL MORE!','name':shop})
    else:
        return render(request,'saleProducts.html',{'name':shopn})


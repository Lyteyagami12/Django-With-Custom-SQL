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

register = template.Library()
from django.conf import settings
# from django.core.cache import cache
# cache._cache.flush_all()
from django.contrib import  messages

class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/home{request.get_full_path()[1:]}')


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
            sql = "select USERNAME, KEY ,SALT, CUSTOMER_NAME, EMAIL,CUSTOMER_PHOTO from PEOPLE where USERNAME = %s"
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
            img = 'uploads/products/10000069-2_28-fresho-capsicum-green.jpg'
            try:
                img = request[5]
            except:
                print('failed to load image!')
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


def test(request):
    return render(request,'hello.html',{})


def lol(request):
    return render(request, 'lol.html', {})


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


def products(request):
    customerid = None

    name = None
    if request.method == "POST":
        print('i m in POST')

        orderid = random.randrange(start=100000, step=1)
        print("orderid: "+ str(orderid))
        # choice = request.POST.get('choose')
        # print(choice,end=' ')
        # print("!")
        productid = request.POST.get('product')
        print("product:" + str(productid))
        try:
            name = request.session['name']
            email = request.session['email']
        except:
            print('log in first bitch!')
            return redirect('/home/login')
        try:

            # try:
            #     productid = request.POST.get('id')
            # except:
            #     print('failed to get from page')
            #     return redirect('/home')

            cur = connection.cursor()
            result = None
            try:
                cur.execute("select CUSTOMER_ID from PEOPLE where EMAIL=%s", [email])
                result = cur.fetchall()
            except:
                print('no id match with this mail!')
                return redirect('/home')

            print(email)
            for r in result:
                customerid = r[0]
            quantity = 1
            List = []
            price = None
            try:
                cur.execute("SELECT PRODUCT_NAME, PRICE FROM PRODUCTS WHERE PRODUCT_ID = %s", [productid])
                result = cur.fetchall()
                for r in result:
                    price = r[1]
                    product_name = r[0]
                    List.append((product_name, price))
                    print('list created!')
            except:
                print('product not found!')
                return redirect('/home')
            status = 'Not Done'
            List = 'shari, panjubi'
            print("customerid: " + str(customerid))
            date = datetime.date.today()  # .strftime("%d/%m/%Y")
            print("date:" + str(date))
            try:

                cur.execute(
                    "INSERT INTO ORDERS(order_id, customer_id, order_date, amount, quantity, payment_status, items) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    [orderid, customerid, date, price, quantity, status, List])
                connection.commit()
                cur.execute("INSERT INTO PRODUCT_ORDERS(ORDER_ID, PRODUCT_ID) VALUES (%s,%s)", [orderid, productid])
                connection.commit()
                cur.close()
                print('order success!')
            except:
                print('could not make the order!')
                return redirect('/home')
            # return render(request, 'cart.html', {'user': name})
            # print("ki hsse vai!")
            return redirect('/home')
        except:
            print('log in plz!')
            return redirect('/home/login')
    else:
        result = None
        try:
            cur = connection.cursor()
            cur.execute("SELECT * FROM PRODUCTS ")
                        # "where CAT_ID = ("select CAT_ID from CATAGORIES where CAT_NAME = 'Gadgets'"))
            result = cur.fetchall()
            cur.close()
            # print("results:", end=' ')
            # print(len(result))
        except:
            print('product fetch failed!')
            return redirect('/home')
        dic_res = []
        for r in result:
            product_id = r[0]
            product_name = r[1]
            # cat = r[2
            product_photo = r[3]
            status = r[4]
            price = r[5]
            ##password
            # price = r[6]
            discount = r[6]
            quantity = r[7];
            description = r[8]
            shopid = r[9]
            brand = r[10]

            resultt = None
            try:
                cur = connection.cursor()
                cur.execute("select SHOP_NAME from SHOPS where SHOP_ID = %s",[shopid])
                resultt = cur.fetchall()
            except:
                print("Shop not found!")
                return render(request,'index.html', {'msg':'something went wrong!'})
            shopName = None

            for r1 in resultt:
                shopName = r1[0]

            # print("shop name :" + str(shopName))
            row = {'id': product_id, 'shop': shopName,'photo':product_photo,'name': product_name, 'price':price,'brand':brand,
                   'status': status, 'desc': description}
            dic_res.append(row)

        # print("products: ",end=' ')
        # print(dic_res)
        # print("dic len: " ,end=' ')
        # print(len(dic_res))
        cur.close()
        cur = connection.cursor()
        catdic = []
        cur.execute("SELECT CAT_ID, CAT_NAME FROM CATAGORIES")
        catres = cur.fetchall()
        for i in catres:
            catid = i[0]
            catname = i[1]
            catrow = {'id': catid, 'name': catname}
            catdic.append(catrow)
        cur.close()
        # print("cats: ",end=' ')
        # print(len(catdic))
        request.session['cats'] = catdic
        print("closing....")
        message = 'LOG IN'
        logout = 'SIGN UP'
        try:
            username = request.session['name']
            message = username
            logout = 'LOG OUT'
            return render(request, 'index3.html', {'products':dic_res,'catagories':dic_res,'login': message, 'logout': logout})
        except:
            return render(request, 'index3.html', {'products':dic_res,'catagories':dic_res,'login': message, 'logout': logout})


def home(request):
    message = 'LOG IN'
    logout = 'SIGN UP'
    try:
        name = request.session['name']
        message = name
        logout = 'LOG OUT'
        return render(request, 'index.html', {'login': message, 'logout': logout})
    except:
        return render(request, 'index.html', {'login': message, 'logout': logout})


def sell(request):
    name = None
    try:
        name = request.session['shopname']
        return redirect('/saleproduct')
    except:
        print('sell now!')
    return render(request, 'sell.html',{})


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
    sql = "SELECT CUSTOMER_ID, CUSTOMER_NAME, ZONE, EMAIL FROM PEOPLE"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []
    # print("\\")
    for r in result:
        customer_id = r[0]
        customer_name = r[1]
        # username = r[2]
        # customer_photo = r[3]
        # gender = r[4]
        # birthdate = r[5]
        # ##password
        # address = r[7]
        # contact = r[8];
        zone = r[2]
        email = r[3]
        # role = r[4]
        # payment = r[12]
        row = {'customer_id':customer_id,'customer_name':customer_name,'zone':zone,'email':email}
        # row = {'customer_id': customer_id, 'photo': customer_photo, 'customer_name': customer_name, 'gender': gender,
               # 'contact': contact, 'zone': zone, 'email': email, 'payment': payment}
        dict_result.append(row)

    # return render(request,'list_jobs.html',{'jobs' : Job.objects.all()})
    print("showing...")
    return render(request, 'list_jobs.html', {'people': dict_result})


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


def accountsettings(request):
    username = None
    try:
        username = request.session['username']
    except:
        return redirect('/home/login')
    print("i m in profile")
    print(username)
    if request.method == 'POST':
        print("reached!")
        # username = request.POST.get('email')
        #password = request.POST.get('password')

        cursor = connection.cursor()

        sql = "select CUSTOMER_ID  from PEOPLE where USERNAME = %s"
        cursor.execute(sql,[username])
        result = cursor.fetchall()
        email = request.POST.get('email')
        Address = request.POST.get('address')
        contact = request.POST.get('contact')
        # handle_uploaded_file(request.FILES['pro_pic'])
        # f = request.FILES['pro_pic']
        dbid = None

        for r in result:
            dbid = r[0]


        img = request.FILES['pro_pic']
        img_extension = os.path.splitext(img.name)[1]

        user_folder = 'static/uploads/profile/'
        if not os.path.exists(user_folder):
            os.mkdir(user_folder)

        img_save_path =user_folder+'pro_pic'+str(dbid)+img_extension
        # img_save_path = user_folder + 'pro_pic'+img_extension
        img_url = 'uploads/profile/'+'pro_pic'+ str(dbid)+img_extension
        request.session['img_url'] = img_url
        with open(img_save_path, 'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)




        sql = "UPDATE PEOPLE SET USERNAME = %s , EMAIL = %s, ADRESS = %s , CONTACT= %s,CUSTOMER_PHOTO= %s WHERE CUSTOMER_ID = %s"
        cursor.execute(sql,[username,email,Address,contact,img_url,dbid])

        return redirect('/home/profile')
    else:
        return render(request, 'accountsettings.html', {})



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


#
# def order(request):
#     print('i m in order!')
#     customerid = None
#
#     name = None
#     if request.method == "POST":
#         print('i m in POST')
#
#         orderid = random.randrange(start=100000,step=1)
#         # choice = request.POST.get('choose')
#         # print(choice,end=' ')
#         # print("!")
#         productid = request.POST.get('product')
#         print("product:"+str(productid))
#         try:
#             name = request.session['name']
#             email = request.session['email']
#         except:
#             print('log in first bitch!')
#             return redirect('/home/login')
#         try:
#
#             # try:
#             #     productid = request.POST.get('id')
#             # except:
#             #     print('failed to get from page')
#             #     return redirect('/home')
#
#             cur = connection.cursor()
#             result = None
#             try:
#                 cur.execute("select CUSTOMER_ID from PEOPLE where EMAIL=%s",[email])
#                 result = cur.fetchall()
#             except:
#                 print('no id match with this mail!')
#                 return redirect('/home')
#
#             print(email)
#             for r in result:
#                 customerid = r[0]
#             quantity =1
#             List = []
#             price = None
#             try:
#                 cur.execute("SELECT PRODUCT_NAME, PRICE FROM PRODUCTS WHERE PRODUCT_ID = %s",[productid])
#                 result = cur.fetchall()
#                 for r in result:
#                     price = r[1]
#                     product_name = r[0]
#                     List.append((product_name,price))
#                     print('list created!')
#             except:
#                 print('product not found!')
#                 return redirect('/home')
#             status = 'Not Done'
#             List =[]
#             print("customerid: " + str(customerid))
#             try:
#                 cur.execute("INSERT INTO ORDERS(order_id, customer_id, order_date, amount, quantity, payment_status, items) VALUES (%s,%s,%s,%s,%s,%s,%s)",[orderid,customerid,datetime.date.today().strftime("%d/%m/%Y"),price,quantity,status,List])
#                 connection.commit()
#                 cur.execute("INSERT INTO PRODUCT_ORDERS(ORDER_ID, PRODUCT_ID) VALUES (%s,%s)",[orderid,productid])
#                 connection.commit()
#                 cur.close()
#                 print('order success!')
#             except:
#                 print('could not make the order!')
#                 return redirect('/home')
#             # return render(request, 'cart.html', {'user': name})
#             print("ki hsse vai!")
#             return redirect('/home')
#         except:
#             print('log in plz!')
#             return redirect('/home/login')
#     else:
#         print('ufffffffffffo!')
#         return render(request,'index.html',{})


def cart(request):
    # try:

     if request.method == 'POST':

       try:
           updateCart(request)
           return redirect('/home/cart/')
       except:
           print("failed to update cart!")
           return redirect('/home/cart/')
     else:
         print("i m n try")
         car = request.session.get('cart')
         keys = list(car.keys())
         # keys = cart.keys()
         # print(keys)
         print(car)

         print(keys)
         print(car['2001'])
         product_dic = []
         total = 0
         cur = connection.cursor()
         for id in keys:
             cur.execute("select PRODUCT_NAME,PRICE,DESCRIPTION from PRODUCTS where PRODUCT_ID=%s",[int(id)])
             result = cur.fetchone()
             name = result[0]
             price = result[1]
             desc = result[2]
             quantity = int(car[str(id)])
             total+=quantity*price
             row = {'name':name,'price':price,'specs':desc,'id':id,'quantity':quantity,'price_total':quantity*price }
             product_dic.append(row)
         cur.close()
         # return redirect('homepage')
         return render(request,'cart1.html',{'products':product_dic,'total':total})
     # name = request.session['name']
     # /\return render(request, 'cart1.html',{})
    # except:
    #     print('lololo')
    #     return redirect('/home/login')

# checking out===================
def check(request):
    email = None
    try:
        email = request.session['email']
    except:
        return redirect('/home/login')
    if request.method == 'POST':
        fname = request.POST.get('fname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        postcode = request.POST.get('zip')
        city = request.POST.get('city')
        flat = request.POST.get('flat')
        nameoncard = request.POST.get('cardname')
        cardno = request.POST.get('cardnumber')
        expdate = request.POST.get('expdate')
        cvv = request.POST.get('cvv')
        zipcode = int(request.POST.get('zipcode'))
        otp = random.randrange(3456)
        peopleid =None
        sqlonPEOPLE = "SELECT CUSTOMER_ID FROM PEOPLE WHERE EMAIL=%s"
        sqlonOrder = "select ORDER_ID from ORDERS where CUSTOMER_ID=%s"
        orderid = None
        productid = None
        deliveryat = 'Name: '+ fname +'\n'+ 'Address: '+ address + '\n'+'Postcode: '+ postcode + '\n'+ flat + '\n'
        try:
            cur = connection.cursor()
            cur.execute(sqlonPEOPLE, [email])
            result = cur.fetchall()
            for i in result:
                peopleid = i[0]
            result = cur.execute(sqlonOrder, [peopleid])
            for i in result:
                orderid = i[0]

            print("orderid : "+ str(orderid))
            print(peopleid)
            print(email)
            cur.close()
        except:
            print('error from database')
            return redirect('/home/pay')
        try:
            sqlonProduct_order = "SELECT PRODUCT_ID FROM PRODUCT_ORDERS where ORDER_ID =%s"
            sqlonPayment = "INSERT INTO PAYMENTS(PAYMENT_ID, ORDER_ID, PAYMENT_STATUS, METHOD) VALUES (%s,%s,%s,%s)"
            sqlonCreditcard = "INSERT INTO CREDIT_CARD(CARD_NO, NAME_ON_CARD, EXP_DATE, CVV, OTP, PAYMENT_ID, ZIP_CODE) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            sqlonsHipment = "INSERT INTO SHIPMENTS(SHIPMENT_ID, SHIPMENT_DATE, ORDER_ID, STATUS, DELIVERYAT) VALUES (%s,%s,%s,%s,%s)"
            paymentid = random.randrange(102023)
            paymentstatus = "True"
            method = 'CreditCard'
            shipmentid = random.randrange(orderid)
            cur = connection.cursor()
            cur.execute(sqlonProduct_order,[orderid])
            result = cur.fetchall()
            for i in result:
                productid = i[0]
            cur.execute(sqlonPayment,[paymentid,orderid,paymentstatus,method])
            connection.commit()
            cur.execute(sqlonCreditcard,[cardno,nameoncard,expdate,cvv,otp,paymentid,zipcode])
            connection.commit()
            date = datetime.date.today()
            cur.execute(sqlonsHipment,[shipmentid,date,orderid,'False',deliveryat])
            connection.commit()
            cur.close()
            # except:
            #     print("failed to push!")
            print(fname)
            print(city)
            return redirect('/home/shipment')

        except:
             print("failed to push may b unique key violated!")
             return redirect('/home/pay')
    else:
        try:
            username = request.session['name']
            message = username
            logout = 'LOG OUT'

            return render(request, 'check.html', {'login': message, 'logout': logout})
        except:

            return render(request,'check.html',{})

def shipment(request):
    cur = connection.cursor()
    sql = "SELECT * FROM SHIPMENTS"
    cur.execute(sql)
    result = cur.fetchall()
    d = []
    for r in result:
        shipid = r[0]
        shipdate = r[1]
        orderid = r[2]
        status = r[3]
        deliveryat = r[4]
        print(shipid)
        cur.execute("select CUSTOMER_ID from ORDERS where ORDER_ID =%s", [orderid])
        res = cur.fetchall()
        custid = None
        customername = None
        for r1 in res:
            custid = r1[0]
        print(custid)
        cur.execute("select CUSTOMER_NAME from PEOPLE where CUSTOMER_ID=%s",[custid])
        result2 = cur.fetchall()
        for r2 in result2:
            customername = r2[0]
        row = {'id':custid,'name':customername,'address':deliveryat,'orderid':orderid,'shipdate':shipdate}
        d.append(row)
    cur.close()
    return render(request,'shipment.html',{'ship':d})


@register.filter(name="islogin")
def isLogin(request):
    try:
        name = request.session['name']
        return True
    except:
        return False

@register.filter(name="getname")
def getName(request):
    try:
        name = request.session['name']
        return name
    except:
        return 'Anonymous'

def updateCart(request):

        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart

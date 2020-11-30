from django.shortcuts import render, redirect
import random
import os
import hashlib
from datetime import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
# from .models import people
from django.db import connection


def credit_check(request):
    email = None
    try:
        email = request.session['email']
    except:
        print("couldn't find you logged in")
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
        orderid = random.randrange(start=2357119, step=1)

        sqlonPEOPLE = "SELECT CUSTOMER_ID FROM PEOPLE WHERE EMAIL=%s"

        sqlonOrder = "INSERT INTO ORDERS(ORDER_ID, CUSTOMER_ID, ORDER_DATE, AMOUNT, QUANTITY, PAYMENT_STATUS, ITEMS) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        productid = None
        productList = request.session.get('productList')
        print(productList)
        #getting products from cart.....
        cart = request.session.get('cart')
        # print(cart)
        cartkeys = list(cart.keys())
        items = []
        if cart:
           print('something is in cart!')
           for key in cartkeys:
               items.append(productList[key])
        else:
            print('cart is empty!')


        print(cart)
        deliveryat = 'Name: '+ fname +'\n'+ 'Address: '+ address + '\n'+'Postcode: '+ postcode + '\n'+ flat + '\n'
        # try:
        print(
            'trying to order: step-1'
        )
        cur = connection.cursor()
        cur.execute(sqlonPEOPLE, [email])
        result = cur.fetchall()
        cur.close()
        for i in result:
            peopleid = i[0]
        print("people id : " + str(peopleid))
        # print(peopleid)
        print(email)
        orderdate =  datetime.now().strftime("%d-%m-%y %H:%M:%S")
        print(orderdate)

        try:
            total_amount = request.session['total']
        except:
            print('failed to get amount from session!')
            total_amount = 0
        '''Pushing  Orders in order Table'''
        count = len(cartkeys)
        print("length of cart:" + str(count))
        # productList = str(productList)
        items = str(items)
        print("products:"+ items)

        cur = connection.cursor()
        cur.execute(sqlonOrder, [orderid, peopleid, orderdate, total_amount, count, 'False', items])
        connection.commit()
        cur.close()
        print('ordered!')

        '''Now put them on Product_Orders Table'''
        for product in cartkeys:
            try:
                product = int(product)
                cur = Initiate_Cursor()
                cur.execute("INSERT INTO PRODUCT_ORDERS(ORDER_ID, PRODUCT_ID) VALUES (%s,%s)", [orderid, product])
            except:
                print('failed to push in product_orders table')
        # except:
        # print('error from database')
        # return redirect('/home/pay')
        # try:

        # sqlonProduct_order = "SELECT PRODUCT_ID FROM PRODUCT_ORDERS where ORDER_ID =%s"
        sqlonPayment = "INSERT INTO PAYMENTS(PAYMENT_ID, ORDER_ID, PAYMENT_STATUS, METHOD) VALUES (%s,%s,%s,%s)"
        sqlonCreditcard = "INSERT INTO CREDIT_CARD(CARD_NO, NAME_ON_CARD, EXP_DATE, CVV, OTP, PAYMENT_ID, ZIP_CODE) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        sqlonsHipment = "INSERT INTO SHIPMENTS(SHIPMENT_ID, SHIPMENT_DATE, ORDER_ID, STATUS, DELIVERYAT) VALUES (%s,%s,%s,%s,%s)"

        paymentid = random.randrange(start=102023, step=1)
        paymentstatus = "True"
        '''setting payment_status and Credit_card for now. later it should be checked first!'''
        method = 'CreditCard'

        shipmentid = random.randrange(start=orderid, step=1)
        print('expdate', end=' ')
        print(expdate)

        # cur = connection.cursor()
        # cur.execute(sqlonProduct_order, [orderid])
        # result = cur.fetchall()
        # cur.close()
        # for i in result:
        #     productid = i[0]
        print('i m here1')

        cur = Initiate_Cursor()
        cur.execute(sqlonPayment, [paymentid, orderid, paymentstatus, method])
        connection.commit()
        cur.close()
        print('i m here 2')
        cur = Initiate_Cursor()
        cur.execute(sqlonCreditcard, [cardno, nameoncard, expdate, cvv, otp, paymentid, zipcode])
        connection.commit()
        cur.close()
        print('i m here 3')
        date = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        print(date)
        # cur.execute(sqlonsHipment,[shipmentid,date,orderid,'False',deliveryat])
        # connection.commit()
        # cur.close()
        # except:
        #     print("failed to push!")
        print(fname)
        print(city)
        print('order successful!')
        request.session['cart'] = {}
        request.session['productList'] = {}

        return redirect('/home/shipment')

        # except:
        # print("failed to push may b unique key violated!")
        # return redirect('/home/pay')
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
    print(d)
    return render(request,'shipment.html',{'ship':d})


def Initiate_Cursor():
    cursor = connection.cursor()
    return cursor


def emptyCart(request):
    request.session.delete('cart')
    request.session.delete('productList')
    request.session.delete('total')


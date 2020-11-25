from django.shortcuts import render, redirect
import random
import os
import hashlib
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
# from .models import people
from django.db import connection


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


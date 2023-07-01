from django.shortcuts import render
from . import pool
from django.http import JsonResponse
import json
from urllib .parse import unquote


def Index(request):
    return render(request,"Index.html")

def Buy_product(request):
    product=unquote(request.GET['product'])
    product=json.loads(product)
    print('Value: ',product)
    db, cmd = pool.ConnectionPooling()
    query = "select * from pictures where productid={0}".format(product['productid'])
    cmd.execute(query)
    pictures = cmd.fetchall()

    db.close()

    return render(request, "Buy_product.html", {'product': product, 'pictures': pictures})
def Fetch_All_Categories_JSON_user(request):
  try:
    db, cmd = pool.ConnectionPooling()

    Q = "select * from categories"
    cmd.execute(Q)

    records = cmd.fetchall()
    db.close()
    return JsonResponse({'data': records}, safe=False)
  except Exception as e:
    print('error', e)
    return render(request, 'displayAllcategories.html', {'data': None})

def Fetch_All_Product_JSON(request):
  try:
    db, cmd = pool.ConnectionPooling()

    Q = "select p.*,(select c.categoryname from categories c where c.categoryid=p.categoryid) as cname," \
        "(select s.subcategoryname from subcategories s where p.subcategoryid=s.subcategoryid) as scname," \
        "(select b.brandname from brand b where p.brandid=b.brandid) as bname from products p"
    cmd.execute(Q)

    records = cmd.fetchall()
    db.close()
    return JsonResponse({'data': records}, safe=False)
  except Exception as e:
    print('error', e)
    return JsonResponse({'data':[]}, safe=False)

def Fetch_All_SubCategories_JSON_user(request):
  try:
    db, cmd = pool.ConnectionPooling()

    Q = "select * from subcategories"
    cmd.execute(Q)

    records = cmd.fetchall()
    db.close()
    return JsonResponse({'data': records}, safe=False)
  except Exception as e:
    print('error', e)
    return JsonResponse({'data':[]},safe=False)

def AddToCart(request):
   try:
     product=request.GET['product']
     qnty=request.GET['qnty']
     product=product.replace("'","\"")
     product=json.loads(product)
     product['qnty']=qnty
     print('UPDATED PRODUCTS:', product)
     # Crate Cart using session

     try:
       CART_CONTAINER=request.session['CART_CONTAINER']
       CART_CONTAINER[str(product['productid'])]= product
       request.session['CART_CONTAINER'] = CART_CONTAINER
     except:
       CART_CONTAINER={}
       CART_CONTAINER[str(product['productid'])]=product
       request.session['CART_CONTAINER']=CART_CONTAINER
     print('CART: ', CART_CONTAINER)
     CART_CONTAINER = str(CART_CONTAINER).replace("'", "\"")
     return JsonResponse({'data':CART_CONTAINER}, safe=False)

   except Exception as e:
     print(e)
     return JsonResponse({'data': []}, safe=False)


def FetchCart(request):
  try:

    try:
      CART_CONTAINER = request.session['CART_CONTAINER']

    except:
      CART_CONTAINER = {}

    print('CART: ', CART_CONTAINER)
    CART_CONTAINER = str(CART_CONTAINER).replace("'", "\"")
    return JsonResponse({'data': CART_CONTAINER}, safe=False)

  except Exception as e:
    print(e)
    return JsonResponse({'data': []}, safe=False)


def Remove_Cart(request):
  try:
      productid = request.GET['productid']
    # Crate Cart using session

      CART_CONTAINER = request.session['CART_CONTAINER']
      del CART_CONTAINER[productid]
      request.session['CART_CONTAINER'] = CART_CONTAINER
      print('CART: ', CART_CONTAINER)
      CART_CONTAINER = str(CART_CONTAINER).replace("'", "\"")
      return JsonResponse({'data': CART_CONTAINER}, safe=False)

  except Exception as e:
    print(e)
    return JsonResponse({'data': []}, safe=False)

def ShoppingCart(request):
    try:

        try:
            CART_CONTAINER = request.session['CART_CONTAINER']
            totl=0
            totlprice=0
            totlsaving=0
            for key in CART_CONTAINER.keys():
                print('record:',key)
                amt=int(CART_CONTAINER[key]['price'])-int(CART_CONTAINER[key]['offerprice'])
                CART_CONTAINER[key]['save']=amt*int(CART_CONTAINER[key]['qnty'])
                totlsaving+=CART_CONTAINER[key]['save']
                CART_CONTAINER[key]['productprice']=int(CART_CONTAINER[key]['offerprice'])*int(CART_CONTAINER[key]['qnty'])
                totl+=int(CART_CONTAINER[key]['offerprice'])*int(CART_CONTAINER[key]['qnty'])
                totlprice+=int(CART_CONTAINER[key]['price'])*int(CART_CONTAINER[key]['qnty'])


        except Exception as e:
            CART_CONTAINER = {}
            print('errrrrrrrrrr',e)

        print('Shopping_CART: ', CART_CONTAINER.values())
        # CART_CONTAINER = str(CART_CONTAINER).replace("'", "\"")
        return render(request, "MyCart.html",{'data': CART_CONTAINER.values(),'totlamt':totl,'totalproduct':len(CART_CONTAINER.keys()),'totalprice':totlprice,'totalsaving':totlsaving})

    except Exception as e:
        print(e)
        return render(request, "MyCart.html",{'data': {}})


def User_check_mobileno(request):

      mobileno=request.GET['mobileno']
      try:
         db,cmd=pool.ConnectionPooling()

         q="select * from user where mobileno='{0}' ".format(mobileno)

         cmd.execute(q)
         record=cmd.fetchone()
         print('usersign in: ',record)
         if(record):
             return JsonResponse({'data':record,'status':True},safe=True)
         else:
             return JsonResponse({'data':[],'status':False},safe=True)

         db.close()

      except Exception as e:
          print('errorrrr user: ',e)
          return JsonResponse({'data':[]},safe=False)


def UserData(request):

    fname = request.GET['firstname']
    lname= request.GET['lastname']
    mobileno = request.GET['mobileno']
    email = request.GET['email']
    password = request.GET['password']
    try:
        db, cmd = pool.ConnectionPooling()

        q = "insert into user values('{0}','{1}','{2}','{3}','{4}') ".format(fname,lname,mobileno,email,password)

        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'status': True}, safe=True)

    except Exception as e:
        print('errorrrr user: ', e)
        return JsonResponse({'status':False}, safe=False)


def User_check_mobilenoforaddress(request):
    mobileno = request.GET['mobileno']
    try:
        db, cmd = pool.ConnectionPooling()

        q = "select UA.*,(select U.fname from user U where U.mobileno=UA.mobileno)as firstname,(select U.lname from user U where U.mobileno=UA.mobileno)as lastname from user_address UA where UA.mobileno='{0}' ".format(mobileno)

        cmd.execute(q)
        record = cmd.fetchone()
        print('happy: ', record)
        if (record):
            return JsonResponse({'data': record, 'status': True}, safe=True)
        else:
            return JsonResponse({'data': [], 'status': False}, safe=True)

        db.close()

    except Exception as e:
        print('errorrrr user: ', e)
        return JsonResponse({'data': []}, safe=False)


def UseraddressData(request):

    house = request.GET['house']
    areaname= request.GET['areaname']
    mobileno = request.GET['m3mobileno']
    email = request.GET['m3email']
    city = request.GET['city']
    state = request.GET['state']
    pincode = request.GET['pincode']
    try:
        db, cmd = pool.ConnectionPooling()

        q = "insert into user_address(mobileno,email,houseno,areaname,city,state,pincode) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}') ".format(mobileno,email,house,areaname,city,state,pincode)
        print("address: ",q)
        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'status': True}, safe=True)

    except Exception as e:
        print('errorrrr user: ', e)
        return JsonResponse({'status':False}, safe=False)

from django.shortcuts import render
from . import pool
from  django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def product_interface(request):
    try:
        admin=request.session['ADMIN']
        return render(request, "product_interface.html")
    except:
        return render(request, "Admin_login.html")

@xframe_options_exempt
def product_submit(request):
    try:
        db,cmd=pool.ConnectionPooling()
        categoryid=request.POST['categoryid']
        subcategoryid=request.POST['subcategoryid']
        brandid=request.POST['brandid']
        productname=request.POST['productname']
        price=request.POST['price']
        offerprice=request.POST['offerprice']
        quantity=request.POST['quantity']
        packingtype=request.POST['packingtype']
        productstatus=request.POST['productstatus']
        salestatus=request.POST['salestatus']
        producticon=request.FILES['productimage']

        q="insert into products(categoryid,subcategoryid,brandid,productname,price,offerprice,quantity,productimage,packingtype" \
          ",salestatus,status) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format  \
            (categoryid,subcategoryid,brandid,productname,price,offerprice,quantity,producticon.name,packingtype,salestatus,productstatus)

        S=open("c:/users/H.P/django project/medassist_ecom/assets/"+producticon.name,'wb')

        for chunk in producticon.chunks():
             S.write(chunk)
             S.close()

        cmd.execute(q)
        db.commit()
        db.close()

        return render(request, 'product_interface.html', {'message': 'record submitted successfully'})

    except Exception as e:
           print('error', e)
           return render(request, 'product_interface.html', {'message': 'record not  submitted'})

@xframe_options_exempt
def product_display(request):

   try:
       admin=request.session['ADMIN']
       try:
         db,cmd=pool.ConnectionPooling()

         q="select p.*,(select c.categoryname from categories c where c.categoryid=p.categoryid) as cname," \
           "(select s.subcategoryname from subcategories s where p.subcategoryid=s.subcategoryid) as scname," \
           "(select b.brandname from brand b where p.brandid=b.brandid) as bname from products p"

         cmd.execute(q)
         record=cmd.fetchall()

         db.close()

         return render(request, 'Display_product.html', {'records': record})

       except Exception as e:
         print('error', e)
         return render(request,'Display_product.html', {'records': None})
   except:
         return render(request, "Admin_login.html")


@xframe_options_exempt
def edit_product(request):
    try:
        db,cmd=pool.ConnectionPooling()

        categoryid=request.GET['categoryid']
        subcategoryid=request.GET['subcategoryid']
        productid=request.GET['productid']
        brandid=request.GET['brandid']
        productname=request.GET['productname']
        price=request.GET['price']
        offerprice=request.GET['offerprice']
        quantity=request.GET['quantity']
        packingtype=request.GET['packingtype']
        status=request.GET['status']
        salestatus=request.GET['salestatus']

        q="update products set categoryid='{0}',subcategoryid='{1}',brandid='{2}',productname='{3}',price='{4}',offerprice='{5}',quantity='{6}'" \
          ",packingtype='{7}',status='{8}',salestatus='{9}' where productid='{10}' ".format(categoryid,subcategoryid,brandid,productname,price,offerprice
            ,quantity,packingtype,status,salestatus,productid)

        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'result': True}, safe=False)

    except Exception as e:
        print('Error', e)
        return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def delete_product(request):
    try:
        db,cmd=pool.ConnectionPooling()
        productid=request.GET['productid']

        q="delete from products where productid={0}".format(productid)

        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'result': True}, safe=False)

    except Exception as e:
        print('Error', e)
        return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def edit_producticon(request):
        try:
            db, cmd = pool.ConnectionPooling()
            productid = request.POST['productid']
            producticon = request.FILES['producticon']

            q = "update products set productimage='{0}' where productid='{1}' ".format(producticon.name,productid)
            print(q)
            f = open("c:/users/H.P/django project/medassist_ecom/assets/" + producticon.name, 'wb')

            for chunk in producticon.chunks():
                f.write(chunk)
            f.close()

            cmd.execute(q)
            db.commit()
            db.close()

            return JsonResponse({'result': True}, safe=False)
        except Exception as e:
            print('Error', e)
            return JsonResponse({'result': False}, safe=False)


@xframe_options_exempt
def images_interface(request):
    try:
        admin = request.session['ADMIN']
    except:
        return render(request, 'Login_Page.html')
    return render(request,"addpicture.html")


@xframe_options_exempt
def Add_picture(request):
    try:
        db,cmd=pool.ConnectionPooling()
        categoryid=request.POST['categoryid']
        subcategoryid=request.POST['subcategoryid']
        brandid=request.POST['brandid']
        productid=request.POST['productid']
        productimage=request.FILES['productimage']
        query="insert into pictures(categoryid,subcategoryid,brandid,productid,images) values('{0}','{1}','{2}','{3}','{4}')".format(categoryid,subcategoryid,brandid,productid,productimage)
        F = open("C:/Users/H.P/django project/medassist_ecom/assets/" + productimage.name, 'wb')
        for chunk in productimage.chunks():
            F.write(chunk)
        F.close()
        cmd.execute(query)
        db.commit()
        db.close()
        return render(request,"addpicture.html",{'message':'Picture added successfully'})
    except Exception as e:
        return render(request,"addpicture.html",{'message':'Something went wrong'})



@xframe_options_exempt
def fetch_all_product_json(request):
    try:
        db, cmd = pool.ConnectionPooling()
        brandid=request.GET['brandid']
        query = "select * from products where brandid={0}".format(brandid)
        print(query)
        cmd.execute(query)
        result = cmd.fetchall()
        print('xxxxxxxxxxx',result)
        db.close()
        return JsonResponse({'pdata':result}, safe=False)
    except Exception as e:
        return JsonResponse({'pdata': None}, safe=False)

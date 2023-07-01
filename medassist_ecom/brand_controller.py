from django.shortcuts import render
from . import pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def main(request):
    try:
        admin=request.session['ADMIN']
        return render(request,'brand_interface.html')
    except:
        return render(request,"Admin_login.html")

@xframe_options_exempt
def submit_brand(request):
    try:
        db,cmd=pool.ConnectionPooling()
        categoryid=request.POST['categoryid']
        subcategoryid=request.POST['subcategoryid']
        brandname=request.POST['brandname']
        contactperson=request.POST['contactperson']
        mobilenumber=request.POST['mobilenumber']
        status=request.POST['status']
        brandicon=request.FILES['brandicon']

        Q="insert into brand(categoryid,subcategoryid,brandname,contactperson,mobilenumber,status,brandicon) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(categoryid,subcategoryid,brandname,contactperson,mobilenumber,status,brandicon.name)

        S=open("c:/users/H.P/django project/medassist_ecom/assets/"+brandicon.name,'wb')

        for chunk in brandicon.chunks():
            S.write(chunk)
            S.close()

        cmd.execute(Q)
        db.commit()
        db.close()

        return render(request,'brand_interface.html',{'message':'record submitted successfully'})
    except Exception as e:
        print('error',e)
        return render(request, 'brand_interface.html', {'message': 'record not  submitted'})

@xframe_options_exempt
def displaybrand(request):

    try:
        admin=request.session['ADMIN']

        try:
          db, cmd = pool.ConnectionPooling()

          Q = "select B.*,(select C.categoryname from categories C where C.categoryid=B.categoryid ) as cname from brand B"
          cmd.execute(Q)

          records = cmd.fetchall()
          print(records)
          db.close()

          return render(request,'display_brand.html', {'records': records})

        except Exception as e:
          print('error', e)
          return render(request,'display_brand.html', {'records': None})
    except:
        return render(request,"Admin_login.html")

@xframe_options_exempt
def update_brand(request):
    try:
        db,cmd=pool.ConnectionPooling()

        brandid=request.GET['brandid']
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        brandname = request.GET['brandname']
        contactperson = request.GET['contactperson']
        mobilenumber = request.GET['mobilenumber']
        status = request.GET['status']


        q="update brand set categoryid='{0}',subcategoryid='{1}',brandname='{2}',contactperson='{3}',mobilenumber='{4}',status='{5}' where brandid='{6}'".format(categoryid,subcategoryid,brandname,contactperson,mobilenumber,status,brandid)
        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'result': True}, safe=False)

    except Exception as e:
       print('Error', e)
       return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def brand_delete(request):
    try:
        db,cmd=pool.ConnectionPooling()

        brandid=request.GET['brandid']

        q="delete from brand where brandid='{0}'".format(brandid)

        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        print('Error', e)
        return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def edit_brandicon(request):
    try:
        db, cmd = pool.ConnectionPooling()
        brandicon = request.FILES['brandicon']
        brandid=request.POST['brandid']

        q = "update brand set brandicon='{0}' where brandid='{1}' ".format(brandicon.name,brandid)

        S = open("c:/users/H.P/django project/medassist_ecom/assets/" + brandicon.name, 'wb')

        for chunk in brandicon.chunks():
            S.write(chunk)
            S.close()

        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        print('Error', e)
        return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def fetch_all_brand_json(request):
    try:
        db, cmd = pool.ConnectionPooling()

        subcategoryid = request.GET['subcategoryid']

        Q = "select * from brand where subcategoryid={0}".format(subcategoryid)
        cmd.execute(Q)

        records = cmd.fetchall()
        db.close()
        return JsonResponse({'bdata': records}, safe=False)

    except Exception as e:
        print('error', e)
        return JsonResponse({'bdata': None}, safe=True)


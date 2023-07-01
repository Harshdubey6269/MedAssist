from django.shortcuts import render
from . import pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def category_interface(request):
   try:
     admin=request.session['ADMIN']
     return render(request, "Categoryinterface.html")
   except:
    return render(request,"Admin_login.html")

@xframe_options_exempt
def submit_category(request):
  try:
    db,cmd=pool.ConnectionPooling()
    categoryname=request.POST['categoryname']
    categoryicon=request.FILES['categoryicon']

    q="insert into categories(categoryname,categoryicon) values ('{0}' , '{1}')".format(categoryname,categoryicon.name)
    f=open("c:/users/H.P/django project/medassist_ecom/assets/"+categoryicon.name,'wb')

    for chunk in categoryicon.chunks():
      f.write(chunk)
    f.close()
    cmd.execute(q)
    db.commit()
    db.close()

    return render(request, 'Categoryinterface.html', {'message': 'Record submitted'})
  except Exception as e:
    print('Error',e)
    return render(request, 'Categoryinterface.html', {'message': 'Record not  submitted'})

@xframe_options_exempt
def displayyAll_categories(request):
  try:
    admin = request.session['ADMIN']

    try:
       db, cmd = pool.ConnectionPooling()

       Q = "select * from categories"
       cmd.execute(Q)

       records = cmd.fetchall()
       db.close()
       return render(request, 'displayAllcategories.html', {'records': records})

    except Exception as e:
       print('error', e)
       return render(request, 'displayAllcategories.html', {'records': None})

  except:
    return render(request, "Admin_login.html")


@xframe_options_exempt
def edit_category(request):
       try:
         db, cmd = pool.ConnectionPooling()
         categoryname = request.GET['categoryname']
         categoryid = request.GET['categoryid']

         q = "update categories set categoryname='{0}' where categoryid='{1}' ".format(categoryname,categoryid)


         cmd.execute(q)
         db.commit()
         db.close()

         return JsonResponse({'result':True},safe=False)
       except Exception as e:
         print('Error', e)
         return JsonResponse({'result':False},safe=False)

@xframe_options_exempt
def delete_category(request):
  try:
    db, cmd = pool.ConnectionPooling()

    categoryid = request.GET['categoryid']

    q = "delete from categories where categoryid='{0}' ".format(categoryid)

    cmd.execute(q)
    db.commit()
    db.close()

    return JsonResponse({'result': True}, safe=False)
  except Exception as e:
    print('Error', e)
    return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def edit_categoryicon(request):
       try:
         db, cmd = pool.ConnectionPooling()
         categoryid = request.POST['categoryid']
         categoryicon = request.FILES['categoryicon']

         q = "update categories set categoryicon='{0}' where categoryid='{1}' ".format(categoryicon.name,categoryid)
         print(q)
         f = open("c:/users/H.P/django project/medassist_ecom/assets/" + categoryicon.name, 'wb')

         for chunk in categoryicon.chunks():
           f.write(chunk)
         f.close()

         cmd.execute(q)
         db.commit()
         db.close()

         return JsonResponse({'result':True},safe=False)
       except Exception as e:
         print('Error', e)
         return JsonResponse({'result':False},safe=False)

@xframe_options_exempt
def Fetch_All_Categories_JSON(request):
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

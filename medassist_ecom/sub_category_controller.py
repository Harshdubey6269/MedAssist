from django.shortcuts import render
from . import pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def subcategory_interface(request):
    try:
        admin = request.session['ADMIN']
        return render(request, "sub_category.html")
    except:
        return render(request, "Admin_login.html")


@xframe_options_exempt
def submit_subcategory(request):
    try:
        db,cmd=pool.ConnectionPooling()
        categoryid=request.POST['categoryid']
        subcategoryname=request.POST['subcategoryname']
        subcategoryicon=request.FILES['subcategoryicon']

        Q="insert into subcategories(categoryid,subcategoryname,subcategoryicon) values ('{0}','{1}','{2}')".format(categoryid,subcategoryname,subcategoryicon.name)

        S=open("c:/users/H.P/django project/medassist_ecom/assets/"+subcategoryicon.name,'wb')

        for chunk in subcategoryicon.chunks():
            S.write(chunk)
            S.close()

        cmd.execute(Q)
        db.commit()
        db.close()

        return render(request,'sub_category.html',{'message':'record submitted successfully'})
    except Exception as e:
        print('error',e)
        return render(request, 'sub_category.html', {'message': 'record not  submitted'})


@xframe_options_exempt
def displayySub_categories(request):
    try:
        admin = request.session['ADMIN']

        try:
            db, cmd = pool.ConnectionPooling()

            Q = "select S.*,(select C.categoryname from categories C where C.categoryid=S.categoryid) as cname from subcategories S"
            cmd.execute(Q)

            records = cmd.fetchall()
            db.close()
            return render(request, 'Display_subcategory.html', {'records': records})

        except Exception as e:
            print('error', e)
            return render(request, 'Display_subcategory.html', {'records': None})

    except:
        return render(request, "Admin_login.html")



@xframe_options_exempt
def edit_subcategory(request):
    try:
        db, cmd = pool.ConnectionPooling()
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        subcategoryname=request.GET['subcategoryname']

        q = "update subcategories set subcategoryname='{0}',  categoryid='{1}' where subcategoryid='{2}' ".format(subcategoryname,categoryid,subcategoryid)

        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        print('Error', e)
        return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def delete_subcategory(request):
    try:
        db, cmd = pool.ConnectionPooling()
        subcategoryid = request.GET['subcategoryid']


        q = "delete  from subcategories where subcategoryid='{0}' ".format(subcategoryid)

        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        print('Error', e)
        return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def edit_subcategoryicon(request):
    try:
        db, cmd = pool.ConnectionPooling()
        subcategoryicon = request.FILES['subcategoryicon']
        subcategoryid=request.POST['subcategoryid']

        q = "update subcategories set subcategoryicon='{0}' where subcategoryid='{1}' ".format(subcategoryicon.name,subcategoryid)

        S = open("c:/users/H.P/django project/medassist_ecom/assets/" + subcategoryicon.name, 'wb')

        for chunk in subcategoryicon.chunks():
            S.write(chunk)
            S.close()

        cmd.execute(q)
        db.commit()
        db.close()

        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        print('Error', e)
        return JsonResponse({'result': False}, safe=False)
'['
@xframe_options_exempt
def fetch_all_subcategories_json(request):
    try:
      db, cmd = pool.ConnectionPooling()

      categoryid=request.GET['categoryid']

      Q = "select * from subcategories where categoryid={0}".format(categoryid)
      cmd.execute(Q)

      records = cmd.fetchall()
      db.close()
      return JsonResponse({'subdata':records}, safe=False)

    except Exception as e:
      print('error', e)
      return JsonResponse({'subdata': None}, safe=True)


from django.shortcuts import render
from . import pool
from django.http import JsonResponse


def Login_interface(request):
    return render(request,'Admin_login.html')

def Admin_logout(request):
    del request.session['ADMIN']
    return render(request,'Admin_login.html')

def Login_success(request):
    try:
        db,cmd=pool.ConnectionPooling()

        username=request.POST['username']
        password=request.POST['password']

        q="select * from adminlogin where emailid='{0}' and password='{1}'".format(username,password)
        cmd.execute(q)

        row=cmd.fetchone()

        if(row):
            request.session['ADMIN']=row  #session variable  ADMIN

            return render(request, 'Dashboard.html',{'Admindata':row})
        else:
            return render(request, 'Admin_login.html', {'message': 'Invalid Email-Id/Password'})

        db.commit()
        db.close()

    except Exception as e:
        print('Error login:', e)
        return render(request, 'Admin_login.html')

def dashboard(request):
    return render(request,'Dashboard.html')


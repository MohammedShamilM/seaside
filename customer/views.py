from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='admin_login')
def user_list(request):
    if request.user.is_staff:
        User = get_user_model()
        users = User.objects.all().order_by('id')
    
        return render(request,'admin-user.html',{'users': users})
    else:
        return redirect('user_login')

@login_required(login_url='admin_login')
def toggle_user_status(request, user_id):
    if request.user.is_staff:
        User = get_user_model()

        user = User.objects.get(id = user_id)
        if user.is_active:
            user.is_active= False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('user_list') 
    else:
        return redirect('user_login')
from django.shortcuts import render,redirect
from . models import Coupons
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cartandcheckout.models import cart,CartItem
from useraccount.models import user_address
from orders.models import orders
from wallet.models import Wallet



# Create your views here.
@login_required(login_url='admin_login')
def coupon(request):
    coupons = Coupons.objects.order_by('-created_at')
    return render(request,'coupon.html',{'coupons':coupons})

@login_required(login_url='admin_login')
def add_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('couponcode')
        discount = request.POST.get('discount')
        min_order_amount = request.POST.get('min_order_amount')
        expiration_date = request.POST.get('expiration_date')
        details = request.POST.get('details')
        if Coupons.objects.filter(code = code).exists():
            return render(request,'add-coupon.html',{'message' : 'coupon already exist'})
        else:
            coupon = Coupons(code = code, discount = discount, min_order_amount = min_order_amount,expiration_date = expiration_date,details = details)
            coupon.save()
            return redirect('coupons')
    else:
        return render(request,'add-coupon.html')

@login_required(login_url='admin_login')
def toggle_coupon_status(request,coupon_id):
    if request.user.is_staff:
        coupon = Coupons.objects.get(id = coupon_id)
        if coupon.is_active:
            coupon.is_active = False
            coupon.save()
        else:
            coupon.is_active = True
            coupon.save()
        return redirect('coupons')
    else:
        return redirect('user_login')


@login_required(login_url='admin_login')
def edit_coupon(request,coupon_id):
    if request.user.is_staff:
        Coupon = Coupons.objects.get(id = coupon_id)
        if request.method == 'POST':
            code = request.POST.get('couponcode')
            discount = request.POST.get('discount')
            min_order_amount = request.POST.get('min_order_amount')
            expiration_date = request.POST.get('expiration_date')
            details = request.POST.get('details')
            
            Coupon.code = code
            Coupon.discount = discount
            Coupon.min_order_amount = min_order_amount
            Coupon.expiration_date = expiration_date
            Coupon.details = details
            Coupon.save()
            return redirect('coupons')
        return render(request,'add-coupon.html',{'coupon' : Coupon})
    else:
        return redirect('user_login')


@login_required(login_url='user_login')
def apply_coupon(request):
    if request.method == 'POST':
        User = request.user
        Cartofuser = cart.objects.get(user = User)
        Cart_Item =  CartItem.objects.filter(Cart = Cartofuser)
        totalprice = sum([item.item_total for item in Cart_Item])
        coupons = Coupons.objects.all().filter(is_active = True)
        order = orders.objects.filter(user = User,discount = 50)
        useraddress = user_address.objects.filter(user = User)
        code = request.POST.get('couponcode')
        print(code,totalprice)
        coupon = Coupons.objects.get(code = code)
        order = orders.objects.filter(user = User,discount = coupon.discount).first()
        wallet_balance = Wallet.objects.get(user = User)
        if not order:
            if coupon.min_order_amount > totalprice:
                message = 'Minimum order amount not reached'
                return render(request,'checkout.html',{'Cart_Item': Cart_Item,
                                                       'totalprice': totalprice,                                                           
                                                       'coupons': coupons,                                                           
                                                       'useraddress': useraddress,
                                                       'message' : message,
                                                       'wallet_balance':wallet_balance})

            if coupon.discount:
                discount = (totalprice /100) * coupon.discount
                discounted_price = totalprice - discount
                return render(request,'checkout.html',{'Cart_Item': Cart_Item,
                                                       'totalprice': totalprice,
                                                       'coupon': coupon,
                                                       'coupons': coupons,
                                                       'discounted_price':discounted_price,
                                                       'useraddress': useraddress,
                                                       'wallet_balance':wallet_balance})
        else:
            return render(request,'checkout.html',{'Cart_Item': Cart_Item,
                                                       'totalprice': totalprice,                                                           
                                                       'coupons': coupons,                                                           
                                                       'useraddress': useraddress,
                                                       'message' : 'coupon already used',
                                                       'wallet_balance':wallet_balance})

        

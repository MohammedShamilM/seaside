from django.shortcuts import render,redirect
from . models import orders,order_items
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from wallet.models import Wallet,Transaction
from products.models import variant


# Create your views here.
@login_required(login_url='admin_login')
def admin_order_list(request):
    if request.user.is_staff:
        order_list = orders.objects.all().order_by('-created_at')
        return render(request, 'admin-order-list.html',{'order_list': order_list})  
    else:
        return redirect('user_login')


@login_required(login_url='admin_login')
def admin_order_detail(request,order_id):
    if request.user.is_staff:

        order = orders.objects.get(id = order_id)
        order_items = order.order_items.all()
        status_options = ['Order confirmed', 'Shipped', 'Out For Delivery', 'Delivered', 'Cancelled']
        if request.method == 'POST':
            status = request.POST.get('status') 
            if order.order_status != 'Cancelled' and order.order_status != 'Delivered' :
                order.order_status = status
                order.save()
                # to change the item status also into delivered#
                #-------------------------------------------------#
                for item in order_items:
                    if order.order_status == 'Delivered' and item.status != 'Cancelled':
                        item.status = 'Delivered'
                        item.save()
                print(order.payment_method)
                # to change the payment_status if it is delivered and COD#
                if order.order_status == 'Delivered' and order.payment_method  == 'Cash On Delivery':             
                    order.payment_status = 'Success'
                    order.save()

                    # do the things with all status 
            
                
                return render(request, 'admin-order-details.html',{'order': order,'order_items': order_items,'status_options' : status_options})
            else:
                message = f"cannot change the status of {order.order_status} order"
                return render(request, 'admin-order-details.html',{'order': order,'order_items': order_items,'message' : message,'status_options' : status_options})
        else:   
            return render(request, 'admin-order-details.html',{'order': order,'order_items': order_items,'status_options' : status_options})
    else:
        return redirect('user_login')

@login_required(login_url='admin_login')
def search_orders_admin(request):
    if request.user.is_staff:
        query = request.GET.get('query', '').strip()
        if query:
            # Always apply filters to order_id (numeric or not)
            filters = (Q(order_id__icontains=query) | 
                    Q(order_status__icontains=query) | 
                    Q(user__username__icontains=query)|
                    Q(shipping_address__address__icontains = query)
                    )

            # Add a filter for `total_price` only if the query is numeric
            if query.replace('.', '', 1).isdigit():
                filters |= Q(total_price__icontains=query)

            # Apply the combined filters
            result = orders.objects.select_related('shipping_address').filter(filters)
        
            return render(request, 'admin-order-list.html',{'result': result}) 
        else:
            return render(request, 'admin-order-list.html',{'none':'none'})
    else:
        return redirect('user_login')
     
     
@login_required(login_url='user_login')
def cancel_order(request,item_id):
    Item = order_items.objects.get(id = item_id)
    order_id = Item.order.id
    Items = order_items.objects.filter(order = order_id)
    order = orders.objects.get(id = order_id)
    flag = 0
    

    Item.status = 'Cancelled'
    Variant = Item.variant
    Variant.stock = Variant.stock + Item.quantity
    Variant.save()
    Item.save()
    order.total_price -= Item.subtotal
    order.save()
    if order.payment_method != 'Cash On Delivery':
        wallet = Wallet.objects.get(user = request.user)
        wallet.balance = wallet.balance + Item.subtotal
        wallet.save()
        details = f"cancelled orders of  {Item.product.name}"
        transaction = Transaction(wallet = wallet,
                                  transaction_type = 'credit',
                                  amount = Item.subtotal,
                                  balance_after = wallet.balance,
                                  details = details)
        transaction.save()
    
    for item in Items:
        if item.status != 'Cancelled':
            flag = 1
    if flag == 0:
        order.order_status = 'Cancelled'
        if order.payment_method != 'Cash On Delivery':
            order.payment_status = 'Refunded'
        order.save()

        
    return redirect('order_details',order_id = order_id)
    
    
    
@login_required(login_url='user_login')
def request_return(request,item_id):
    Item = order_items.objects.get(id = item_id)
    order_id = Item.order.id
    Items = order_items.objects.filter(order = order_id)
    order = orders.objects.get(id = order_id)
    flag = 0

    Item.status = 'Requested Return'
    Item.save()
    return redirect('order_details',order_id)



@login_required(login_url='user_login')
def approve_return(request,item_id):
    Item = order_items.objects.get(id = item_id)
    order_id = Item.order.id
    Items = order_items.objects.filter(order = order_id)
    order = orders.objects.get(id = order_id)
    flag = 0
    

    Item.status = 'Returned'
    Variant = Item.variant
    Variant.stock = Variant.stock + Item.quantity
    Variant.save()
    Item.save()
    order.total_price -= Item.subtotal
    order.save()
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    wallet.balance = wallet.balance + Item.subtotal
    wallet.save()
    details = f"Return orders of  {Item.product.name}"
    transaction = Transaction(wallet = wallet,
                              transaction_type = 'credit',
                              amount = Item.subtotal,
                              balance_after = wallet.balance,
                              details = details)
    transaction.save()
    check = 0
    for item in Items:
        if item.status != 'Returned':
            flag = 1
        elif item.status == 'Cancelled' or item.status == 'Returned':
            continue
        else:
            check = 1
    
    if flag == 0:
        order.order_status = 'Returned'
        order.payment_status = 'Refunded'
        order.save()
        
    if check == 0 :
        order.payment_status = 'Refunded'
        order.order_status = 'Returned'
        order.save()
        
    return redirect('admin_order_detail',order_id = order_id)



    
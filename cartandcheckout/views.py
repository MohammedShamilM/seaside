from django.shortcuts import render,redirect
from . models import cart,CartItem
from products.models import variant,product, VariantImage
from coupon.models import Coupons   
from useraccount.models import user_address  
from orders.models import orders,order_items,shipping_address
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from wallet.models import Wallet,Transaction

# Create your views here.
@login_required(login_url='user_login')
def Cart(request):
    User = request.user
    print(request.user)
    Cartuser = cart.objects.get_or_create(user = User)
    Cartofuser = cart.objects.get(user = User)
    Cart_Item =  CartItem.objects.filter(Cart = Cartofuser).order_by('-created_at')
    totalprice = sum([item.item_total for item in Cart_Item])
    return render (request,'cart.html',{'Cart_Item': Cart_Item,'totalprice': totalprice})

@login_required(login_url='user_login')
def add_to_cart(request,variant_id):
    if request.user.is_authenticated:
        Variant = variant.objects.prefetch_related('images').get(id = variant_id)
        Product = product.objects.get(id = Variant.product_id)
        images = VariantImage.objects.filter(variant = variant_id )
        img = images[0].image
        
        if cart.objects.filter(user = request.user).exists():
            Cart = cart.objects.get(user = request.user)
        else:
            Cart = cart(user = request.user)
            Cart.save()
        if  CartItem.objects.filter(Cart = Cart, variant = Variant).exists():
            return redirect('cart')
        else:
            Cart_Item = CartItem(Cart = Cart, variant = Variant, product = Product, item_total = Variant.final_price, image = img )
            Cart_Item.save()
            return redirect('cart')
        
    else:
        return redirect('home')
    
@login_required(login_url='user_login')
def remove_from_cart(request,variant_id):
    if request.user.is_authenticated:
        Variant = variant.objects.get(id = variant_id)
        Cart = cart.objects.get(user = request.user)
        Cart_Item = CartItem.objects.get(Cart = Cart, variant = Variant)
        Cart_Item.delete()
        return redirect('cart')
    else:
        return redirect('cart')
    
@login_required(login_url='user_login')
def add_quantity(request,variant_id):
    if request.user.is_authenticated:
        Variant = variant.objects.get(id = variant_id)
        Cart = cart.objects.get(user = request.user)
        Cart_Item = CartItem.objects.get(Cart = Cart, variant = Variant)
        if Variant.stock > Cart_Item.quantity:
            Cart_Item.quantity += 1
            Cart_Item.item_total = Cart_Item.quantity * Variant.final_price
            Cart_Item.save()
        return redirect('cart')
    else:
        return redirect('products')


@login_required(login_url='user_login')
def remove_quantity(request,variant_id):
    if request.user.is_authenticated:
        Variant = variant.objects.get(id = variant_id)
        Cart = cart.objects.get(user = request.user)
        Cart_Item = CartItem.objects.get(Cart = Cart, variant = Variant)
        if Cart_Item.quantity == 1:
            Cart_Item.delete()
        else:
            Cart_Item.quantity -= 1
            Cart_Item.item_total = Cart_Item.quantity * Variant.final_price
            Cart_Item.save()
        return redirect('cart')
    else:
        return redirect('products')


@login_required(login_url='user_login')
def checkout (request):
    User = request.user
    if cart.objects.filter(user = User).exists():
        Cartofuser = cart.objects.get(user = User)
    else:
        Cartofuser = None
    coupons = Coupons.objects.filter(is_active= True)
    Cart_Item =  CartItem.objects.filter(Cart = Cartofuser)
    totalprice = int(sum([item.item_total for item in Cart_Item]))
    useraddress = user_address.objects.filter(user = User)
    if Wallet.objects.filter(user = User).exists():
        wallet_balance = Wallet.objects.get(user = User)
    else:
        wallet_balance = 0
    
    

    # checking is there any 0 stock products#
    # -----------------------------------------#
    for item in Cart_Item:
        if item.variant.stock <= 0:
            return render (request,'cart.html',{'Cart_Item': Cart_Item,'totalprice': totalprice,'message' : 'Remove 0 stock product from cart'})

    # checking is there any over quantity products#
    # -----------------------------------------#    
    for item in Cart_Item:
        if item.quantity > 10:
            return render (request,'cart.html',{'Cart_Item': Cart_Item,'totalprice': totalprice,'message' : 'Reduce the quantity of item'})

    # for adding new address
    # -------------------------
    if request.method == 'POST' :
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('zip')
        phone_number = request.POST.get('phone')

        user = request.user
        address = user_address(name = name,
                           address = address,
                           city = city,
                           state =  state,
                           postal_code = postal_code,
                           phone_number = phone_number,
                           user = user
                           )
        address.save()
        return render(request,'checkout.html',{'Cart_Item': Cart_Item,'totalprice': totalprice,'coupons': coupons,'useraddress': useraddress,'wallet_balance' : wallet_balance})
    else:
        return render(request,'checkout.html',{'Cart_Item': Cart_Item,'totalprice': totalprice,'coupons': coupons,'useraddress': useraddress,'wallet_balance' : wallet_balance})




import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from decimal import Decimal,InvalidOperation
from django.http import HttpResponse


@login_required(login_url='user_login')
def orderPlaced(request):
    if request.method == 'POST':
        useraddress = request.POST.get('address')
        payment_method = request.POST.get('paymentmethod')
        totalprice = request.POST.get('totalprice')
        discount_price = request.POST.get('discounted_price')
        if discount_price == '':
            discount_price = 0
        shipping_fee = request.POST.get('shipping_fees')
        print('shipping fees',shipping_fee)
        
        print('this is the total price ',totalprice)
        print('this is the discount price',discount_price)

        coupon_discount = request.POST.get('coupon_discount')
        if coupon_discount == '':
            coupon_discount = 0
        User = request.user
        Cartofuser = cart.objects.get(user=User)
        Cart_Item = CartItem.objects.filter(Cart=Cartofuser)
        address = user_address.objects.get(id=useraddress)

        # Generate random order_id
        import random
        def generate_order_id():
            order_id = random.randint(100000, 999999)
            if orders.objects.filter(order_id=order_id).exists():
                return generate_order_id()
            return order_id

        shippingaddress = shipping_address(
            user=User,
            name=address.name,
            address=address.address,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code,
            phone_number=address.phone_number
        )
        shippingaddress.save()

        if payment_method == 'Cash On Delivery':
            order = orders(
                user=User,
                order_id=generate_order_id(),
                total_price=totalprice,
                discount = coupon_discount,
                discount_price = discount_price,
                payment_method=payment_method,
                shipping_address=shippingaddress
            )
            order.save()
            if order.discount_price and int(order.discount_price) <= 500:
                order.shipping_fees = shipping_fee
            elif int(order.total_price) <= 500:
                order.shipping_fees = shipping_fee
            order.save()
            print('order has shipping_fees',order.shipping_fees)

            for item in Cart_Item:
                order_item = order_items(
                    order=order,
                    product=item.product,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.price,
                    subtotal=item.item_total,
                )
                order_item.save()
                Variant = variant.objects.get(id=item.variant.id)
                Variant.stock -= item.quantity
                Variant.save()
                item.delete()

            return render(request, 'ordersuccess.html', {'order': order} )

        elif payment_method == 'Razorpay':
            # Create a Razorpay order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.set_app_details({"title": "seaside", "version": "1.0"})
            if discount_price:
                razorpay_order = client.order.create({
                    "amount": int(float(discount_price)) * 100,  # Razorpay expects amount in paise
                    "currency": "INR",
                    "payment_capture": "1"  # Auto-capture payment
                })
            else:
                razorpay_order = client.order.create({
                    "amount": int(float(totalprice)) * 100,  # Razorpay expects amount in paise
                    "currency": "INR",
                    "payment_capture": "1"  # Auto-capture payment
                })

            # Save the order for Razorpay
            order = orders(
                user=User,
                order_id=generate_order_id(),
                total_price=totalprice,
                discount = coupon_discount,
                discount_price = discount_price,
                payment_method=payment_method,
                shipping_address=shippingaddress,
                razorpay_order_id=razorpay_order['id']
            )
            order.save()
            if order.discount_price and order.discount_price <= 500:
                order.shipping_fees = shipping_fee
            elif int(order.total_price) <= 500:
                order.shipping_fees = shipping_fee
            order.save()
            for item in Cart_Item:
                order_item = order_items(
                    order=order,
                    product=item.product,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.price,
                    subtotal=item.item_total,
                )
                order_item.save()
                
                item.delete()

            # Prepare Razorpay data for frontend
            if order.discount != 0:
                totalprice = order.discount_price
            if order.shipping_fees:
                totalprice = totalprice + order.shipping_fees

            razorpay_data = {
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "razorpay_order_id": razorpay_order['id'],
                "total_price": totalprice,
                "user_email": User.email,
                "user_name": User.username
            }
            

            return render(request, 'razorpay_checkout.html', {'razorpay_data': razorpay_data})
        
        elif payment_method == 'Wallet':
            wallet = Wallet.objects.get(user = request.user)
            order = orders(
                user=User,
                order_id=generate_order_id(),
                total_price=totalprice,
                discount = coupon_discount,
                discount_price = discount_price,
                payment_method=payment_method,
                shipping_address=shippingaddress
            )
            
            order.save()
            if order.discount_price and order.discount_price <= 500:
                order.shipping_fees = shipping_fee
            elif int(order.total_price) <= 500:
                order.shipping_fees = shipping_fee
            order.save()
            names = []
            for item in Cart_Item:
                order_item = order_items(
                    order=order,
                    product=item.product,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.price,
                    subtotal=item.item_total,
                )
                order_item.save()
                Variant = variant.objects.get(id=item.variant.id)
                Variant.stock -= item.quantity
                Variant.save()
                names.append(item.product.name)
                item.delete()
            if order.discount_price :
                wallet.balance = wallet.balance - Decimal(order.discount_price)
                transaction_amount = order.discount_price
            else:
                wallet.balance = wallet.balance - Decimal(order.total_price)
                transaction_amount = order.total_price
            wallet.save()
            details = f"buy the products  {', '.join(names)}"
            transaction = Transaction(wallet = wallet,
                                  transaction_type = 'debit',
                                  amount = transaction_amount,
                                  balance_after = wallet.balance,
                                  details = details)
            transaction.save()
            order.payment_status = 'Success'
            order.save()
            

            return render(request, 'ordersuccess.html', {'order': order} )
       

        else:
            return redirect('checkout')

    else:
        return redirect('checkout')

from django.shortcuts import get_object_or_404
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        # Handle Razorpay webhook/response
        data = request.POST
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = get_object_or_404(orders, razorpay_order_id=razorpay_order_id)
        
        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Update the order as paid
            order = orders.objects.get(razorpay_order_id=razorpay_order_id)
            order.payment_status = 'Success'
            order.save()
            Order_items = order_items.objects.filter(order = order )
            for item in Order_items:
                Variant = variant.objects.get(id=item.variant.id)
                Variant.stock -= item.quantity
                Variant.save()

            return render(request, 'ordersuccess.html', {'order': order})
        except razorpay.errors.SignatureVerificationError:
            return render(request, 'ordersuccess.html', {'error': 'Payment testing verification failed.'})

    return redirect('checkout')
















































































































































































































from django.http import JsonResponse
import json

MAX_PURCHASE_LIMIT = 10  # Set purchase limit

def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        variant_id = data.get('variant_id')
        quantity = data.get('quantity')
        Variant = variant.objects.get(id = variant_id)
        # Get the current user's cart
        Cart = cart.objects.get(user=request.user)
            
            # Find the cart item based on the variant_id
        cart_item = CartItem.objects.get(Cart=Cart, variant_id=variant_id)


        if cart_item:
            # Check stock availability
            if quantity > cart_item.variant.stock:
                return JsonResponse({
                    'success': False,
                    'error': 'stock_limit',
                    'available_stock': cart_item.variant.stock
                })
            
            # Check purchase limit
            if quantity > MAX_PURCHASE_LIMIT:
                return JsonResponse({
                    'success': False,
                    'error': 'purchase_limit',
                    'purchase_limit': MAX_PURCHASE_LIMIT
                })
            
            # Update the quantity
            cart_item.quantity = quantity
            cart_item.item_total = cart_item.quantity * Variant.final_price
            cart_item.save()

            item_total = cart_item.variant.final_price * cart_item.quantity
            return JsonResponse({'success': True, 'item_total': float(item_total)})
    return JsonResponse({'success': False})


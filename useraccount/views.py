from django.shortcuts import render,redirect
from . models import user_address
from orders.models import orders
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import io
from reportlab.lib.pagesizes import letter


# Create your views here.

@login_required(login_url='user_login')
def my_account(request):
    User = request.user
    print(User.email)
    print(request.user.username)

    return render (request,'my_account.html',{'User' : User})


@login_required(login_url='user_login')
def edit_profile(request):
    User = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        User.username = username
        User.email = email
        User.phone_number = phone_number
        User.save()
        return redirect('my_account')
    else:
        return render(request,'edit-profile.html',{'User': User})

from django.core.paginator import Paginator

@login_required(login_url='user_login')
def order_list(request):
    user_orders = orders.objects.filter(user = request.user).order_by('-created_at')
    paginator = Paginator(user_orders,10)

    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'order-list.html',{'user_orders': page_obj})

@login_required(login_url='user_login')
def order_details(request,order_id):
    order = orders.objects.get(id = order_id)
    order_items = order.order_items.all()
    return render(request, 'order-details.html',{'order': order,'order_items': order_items})


@login_required(login_url='user_login')
def search_orders(request):
    query = request.GET.get('query', '').strip()
    if query:
        # Always apply filters to order_id (numeric or not)
        filters = (Q(order_id__icontains=query) | 
                   Q(order_status__icontains=query)
                  )

        # Add a filter for `total_price` only if the query is numeric
        if query.replace('.', '', 1).isdigit():
            filters |= Q(total_price=query)

        # Apply the combined filters
        result = orders.objects.filter(filters)
        result = orders.objects.filter(user = request.user).filter(filters).order_by('-created_at')
    
        return render(request, 'order-list.html',{'result': result}) 
    else:
        return render(request, 'order-list.html',{'none':'none'})


@login_required(login_url='user_login')
def User_address(request):
    Address = user_address.objects.filter(user_id = request.user.id)
    context = {'Address' : Address}
    print(request.user.id)
    return render (request,'address.html',context)

@login_required(login_url='user_login')
def add_address(request):
    if request.method == 'POST':
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
        return redirect('my_address')
    else:

        return render(request,'add-address.html')

@login_required(login_url='user_login')
def edit_address(request,address_id):
    Address = user_address.objects.get(id = address_id)

    if request.method  == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('zip')
        phone_number = request.POST.get('phone')

        Address.name = name
        Address.address = address
        Address.city = city
        Address.state = state
        Address.postal_code = postal_code
        Address.phone_number = phone_number
        Address.save()


        return redirect('my_address')

    else:
        return render(request,'add-address.html',{'Address' : Address})



@login_required(login_url='user_login')
def list_address(request,address_id):
    if request.method == 'POST':
        address = user_address.objects.get(id = address_id)
        if address.is_listed:
            address.is_listed = False
            address.save()
        else:
            address.is_listed = True
            address.save()
        return redirect('my_address')
    else:
        return redirect('my_address')
    


@login_required(login_url='admin_login')
def generate_pdf_report_views(request,order_id):
        Order = orders.objects.get(id = order_id)
        order_items = Order.order_items.all()
        return generate_pdf_reports(Order,order_items )
   


def generate_pdf_reports(orders,order_items):
    # Create a buffer to hold the PDF data
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Title and header section
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Order Invoice")
    c.setFont("Helvetica", 12)
    c.drawString(200, 730, f"Seaside Mobile Phones")
    c.drawString(200, 710, f"Email: seasidemobilephones@gmail.com")
    c.drawString(200, 690, f"Date: {orders.created_at.date()}")
    c.drawString(200, 670, f"Payment_Method: {orders.payment_method}")
    c.drawString(200, 650, f"Payment_Status: {orders.payment_status}")
    if orders.discount_price:
        c.drawString(200, 630, f"Total Price: {orders.total_price}")
        c.drawString(200, 610, f"Discounted Price: {orders.discount_price}")
    else:
        c.drawString(200, 630, f"Total Price: {orders.total_price}")


    
    

   

    # Table header
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 600, "Product")
    c.drawString(150, 600, "Quantity")
    c.drawString(250, 600, "Price")
    c.drawString(350, 600, "Sub Total")

    # Table data
    y_position = 580
    c.setFont("Helvetica", 10)
    for item in order_items:
        c.drawString(50, y_position, str(item.product.name))
        c.drawString(150, y_position, str(item.quantity))
        c.drawString(250, y_position, str(item.subtotal))
        c.drawString(350, y_position, str(item.price))
        y_position -= 20  # Move to the next line

    # Finalize and return the response
    c.showPage()
    c.save()
    buffer.seek(0)

    # Return PDF response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response


from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import never_cache
from products.models import category, product, variant, VariantImage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from products.models import Review
from orders.models import orders,order_items




# Create your views here.
@never_cache
def home(request):
    if request.user.is_authenticated :
        Filter =  request.GET.get('filterr')
        print(Filter)
        variants = variant.objects.select_related('product__category').prefetch_related('images').exclude(Q(is_listed=False) | Q(product__category__is_listed=False))
        categories = category.objects.all()
        if Filter:
            for  cat in categories:
                if Filter == cat.name:
                    variants = variant.objects.select_related('product__category').prefetch_related('images').filter(product__category = cat.id).exclude(Q(is_listed=False) | Q(product__category__is_listed=False))
                    if variants:
                        return render(request,'home.html',{'variants': variants,'categories': categories})
                    else:
                        return render(request,'home.html',{'categories': categories, 'Filter' : Filter})

        
        return render(request,'home.html',{'variants': variants,'categories': categories})
    return redirect('user_login')


def products(request):
    Filter =  request.GET.get('filterr')
    print(Filter)
    variants = variant.objects.select_related('product__category').prefetch_related('images').exclude(Q(is_listed=False) | Q(product__category__is_listed=False))
    categories = category.objects.annotate(product_count = Count('products'))
    if Filter:
            for  cat in categories:
                if Filter == cat.name:
                    variants = variant.objects.select_related('product__category').prefetch_related('images').filter(product__category = cat.id).exclude(Q(is_listed=False) | Q(product__category__is_listed=False))
                    return render(request,'products.html',{'variants': variants,'categories': categories})
    return render(request,'products.html',{'variants': variants,'categories': categories})

@login_required(login_url='user_login')
def product_details(request,product_id):
    Product = product.objects.get(id=product_id)   
    variants = variant.objects.filter(product__category=Product.category).prefetch_related(
        'images',  # Prefetch related images
        'product'  # Prefetch related product
    )
    reviews = Review.objects.filter(user = request.user,product = Product)
    relatedproducts = variants = variant.objects.filter(product__category=Product.category).prefetch_related('images','product').exclude(product_id = product_id).exclude(Q(is_listed=False) | Q(product__category__is_listed=False))
    

    Order_items = order_items.objects.filter(order__user = request.user,product_id = product_id)
    if Order_items:
        return render(request, 'product_details.html', {'products': Product,
                                                    'variants': variants,
                                                    'relatedproducts' : relatedproducts,
                                                    'reviews' : reviews,
                                                    'buyed' : 'buyed',
                                                    })
    else:
        return render(request, 'product_details.html', {'products': Product,
                                                    'variants': variants,
                                                    'relatedproducts' : relatedproducts,
                                                    'reviews' : reviews,
                                                    })



@login_required(login_url='user_login')
def search_product(request):
    query = request.GET.get('query', '').strip()
    categories = category.objects.all()
    print(query)
    if query:
        filters = (Q(product__name__icontains = query) | 
                   Q(product__brand_name__icontains = query) | 
                   Q(product__category__name__icontains = query) | 
                   Q(color__icontains = query) | 
                   Q(storage__icontains = query) | 
                   Q(RAM__icontains = query)
                   )
        if query.replace('.', '', 1).isdigit():
            filters |= Q(price=query)
        result = variant.objects.select_related('product__category').prefetch_related('images').filter(filters).exclude(Q(is_listed=False) | Q(product__category__is_listed=False))
        return render(request,'products.html',{'result': result,'categories': categories})
    else:
        variants = variant.objects.select_related('product__category').prefetch_related('images').exclude(Q(is_listed=False) | Q(product__category__is_listed=False))
        return render(request,'products.html',{'variants': variants,'categories': categories})
    
@login_required(login_url='user_login')
def product_sort(request):
    sort_option = request.GET.get('sort_list', 'new') 
    print(sort_option)
    categories = category.objects.all()
    if sort_option == 'price low high':
        result = variant.objects.select_related('product__category').prefetch_related('images').exclude(Q(is_listed=False) | Q(product__category__is_listed=False)).order_by('price')  # Ascending order by price
    elif sort_option == 'price high low':
        result = variant.objects.select_related('product__category').prefetch_related('images').exclude(Q(is_listed=False) | Q(product__category__is_listed=False)).order_by('-price')  # Descending order by price
    elif sort_option == 'A to Z':
        result = variant.objects.select_related('product__category').prefetch_related('images').exclude(Q(is_listed=False) | Q(product__category__is_listed=False)).order_by('product__name')  # Alphabetical order A-Z
    elif sort_option == 'Z to A':
        result = variant.objects.select_related('product__category').prefetch_related('images').exclude(Q(is_listed=False) | Q(product__category__is_listed=False)).order_by('-product__name')  # Reverse alphabetical order Z-A
    
        

    return render(request,'products.html',{'result': result,'categories': categories})
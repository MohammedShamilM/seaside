from django.shortcuts import render,redirect,get_object_or_404
from . models import category,product, variant, VariantImage,Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import variant
from django.core.paginator import Paginator





@login_required(login_url='admin_login')
def categories (request):
    if request.user.is_staff:
        categories = category.objects.all().order_by('id')
        paginator = Paginator(categories,7)

        page_number = request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        return render(request,'admin-category.html',{'categories':page_obj})
    else:
        return redirect('user_login')


@login_required(login_url='admin_login')
def add_category(request):
    if request.user.is_staff:
        if request.method == 'POST':
            catname = request.POST.get('categoryName')
            catdescription = request.POST.get('categoryDescription')
            if category.objects.filter(name = catname).exists():
                messages.error(request,"name already exists")
                return redirect('add_category')

            if not catname or not catdescription:
                messages.error(request, 'All fields are required.')
                return render(request, 'add-category.html')
        
            cat1= category(name = catname,description = catdescription)
            cat1.save()

            return redirect('admin_categories')

        
        return render(request,'add-category.html')
    else:
        return redirect('user_login')


@login_required(login_url='admin_login')
def edit_category(request,category_id):
    if request.user.is_staff:
        Category = category.objects.get(id = category_id)
        if request.method == 'POST':
            catname = request.POST.get('categoryName')
            catdescription = request.POST.get('categoryDescription')
            if category.objects.filter(name = catname).exists():
                messages.error(request,"name already exists")
                return redirect('edit_category',category_id)
            Category.name = catname
            Category.description = catdescription

            Category.save()
            return redirect('admin_categories')

        return render(request,'add-category.html',{'Category':Category})
    else:
        return redirect('user_login')




@login_required(login_url='admin_login')
def toggle_category_status(request, category_id):
    if request.user.is_staff:
        content = category.objects.get(id = category_id)
        if content.is_listed:
            content.is_listed = False
            content.save()
        else:
            content.is_listed = True
            content.save()
        return redirect('admin_categories') 
    else:
        return redirect('user_login')
    


@login_required(login_url='admin_login')
def products (request):
    if request.user.is_staff:
        variants = variant.objects.select_related('product__category').prefetch_related('images').order_by('id')
        paginator = Paginator(variants,7)

        page_number = request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        return render(request,'admin-product.html',{'variants': page_obj})
    else:
        return redirect('user_login')
    

@login_required(login_url='admin_login')
def toggle_product_status(request, variant_id):
    if request.user.is_staff:
        content = variant.objects.get(id = variant_id)
        if content.is_listed:
            content.is_listed = False
            content.save()
        else:
            content.is_listed = True
            content.save()
        return redirect('admin_products') 
    else:
        return redirect('user_login')


@login_required(login_url='admin_login')
def products_details(request,variant_id):
    if request.user.is_staff:
        variants = variant.objects.select_related('product__category').prefetch_related('images').get(id= variant_id)
        print(variants)
        return render(request, 'admin-product-details.html',{'variants': variants})
    else:    
        return redirect('user_login')


@login_required(login_url='admin_login')
def add_product(request):
    if request.user.is_staff:
        categories = category.objects.all()

        if request.method == 'POST':
            product_name = request.POST.get('productName')
            category_id = request.POST.get('category')
            description = request.POST.get('productDescription')
            brand = request.POST.get('brand')
            if not product_name or not category_id or not description or not brand:
                return render(request, 'add-product.html', {'categories': categories, 'error': 'All fields are required.'})

            if product.objects.filter(name = product_name).exists():
                messages.error(request,"product name already exists")
                return redirect('add_product')

            category_name = category.objects.get(id=category_id)
            products = product(name=product_name, description=description, category=category_name,brand_name=brand)
            products.save()

            return redirect('add_variant',product_id = products.id)

        return render(request, 'add-product.html', {'categories': categories})
    else:
        return redirect('user_login')



@login_required(login_url='admin_login')
def add_variant(request,product_id):
    if request.user.is_staff:
        Product = product.objects.get(id=product_id)
        if request.method == 'POST':
            color = request.POST.get('color')
            storage = request.POST.get('storage')
            ram = request.POST.get('RAM')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            offer = request.POST.get('Offer')

            if variant.objects.filter(color = color, storage = storage, RAM = ram).exists():
                messages.error(request,"The variant is existing")
                return redirect('add_variant',product_id)
            
            
            
            
            if offer:
                Variant = variant(
                        product=Product,
                        color=color,
                        storage=storage,
                        RAM = ram,
                        stock=stock,
                        price=price,
                        offer = offer
                )
            else:
                Variant = variant(
                        product=Product,
                        color=color,
                        storage=storage,
                        RAM = ram,
                        stock=stock,
                        price=price,

                )
            
            Variant.save()


            
            return redirect('add_variant_image',variant_id = Variant.id)

        return render (request,'add-variant.html')
    else:
        return redirect('user_login')






@login_required(login_url='admin_login')
def add_variant_image(request, variant_id):
    if request.user.is_staff:
        Variant = get_object_or_404(variant, id=variant_id)
        
        if request.method == 'POST':
            images = request.FILES.getlist('images')
            for image in images:
                # Save each image associated with this variant
                variant_image = VariantImage(variant=Variant, image=image)
                variant_image.save()
            return redirect('admin_products')  # Adjust redirect as needed

        return render(request, 'add-variant-image.html', {'variant': Variant})
    else:
        return redirect('user_login')




@login_required(login_url='admin_login')
def edit_product(request,product_id,variant_id):
    if request.user.is_staff:
        categories = category.objects.all()
        Product = product.objects.get(id = product_id)
        variants = variant.objects.get(id= variant_id)
        if request.method == 'POST':
            
            product_name = request.POST.get('productName')
            category_id = request.POST.get('category')
            description = request.POST.get('productDescription')
            brand = request.POST.get('brand')

            Category = category.objects.get(id = category_id)

            Product.name = product_name
            Product.category = Category
            Product.description = description
            Product.brand_name = brand

            Product.save()

            return redirect('edit_variant' ,variant_id)
        return render (request, 'add-product.html',{'Product' : Product,'categories': categories,'variants':variants})
    else:
        return redirect('user_login')
    


@login_required(login_url='admin_login')
def edit_variant(request,variant_id):
    if request.user.is_staff:
        Variant = variant.objects.get(id = variant_id)  
        if request.method == 'POST':
            color = request.POST.get('color')
            storage = request.POST.get('storage')
            ram = request.POST.get('RAM')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            offer = request.POST.get('Offer')

            Variant.product = Variant.product
            Variant.color = color
            Variant.storage = storage
            Variant.RAM = ram
            Variant.stock = stock
            Variant.price = price
            Variant.offer = offer

            
            Variant.save()
            return redirect('admin_products_details', variant_id = Variant.id)

        return render(request,'add-variant.html',{'Variant': Variant})
    else:
        return redirect('user_login')
        
def add_review(request, product_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            Product = get_object_or_404(product, id=product_id)

            if Review.objects.filter(product=Product, user=user).exists():
                messages.error(request, "You have already reviewed this product.")
                return redirect('products_details', product_id=product_id)

            rating = request.POST.get('rating')
            review = request.POST.get('review')


            if not rating or not rating.isdigit():
                messages.error(request, "Invalid rating. Please select a valid number.")
                return redirect('products_details', product_id=product_id)

            rating = int(rating)
            if rating < 1 or rating > 5:
                messages.error(request, "Rating must be between 1 and 5.")
                return redirect('products_details', product_id=product_id)

            if not review.strip():
                messages.error(request, "Review text cannot be empty.")
                return redirect('products_details', product_id=product_id)

            Review.objects.create(
                product=Product,
                user=user,
                rating=rating,
                review=review
            )

            messages.success(request, "Your review has been submitted successfully.")
            return redirect('products_details', product_id=product_id)

        return redirect('products_details', product_id=product_id)
    
    messages.error(request, "You need to Login.")
    return redirect('user_login')

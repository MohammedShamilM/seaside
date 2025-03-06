from django.shortcuts import render,redirect
from . models import wishlist,WhishlistItem
from products.models import variant,product, VariantImage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.
@login_required(login_url='user_login')
def Wishlist(request):
    User = request.user
    print(request.user)
    wishlistuser = wishlist.objects.get_or_create(user = User)
    Wishlistofuser = wishlist.objects.get(user = User)
    Wishlist_Item =  WhishlistItem.objects.filter(Wishlist = Wishlistofuser)
    paginator = Paginator(Wishlist_Item,3)

    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    return render (request,'wishlist.html',{'Wishlist_Item': page_obj})

@login_required(login_url='user_login')
def add_to_wishlist(request,variant_id):
    if request.user.is_authenticated:
        Variant = variant.objects.select_related('product').get(id = variant_id)
        images = VariantImage.objects.filter(variant = variant_id )
        img = images[0].image 
        
        if wishlist.objects.filter(user = request.user).exists():
            Wishlist = wishlist.objects.get(user = request.user)
        else:
            Wishlist = wishlist(user = request.user)
            Wishlist.save()
        if  WhishlistItem.objects.filter(Wishlist = Wishlist, variant = Variant).exists():
            return redirect('products_details',Variant.product.id)
        else:
            Wishlist_Item = WhishlistItem(Wishlist = Wishlist, variant = Variant, product = Variant.product, price = Variant.price, image = img )
            Wishlist_Item.save()
            return redirect('products_details',Variant.product.id)
        
    else:
        return redirect('products')

@login_required(login_url='user_login')
def remove_from_wishlist(request,variant_id):
    if request.user.is_authenticated:
        Variant = variant.objects.get(id = variant_id)
        Wishlist = wishlist.objects.get(user = request.user)
        Wishlist_Item = WhishlistItem.objects.get(Wishlist = Wishlist, variant = Variant)
        Wishlist_Item.delete()
        return redirect('wishlist')
    else:
        return redirect('user_login')
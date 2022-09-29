from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Order, Products,ProductCategory,WishList,Cart,ShippingAddress
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# storeView for home page
def storeView(request):
    products=Products.objects.all()
    categories=ProductCategory.objects.all()
    if request.user.is_authenticated:
        item_count=WishList.objects.filter(customer=request.user).count()
        cart_count=Cart.objects.filter(customer=request.user).count()
        context={'products':products,'categories':categories,'item_count':item_count,'cart_count':cart_count}
    else:    
        context={'products':products,'categories':categories}    
    return render(request,'store/home.html',context)

# for shop 
def shopView(request):
    products=Products.objects.all()
    if request.user.is_authenticated:
        item_count=WishList.objects.filter(customer=request.user).count()
        cart_count=Cart.objects.filter(customer=request.user).count()
        context={'products':products,'item_count':item_count,'cart_count':cart_count}
    else:
        context={'products':products}    

    return render(request,'store/shop.html',context)

# for category view
def categoryView(request,id):
    name=ProductCategory.objects.get(id=id).category
    products=Products.objects.filter(category=id)
    if request.user.is_authenticated:
        item_count=WishList.objects.filter(customer=request.user).count()
        cart_count=Cart.objects.filter(customer=request.user).count()
        context={'products':products,'name':name,'item_count':item_count,'cart_count':cart_count}
    else:
        context={'products':products,'name':name}    
    return render(request,'store/category.html',context)

# for login page
def LoginView(request):
    if request.method == 'POST':
        username=User.objects.get(email=request.POST['email']).username
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('store')
        else:
            return HttpResponse('Invalid Credentials')    
    context={}
    return render(request,'store/user_login.html',context)

# for logout 
def LogoutView(request):
    logout(request)
    return redirect('store')

# registration view
def RegisterView(request):
    if request.user.is_authenticated==False:
        if request.method == 'POST':
            form=RegistrationForm(request.POST)
            if User.objects.filter(email=request.POST['email']):
                return HttpResponse('this email already used')
            if form.is_valid():
                form.save()
                # return  HttpResponse('user created successfully')
                messages.success(request,'user created successfully')
                return redirect('login')
        else:
            form=RegistrationForm()            
        context={}    
        return render(request,'store/user_register.html',context)
    else:
        return redirect('store')
@login_required
def UpdateProfileView(request):
    cart_count=Cart.objects.filter(customer=request.user).count()
    item_count=WishList.objects.filter(customer=request.user).count()
    if request.method == 'POST':
        username=request.POST['username']
        if request.POST['old_password']:
            old_password=request.POST['old_password']
            user=authenticate(username=request.user,password=old_password)
            if user:
                user.username=username
                new_password=request.POST['new_password']
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Updated Successfully')
                return redirect('login')
            else:
                return HttpResponse('old password is wrong')    
        else:
            email=request.user.email
            user=User.objects.get(email=email) 
            user.username=username
            user.save()
            # print(user.username)
            messages.success(request,'Username Updated Successfully')
            return redirect('store')   
    context={'cart_count':cart_count,'item_count':item_count}
    return render(request,'store/update_profile.html',context)

# for About page
def AboutView(request):
    if request.user.is_authenticated:
        item_count=WishList.objects.filter(customer=request.user).count()
        cart_count=Cart.objects.filter(customer=request.user).count()
        context={'item_count':item_count,'cart_count':cart_count}
    else:
        context={}    
    return render(request,'store/about.html',context)    

# for contact page
def ContactView(request):
    if request.user.is_authenticated:
        item_count=WishList.objects.filter(customer=request.user).count()
        cart_count=Cart.objects.filter(customer=request.user).count()
        context={'item_count':item_count,'cart_count':cart_count}
    else:
        context={}    
    return render(request,'store/contact.html',context)   

# for detail of product
def QuickView(request,id):
    product=Products.objects.get(id=id)
    if request.user.is_authenticated:
        item_count=WishList.objects.filter(customer=request.user).count()
        cart_count=Cart.objects.filter(customer=request.user).count()
        context={'product':product,'item_count':item_count,'cart_count':cart_count}
    else:
        context={'product':product}    
    return render(request,'store/quick_view.html',context)   

# for search by product name
def SearchView(request):
    if request.method == 'POST':
        name=request.POST['search_box']
        products=Products.objects.filter(name__icontains=name)
        if request.user.is_authenticated:
            item_count=WishList.objects.filter(customer=request.user).count()
            cart_count=Cart.objects.filter(customer=request.user).count()
            context={'products':products,'item_count':item_count,'cart_count':cart_count}
        else:
            context={'products':products}
    else:
        if request.user.is_authenticated:
            item_count=WishList.objects.filter(customer=request.user).count()
            cart_count=Cart.objects.filter(customer=request.user).count()
            context={'item_count':item_count,'cart_count':cart_count}
        else:
            context={}        
    return render(request,'store/search_page.html',context)


# for add item in wish list
@login_required
def AddWishListView(request):
    
    if request.method == 'POST':
        customer=request.user
        product_id=Products(request.POST['product_id'])
        if WishList.objects.filter(customer=customer,product_id=product_id):
            messages.success(request,'Product already added')
            return redirect('store')
        else:
            wishlist=WishList.objects.create(customer=customer,product_id=product_id)
            item_count=WishList.objects.filter(customer=customer).count()
            context={'item_count':item_count}
            return redirect('store')
    context={}        
    return render(request,'store/navbar.html',context) 


# for show wish list items
@login_required
def WishListView(request):
    products=WishList.objects.filter(customer=request.user)
    item_count=WishList.objects.filter(customer=request.user).count()
    cart_count=Cart.objects.filter(customer=request.user).count()
    context={'products':products,'item_count':item_count,'cart_count':cart_count}
    return render(request,'store/wishlist.html',context)    

@login_required
def DeleteFromWishList(request):
    if request.method =='POST':
        if request.POST['delete']:
            product_id=request.POST['product_id']
            customer=request.user
            product=WishList.objects.get(product_id=product_id,customer=customer)
            product.delete()  
            return redirect('wishlist')
    return render(request,'store/wishlist.html',{})  


@login_required
def AddCartView(request):
    if request.method == 'POST':
        customer=request.user
        product_id=Products(request.POST['product_id'])
        quantity=request.POST['quantity']
        if Cart.objects.filter(customer=customer,product_id=product_id):
            # return HttpResponse('Product Already Added in Cart')
            messages.info(request,'Product already added')
            return redirect('store')
        else:
            Cart.objects.create(customer=customer,product_id=product_id,quantity=quantity)
            cart_count=Cart.objects.filter(customer=customer).count()
            print(cart_count)
            context={'cart_count':cart_count}
            messages.success(request,'Product Added to your Cart')
            return redirect('store')
    context={}
    return render(request,'store/navbar.html',context) 

@login_required
def CartListView(request):
    products=Cart.objects.filter(customer=request.user)
    cart_count=Cart.objects.filter(customer=request.user).count()
    item_count=WishList.objects.filter(customer=request.user).count()
    grand_total= sum([item.quantity* item.product_id.price for item in products])
    context={'products':products,'cart_count':cart_count,'item_count':item_count,'grand_total':grand_total}
    return render(request,'store/cart.html',context)

@login_required
def DeleteCartView(request):
    if request.method == 'POST':
        customer=request.user
        if request.POST.get('delete'):
            product_id=request.POST['product_id']
            product=Cart.objects.get(customer=customer,product_id=product_id)
            product.delete()
            return redirect('cartlist')
        if request.POST.get('all_delete'):
            products=Cart.objects.filter(customer=customer)
            products.delete()
            print(products)
            return redirect('cartlist')
    return render(request,'store/cart.html')        


@login_required
def UpdateQuantityView(request):
    if request.method == "POST":
        customer=request.user
        product_id=request.POST['product_id']
        quantity=request.POST['quantity']
        product=Cart.objects.get(customer=customer,product_id=product_id)
        product.quantity=quantity
        product.save()
        return redirect('cartlist')
            
    return render(request,'store/cart.html')           


@login_required
def CheckoutView(request):
    cart_count=Cart.objects.filter(customer=request.user).count()
    item_count=WishList.objects.filter(customer=request.user).count()
    products=Cart.objects.filter(customer=request.user)
    grand_total= sum([item.quantity* item.product_id.price for item in products])
    context={'grand_total':grand_total,'cart_count':cart_count,'item_count':item_count,'products':products}
    return render(request,'store/checkout.html',context)


@login_required
def OrderPlaceView(request):
    if request.method == 'POST':
        customer=request.user
        payment_mode=request.POST['method']
        name=request.POST['name']
        mobile_no=request.POST['mobile_no']
        email=request.POST['email']
        address_line1=request.POST['address1']
        address_line2=request.POST['address2']
        city=request.POST['city']
        state=request.POST['state']
        pincode=request.POST['pincode']
        country=request.POST['country']
        ShippingAddress.objects.create(customer=customer,
                                       name=name,
                                       mobile_no=mobile_no,
                                       email=email,
                                       address_line1=address_line1,
                                       address_line2=address_line2,
                                       city=city,
                                       state=state,
                                       pincode=pincode,
                                       country=country 
                                      )
        products=Cart.objects.filter(customer=customer)
        for item in products:
            Order.objects.create(customer=customer,
                                 payment_mode=payment_mode,
                                 product_id=item.product_id,
                                 quantity=item.quantity    
                                )
        items=Cart.objects.filter(customer=customer)
        items.delete()                        
        messages.success(request,'Order Placed')
        return redirect('order_detail')
    return render(request,'store/checkout.html',{})

@login_required
def OrderView(request):
    cart_count=Cart.objects.filter(customer=request.user).count()
    item_count=WishList.objects.filter(customer=request.user).count()
    orders=Order.objects.filter(customer=request.user)
    if ShippingAddress.objects.filter(customer=request.user).exists(): 
        order=orders[0]
        addresses=ShippingAddress.objects.filter(customer=request.user)
        address=addresses[len(addresses)-1]
        shipped_address=", ".join(
                                [str(address.address_line1),
                                address.address_line2,
                                address.city,
                                address.state,
                                str(address.pincode),
                                address.country
                                ]
                                )
        total_price=sum([item.product_id.price * item.quantity  for item in orders])
        context={'order':order,'address':address,'shipped_address':shipped_address,'orders':orders,'total_price':total_price,'cart_count':cart_count,'item_count':item_count}
    else:
        context={'order':0,'cart_count':cart_count,'item_count':item_count}    
    return render(request,'store/order.html',context)

def MSG(request):
    messages.success(request,'hello sachin')
    return render(request,'store/hello.html')    
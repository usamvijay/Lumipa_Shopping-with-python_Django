import random
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from six import ensure_binary
from hashlib import md5
from .models import Catagories, Products,User_data, Add_to_Cart, Orders_items, Order
from SiteApp import models
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views h21ere.

def isAlreadyLogin(request):
    if request.session.has_key('user_email') and request.session.has_key('user_role') and request.session.has_key('user_id'):
        return True
    return False

# -----Index Page view -----

def index(request):
    cat = Catagories.objects.all()
    if 'serch' in request.GET:
        serch =  request.GET['serch']
        items = Products.objects.filter(Product_name__icontains = serch)
    else:
        items = Products.objects.all()

    return render(request, 'site/index-4.html', {'item':items, 'cat':cat} )

# -----User Registration Page view -----

def User_Register_page(request):
    return render(request, 'site/Register.html' )


# -----User Login Page View -----

def User_Login_page(request):
    return render(request, 'site/Login.html' )  
    return render(request,'site/header.html', {'cat':catagory })


def product_details_page(request, id):
    
    Items   =    Products.objects.filter(id = id)
    rel     =    Products.objects.get(id = id)
    Related_items = Products.objects.filter(cat = rel.cat).exclude(id = id)

    return render(request, 'site/product_details_page.html', {'item':Items, 'Related': Related_items } )

# -----Shop Page View  -----

def shop_page(request):
    if isAlreadyLogin(request):
        Catagory    =   Catagories.objects.all()
        CATID       =   request.GET.get('catagory')
        if CATID:
            product =   Products.objects.filter(cat_id = CATID)
        else:
            product =   Products.objects.all()
        
        context = {
            'Catagory':Catagory,
            'product':product,
        }    
        return render(request, 'site/shop_page.html', { 'catagory':Catagory,'items':product } )
    else:
        return HttpResponseRedirect('/site/Login')

# -----Cart Page View -----

def cart_page(request):
    if isAlreadyLogin(request):
        Get_user    =   User_data.objects.get(email = request.session['user_email'])
        Cart_items  =   Add_to_Cart.objects.filter(user = Get_user.id)
        total_price =   0
        for item in Cart_items:
            total_price = total_price + item.Product.descount_price * item.Qty
        return render(request, 'site/cart_page.html', {'cart':Cart_items, 'total':total_price } )
    else:
        return HttpResponseRedirect('site/customer_login')

# -----User Adding Data -----

def User_Register_Data(request):
    if request.method == 'POST':
        if models.User_data.objects.filter(email =  request.POST['email']).exists():

             messages.warning(request, " Youre Email is Alredy Exists...")
             return HttpResponseRedirect('/site/Register')
        else:
            if request.POST['pass'] == request.POST['Cpass']:
                User    =   models.User_data()

                User.firstname   =   request.POST['firstname']
                User.lastname    =   request.POST['lastname']
                User.email       =   request.POST['email']
                User.mobile      =   request.POST['mobile']
                User.password    =   md5(ensure_binary(request.POST['pass'])).hexdigest()
                User.save()
                messages.warning(request, " Youre Register succuessfully... Login Now ")
                return HttpResponseRedirect('/site/User_login')
            else:
                messages.warning(request, " Password & Confirm Password Must Be Same ")
                return HttpResponseRedirect('/site/Register')
    return render(request, 'site/Register.html')

# -----User Login from Hare.. -----

def User_Login(request):
    if isAlreadyLogin(request):
        return HttpResponseRedirect('/site/shop_page/')
    elif request.method == 'POST':
        email    = request.POST['email']
        password = md5(ensure_binary(request.POST['pass'])).hexdigest()
        if models.User_data.objects.filter(email=email, password=password).exists():
            user = models.User_data.objects.get(email=email)
            request.session['user_email'] = email
            request.session['user_role']  = 'user'
            request.session['user_id']    = user.id
            return HttpResponseRedirect('/site/shop_page/')
        else:
            messages.info (request, "Invalid Email or Password")
            return redirect('/site/Login/')
    else:
        return redirect('/site/Login/')

# -----UserLogout from Hare -----

def User_logout(request):
    try:
        del request.session['user_email']
        del request.session['user_role']
    except:
        pass
    return HttpResponseRedirect('/site/index/')

# -----Adding Cart Items From Hare -----

def adding_cart_items(request):
    if isAlreadyLogin(request):
        
        if request.method == "POST":
            User    =  request.session['user_email']
            User1   =  User_data.objects.get(email = User)
            User_id =  User1.id
            
            Cart    =  models.Add_to_Cart()
            Cart.user_id = User_id
            
            Cart.Product_id     = request.POST['product_id']
            Qty                 = request.POST['qty']
            cart_total_price    = 0
            price = request.POST['price']
            
            total_price      = cart_total_price + int(price) * int(Qty)
            Cart.total_price = total_price
            Cart.Qty         = Qty
            Cart.save()
            messages.success(request, "Item Added To Cart Successfully")
            return HttpResponseRedirect('/site/cart_page')
        else:
            return HttpResponseRedirect('site/index')
    else:
        return HttpResponseRedirect('/site/Login')   

# -----Checkout Products From Hare -----

def checkout_page(request):
    Get_user    =   User_data.objects.get(email = request.session['user_email'])
    Cart_items  =   Add_to_Cart.objects.filter(user = Get_user.id)
    total_price =   0
    for item in Cart_items:
        total_price = total_price + item.Product.descount_price * item.Qty
        
    return render(request, 'site/checkout.html', { 'items':Cart_items , 'total':total_price})


def order_items(request):
    if request.method == "POST":
        Get_user =  User_data.objects.get(email = request.session['user_email'])
        user1    =   Get_user.id
        order    =   models.Order()
        order.user_id        =  user1
        order.firstname      =  request.POST['firstname']
        order.lastname       =  request.POST['lastname']
        order.cumpany_name   =  request.POST['company_name']
        order.address        =  request.POST['address']
        order.appartment     =  request.POST['landmark']
        order.city           =  request.POST['city']
        order.state          =  request.POST['state']
        order.Zip_code       =  request.POST['Zip']
        order.mobile         =  request.POST['number']
        order.email          =  request.POST['email']
        order.payment        =  request.POST['payment']

        trac_no              = 'PV'+str(random.randint(111111, 9999999999999))
        while Order.objects.filter(tracing_number = trac_no ) is None:
            trac_no           = 'PV'+str(random.randint(111111, 9999999999999))
        order.tracing_number  =  trac_no
        order.save()

        cart = Add_to_Cart.objects.filter(user = user1)
        for item in cart:
            Orders_items.objects.create(
                user_id        =   Get_user.id,
                product        =   item.Product,
                price          =   item.Product.descount_price,
                Quantity       =   item.Qty,
                tracing_number =   trac_no

            )
            orderproduct = Products.objects.filter(id = item.Product_id).first()
            orderproduct.Qty = orderproduct.Qty - item.Qty
            orderproduct.save()

        Add_to_Cart.objects.filter(user = user1 ).delete()

    messages.info(request, "Order Succuss...")
    return HttpResponseRedirect('/site/orders')
            
def order_invoice(request):
    user = User_data.objects.get(email= request.session['user_email'])
    item_order = Order.objects.filter(user = user.id)
    OrderItem = Orders_items.objects.filter(user_id = user.id)[0:1]
    return render(request, 'site/order_invoice.html',{'order':item_order, 'item':OrderItem})


def my_orders(request):
    user    =   User_data.objects.get(email= request.session['user_email'])
    order   =   Orders_items.objects.filter(user = user.id).order_by('-id')
    null    =   Orders_items.objects.filter(user = user.id)
    total_price =0
    for O in null:
        lat = total_price + int(O.price) * int(O.Quantity)
        print( lat )
    return render(request,'site/my_orders.html', {'orders':order, 'total':lat})

# //////-----Profile page -----///////

def user_profile(request):
    if request.session['user_email']:
        user     =  request.session['user_email']
        user1    =  User_data.objects.filter(email=user )
        return render(request, 'site/user_profile.html',{ 'profile':user1 })
    else:
        return HttpResponseRedirect( 'site/index')


# -----Delete Cart Items from Hare -----

def remove_cart_items(request, id):
    cart_item   =   Add_to_Cart.objects.get(id = id)
    cart_item.delete()
    messages.info(request, "Your Cart item Deleted...")
    return HttpResponseRedirect('/site/cart_page')

# -----Update User Prifle from Hare -----

def update_user_data(request, id):
    if request.method == 'POST':

        profile             =   models.User_data.objects.get(id = id)
        profile.firstname   =   request.POST.get('firstname')
        profile.lastname    =   request.POST.get('lastname')
        profile.email       =   request.POST.get('email')
        profile.mobile      =   request.POST.get('mobile')
        profile.save()
        messages.warning(request, " Profile Updated succuessfully... ")
        return HttpResponseRedirect('/site/profile')
            
    else:           
        user = User_data.objects.filter(id = id)
        return render(request, 'site/update_user.html', {'user':user })

# -----User Password Change from Hare -----

def User_password_change(request, id):
    if request.method   ==  "POST":
        user     =   User_data.objects.get(id = id)

        if md5(ensure_binary(request.POST['Old_pass'])).hexdigest() == user.password:
            if request.POST['New_pass'] == request.POST['C_New_pass']:
                user.password = md5(ensure_binary(request.POST['New_pass'])).hexdigest()
                user.save()
                messages.info(request, 'Password changed success')
                return HttpResponseRedirect('/site/profile/')
            
            else:
                messages.info(request, 'Password and Confirm Password must be same')
                return HttpResponseRedirect('/site/profile/')
        else:           
          messages.info(request, 'Enter Valide Old Password')
          return HttpResponseRedirect('/site/profile/')

    else:
        user =User_data.objects.filter(id= id)
    return render(request, 'site/change_password.html', {'user':user})

  
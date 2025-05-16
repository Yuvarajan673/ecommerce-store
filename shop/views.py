from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json


def home(request):
    products=Product.objects.filter(trending=1)
    return render(request, "index.html",{"products":products})




def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "cart.html",{"cart":cart})
    else:
        return render(request, "cart.html")



def profileimage(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('fileinput')
        if profile_picture:
            profile = UserProfile.objects.get_or_create(user=request.user,userid=request.user.id)[0]
            profile.profile_picture = profile_picture
            profile.save()
            messages.success(request,"Profile Updated Successfully")
            return redirect('/')  # Redirect to profile view after successful upload
        else:
            messages.error(request,"Please Select The Image")
            return redirect('/')





def proimgremove(request):
    photo = get_object_or_404(UserProfile)
    filepath = photo.profile_picture.path
    photo.delete()
    if os.path.exists(filepath):
        os.remove(filepath)
    messages.success(request,"Profile Image Removed Successfully")
    return redirect('/')





def remove_cart(request,cid):
     cartitem = Cart.objects.get(id=cid)
     cartitem.delete()
     return redirect("/cart")




@csrf_protect
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body.decode('utf-8'))
                product_qty = data.get('product_qty')
                product_id = data.get('pid')
                #print(request.user.id)
                product_status = Product.objects.get(id=product_id)
                if product_status:
                    if Cart.objects.filter(user=request.user.id, product_id=product_id):
                        return JsonResponse({'status': 'Product Already In Cart'}, status=200)
                    else:
                        if product_status.quantity >= product_qty:
                            Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                            return JsonResponse({'status': 'Product Added To Cart Successfully'}, status=200)
                        else:
                            return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
                
            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON data'}, status=400)

        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)

    


@csrf_protect
def loginpage(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user:
                login(request,user)
                messages.success(request,"Logged In Successfully")
            else:
                messages.error(request,"Invalid Username or Password")
    return redirect("/")




def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully")
    return redirect("/")




@login_required
def repass(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)  # Assuming you want to reset the password for the currently logged-in user
        newpass = request.POST.get('password1')
        conpass = request.POST.get('password2')

        if newpass == conpass:
            user.set_password(newpass)
            user.save()
            messages.success(request, "Password Changed Successfully")
        else:
            messages.error(request, "Passwords Do Not Match")

    return redirect('/')




@csrf_protect
def registration(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 == pass2:
            user = User.objects.create_user(username=uname,email=email,password=pass1)
            messages.success(request,"Registered Successfully You Can Login Now")
        else:
            messages.error(request, "Password Did Not Match")


    return render(request, 'index.html')





def categories(request):
    category=Category.objects.filter(status=0)
    return render(request, "collections.html",{"category":category})





def products(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name )
        return render(request, "products.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"No Such Catagory Found")
        return redirect('categories')




def pdetails(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"pdetails.html",{"products":products,"category_name":cname})
            
        else:
            messages.error(request,"No Such Product Found")
            return redirect('categories') 
    else:
        messages.error(request,"No Such Catagory Found")
        return redirect('categories') 
    

from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payments.forms import ShippingForm
from payments.models import ShippingAddress
#from django.contrib.auth.models import User

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

# Create your views here.
def search(request):
	# Determine if they filled out the for
    if request.method == "POST":
        searched = request.POST['searched']
        #query the result
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})

def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
        # Get Current User's Shipping Info 
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
        # Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #did they fill out the form
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            #is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been changed...")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, "update_password.html")
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Profile Updated Successfully!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You Must be Logged in to Access This Page!")
        return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password )
        if user is not None:
            login(request, user)

            #do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #get their saved cart from database
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)

                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("You've successfully logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("Something went wrong!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered successfully!"))
            return redirect('home')
        else:
            messages.success(request, ("There was a problem registering, please try again..."))
            return redirect('home')
    return render(request, 'register.html', {'form':form})

def product_user(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request, foo):
    #replace hyphens with spaces
    foo = foo.replace("-", " ")
    #grab the category from the url
    try:
        #look up the category
        category = Category.objects.get(name=foo)
        product = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':product, 'category':category})
    except:
        messages.success(request, ("Sorry, that category doesn't exist!"))
        return redirect('home')
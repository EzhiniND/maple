
import json
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.contrib.auth import logout  # Import the logout function




 
# Define a view function for the home page
@login_required
def home(request):
  return render(request, 'home.html', {'username': request.user.username}) 
# Define a view function for the login page
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)  # Use auth_login instead of login
            return redirect('/products/')
    
    return render(request, 'login.html')
# Define a view function for the registration page
def register(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
         
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
         
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
         
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
         
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')
     
    # Render the registration page template (GET request)
    return render(request, 'register.html')

@login_required
def product_list(request):
    selected_category = request.GET.get('category')
    selected_subcategory = request.GET.get('subcategory')

    categories = Category.objects.values_list('category', flat=True).distinct()
    subcategories = []

    if selected_category:
        subcategories = Category.objects.filter(category=selected_category).values_list('subcategory', flat=True).distinct()

    products = Category.objects.all()

    if selected_category:
        products = products.filter(category=selected_category)
    if selected_subcategory:
        products = products.filter(subcategory=selected_subcategory)

    return render(request, 'product.html', {
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
        'products': products,
        'username': request.user.username
    })

def search_products(request):
    query = request.GET.get('query', '')
    products = Category.objects.filter(
        Q(product_name__icontains=query) | Q(description__icontains=query)
    ) if query else Category.objects.all()

    return render(request, 'product.html', {'query': query, 'products': products})


@login_required
def add_to_cart(request, product_name):
    if request.method == 'POST':
        try:
            product = Category.objects.get(product_name=product_name)
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return redirect('cart')
        except Category.DoesNotExist:
            # Handle case where product doesn't exist
            return redirect('product_list')  # Redirect to a relevant page, e.g., product list
    return redirect('product_list')  
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price,'username': request.user.username})



def remove_from_cart(request, product_name):
    product = get_object_or_404(Category, product_name=product_name)
    cart_item = get_object_or_404(CartItem, product=product)
    cart_item.delete()
    return redirect('cart')


def submit_order(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        email=request.POST.get('email','')
        phone_number = request.POST.get('phoneNumber', '')
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items:
            return redirect('cart')  # Return to cart if empty

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create an order
        order = Order.objects.create(
            user=request.user,
            email=email,
            name=name,
            address=address,
            phone_number=phone_number,
            total_price=total_price
        )

        # Associate cart items with the order
        order.items.set(cart_items)
        order.save()

        # Send confirmation email
        subject = "New Order Confirmation"
        message = f"Name: {name}\nemail:{email}\nphone_number:{phone_number}\nAddress:{address} \n\nyour order has been placed successfully.\n\nCart Details:\n"
        for item in cart_items:
          message += f"Product: {item.product.product_name} - Quantity: {item.quantity}\n"

# Add total price to the message
        message += f"\nTotal Price: Rs. {total_price}"
        from_email = 'ezhinind@gmail.com'  # Update with your email address
        to_email = 'plasticsrmp@gmail.com' 
# Send the confirmation email
        send_mail(subject, message, from_email, [to_email])

        # Optionally, clear the cart
        cart_items.delete()

        return redirect('order_confirmation')  # Assuming you have an 'order_confirmation' view

    return redirect('cart')
def order_confirmation(request):
    return render(request,"order_confirmation.html")


def log_out(request):
    logout(request)  # Logout the user
    return redirect('login')  # Redirect to the login page

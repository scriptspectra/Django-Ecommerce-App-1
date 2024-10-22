from django.shortcuts import render, redirect
from cart.cart import Cart
from payments.forms import ShippingForm, PaymentForm
from payments.models import ShippingAddress, Order, OrderItem
from store.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime
# Import some paypal stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # unique user id for duplicate orders

# Create your views here.
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == "true":
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('shipped_dash')
        return render(request, "payments/orders.html", {"order":order, "items":items})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

"""def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if True or False
            if status == "true":
                # Get the Order
                order = Order.objects.filter(id=pk)
                order.update(shipped=True, date_shipped=datetime.datetime.now())
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, "Shipping Status updated!")
            return redirect('shipped_dash')

        return render(request, "payments/orders.html", {"order":order, "items":items})
    else:
         messages.success(request, "Access Denied!")
         return redirect('home')"""

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        not_shipped_orders = Order.objects.filter(shipped=False)
        shipped_orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Check if true or false
            if status == "true":
                # Get the order
                order = Order.objects.filter(id=num)
                # Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # Get the order
                order = Order.objects.filter(id=num)
                # Update the status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('shipped_dash')


        return render(request, "payments/shipped_dash.html", {"not_shipped_orders":not_shipped_orders, "shipped_orders":shipped_orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def payment_success(request):
    return render(request, "payments/payment_success.html", {})

def payment_failed(request):
    return render(request, "payments/payment_failed.html", {})

def billing_info(request):
    if request.POST:
		#get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantites = cart.get_quants
        totals = cart.cart_total()
          
		#create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
          
        # Get the host
        host = request.get_host()

        # Create paypal form dictionary
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name': 'Order',
            'no_shipping': '2',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': 'https://{}{}'.format(host, reverse("paypal-ipn")),
            'return_url': 'https://{}{}'.format(host, reverse("payment_success")),
            'cancel_return': 'https://{}{}'.format(host, reverse("payment_failed"))
        }

        # Create actual paypal form
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

		#check to see if the user is logged-in
        if request.user.is_authenticated:
			# if logged-in
            billing_form = PaymentForm()
            return render(request, "payments/billing_info.html", {"paypal_form":paypal_form, "cart_products":cart_products, "quantities":quantites, "totals": totals, "shipping_info":request.POST, "billing_form":billing_form})
        else:
			# if not logged-in
            billing_form = PaymentForm()
            return render(request, "payments/billing_info.html", {"paypal_form":paypal_form, "cart_products":cart_products, "quantities":quantites, "totals": totals, "shipping_info":request.POST, "billing_form":billing_form})

        shipping_form = request.POST
        return render(request, "payments/billing_info.html", {"cart_products":cart_products, "quantities":quantites, "totals": totals, "shipping_info":request.POST, "billing_form":billing_form})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        # Get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # Get shipping session data
        my_shipping = request.session.get('my_shipping')

        # Gather order info
        user = request.user
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid = totals
        
        # Create the shipping address
        shipping_address = f"{my_shipping['shipping_address_1']}\n{my_shipping['shipping_address_2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"

        if request.user.is_authenticated:
            user = request.user
            # Create order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk

            # Get the product info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get the product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the session key
                    del request.session[key]

            # Delete cart from database
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete the shopping cart in database
            current_user.update(old_cart="")

            messages.success(request, "Order placed successfully!")
            return redirect('home')
        else:
            create_order = Order(user=None, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
			
			# Get the order ID
            order_id = create_order.pk
			
			# Get product Info
            for product in cart_products():
			    # Get product ID
                product_id = product.id
				# Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

				# Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
						# Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=None, quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the session key
                    del request.session[key]


            messages.success(request, "Order placed successfully!")
            return redirect('home')

    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    shipping = cart.shipping_fee()
    grand_total = cart.grand_total()

    if request.user.is_authenticated:
        #checkout as a logged-in user
        #shipping user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        #shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "checkout.html", {"cart_products":cart_products,"quantity":quantities, "totals":totals, "shipping":shipping, "grand_total":grand_total, "shipping_form":shipping_form})
    else:
        #checkout as a guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "checkout.html", {"cart_products":cart_products,"quantity":quantities, "totals":totals, "shipping":shipping, "grand_total":grand_total, "shipping_form":shipping_form})
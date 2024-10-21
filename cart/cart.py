from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        #Get the current session key if it exists
        cart = self.session.get('session_key')

        #If the user is new, no session ke! So, create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #Make sure cart is available
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_quantity = str(quantity)

        #logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price: ': str(product.price)}
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

                #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #{'2':3, '4':2} to {"2":3, "4":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the Profile model
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)

        #logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price: ': str(product.price)}
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

                #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #{'2':3, '4':2} to {"2":3, "4":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the Profile model
            current_user.update(old_cart=str(carty))


    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        #use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # get the cart
        our_cart = self.cart
        #update dictionary
        our_cart[product_id] = product_qty

        self.session.modified = True
        thing = self.cart

        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #{'2':3, '4':2} to {"2":3, "4":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the Profile model
            current_user.update(old_cart=str(carty))

        return thing
    
    def delete(self, product):
        product_id = str(product)

        #delete from dictionary
        if product_id in self.cart:
            del self.cart[product_id]   

        self.session.modified = True
        
        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #{'2':3, '4':2} to {"2":3, "4":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the Profile model
            current_user.update(old_cart=str(carty))


    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                     total = total + (product.sale_price * value)
                    else:
                     total = total + (product.price * value)
        return total
    
    def shipping_fee(self):
        tot = self.cart_total()
        shipping_fee = (tot / 4)
        return shipping_fee
    
    def grand_total(self):
        grand_total = self.cart_total() + self.shipping_fee()
        return grand_total
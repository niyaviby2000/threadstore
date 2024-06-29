from django.shortcuts import render,redirect

# Create your views here.

from store.forms import SignUpForm,SignInForm

from django.views.generic import View

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from store.models import Product,BasketItem,Size,Basket,Order

class RegistrationView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            # data=form_instance.cleaned_data

            # User.objects.create_user(**data)

            return redirect("register")
        
        return render(request,"register.html",{"form":form_instance})


class LoginView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            print(user_object)

            if user_object:

                login(request,user_object)

                print("success")

                return redirect("index")
            
        print("failed")
        
        return render(request,"login.html",{"form":form_instance})

class IndexView(View):

    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        return render(request,"index.html",{"data":qs})
    
    
# localhost:8000/products/{id}/

class ProductDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Product.objects.get(id=id)

        return render(request,"product_detail.html",{"data":qs})


# localhost:products/{id}/carts/add/

class AddToCartView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        size_name=request.POST.get("size")

        qty=request.POST.get("qty")

        # basket_item_object

        basket_obj=request.user.cart

        size_obj=Size.objects.get(name=size_name)

        # created basketitem to show in cart=>to add in cart

        BasketItem.objects.create(

            basket_object=basket_obj,

            product_object=product_obj,

            size_object=size_obj,

            quantity=qty,

        )

        print("item added to cart")

        # print(product_obj,size_obj,qty)

        return redirect("index")
    
class CartSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitems.filter(is_order_placed=False)

        return render(request,"cart_items.html",{"data":qs})


# localhost:8000/basketitem/{id}/remove

class CartItemDestroyView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItem.objects.get(id=id).delete()

        return redirect("cart-summary")
    
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    
class CartQuantityUpdateView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        basket_item_obj=BasketItem.objects.get(id=id)

        action=request.POST.get("action")

        if action=="increment":

            basket_item_obj.quantity+=1

        else:

            basket_item_obj.quantity-=1

        basket_item_obj.save()
        

        # print(action)

        return redirect("cart-summary")


class PlaceOrderView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"place_order.html")

    def post(self,request,*args,**kwargs):

        email=request.POST.get("email")

        phone=request.POST.get("phone")

        delivery_address=request.POST.get("address")

        payment_mode=request.POST.get("payment_mode")

        pin=request.POST.get("pin")

        user_obj=request.user

        cart_item_objects=request.user.cart.cartitems.filter(is_order_placed=False).order_by("-created_date")

        if payment_mode=="cod":

            order_obj=Order.objects.create(

                user_object=user_obj,

                delivery_address=delivery_address,

                phone=phone,

                pin=pin,

                email=email,

                payment_mode=payment_mode,

            )

            for bi in cart_item_objects:

                order_obj.basket_item_objects.add(bi)

                bi.is_order_placed=True

                bi.save()
            
            order_obj.save()

        print(email,delivery_address,phone,pin,payment_mode)

        return redirect("index")
    
class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"order_summary.html",{"data":qs})




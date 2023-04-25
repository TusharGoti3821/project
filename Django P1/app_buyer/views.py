from django.shortcuts import render
from app_buyer.models import *
from app_seller.models import *
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.db.models import Q

# Create your views here.
# session_user_data = User.objects.get(request.session['email'])
def index(request):
    try:
        request.session['email']
        session_user_data = User.objects.get(request.session['email'])
    except:
        return render(request,"index.html")
def register(request):
    if request.method == "POST":
        try:
            User.objects.get(email= request.POST['email'])
            return render(request,"register.html",{'msg':"user already exist"})
        except:
            if request.POST["pass"]==request.POST["cpass"]:
                global temp
                temp = {
                    'fname':request.POST["fname"],
                    'email':request.POST["email"],
                    'pass':make_password(request.POST["pass"])
                }
                global votp
                votp=random.randint(100000,999999)
                subject = 'EVIB ECOMMERCE OTP VERIFICATION MAIL'
                message = f'YOUR OTP IS  {votp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'],]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,"otp.html")
            else:
                return render(request,"register.html",{'msg':"password and confirm password is not match"})
    else:
        return render (request,"register.html")
    
def about(request):
    return render (request,"about.html")

def otp(request):
    if request.method=="POST":
        if votp == int(request.POST['OTP']):
            User.objects.create(
                fullname = temp['fname'],
                email = temp['email'],
                password = temp['pass']
            )
            return render(request,"login.html",{'msg':'Registraion Sucessfully'})
        else:
            return render (request,"otp.html",{'msg':'OTP is INCORRECT'})
    else:
        return render(request,"otp.html")
    

def login(request):
    if request.method == "POST":
        try:
            user_data=User.objects.get(email= request.POST['email'])
            if check_password(request.POST["pass"],user_data.password):
                request.session['email']=request.POST['email']
                request.session['name']=user_data.fullname
                session_user_data = User.objects.get(email=request.session['email'])
                return render(request, "index.html",{"session_user_data":session_user_data})
            else:
                return render(request,"login.html" , {"msg":"password is incorrect"})
        except:
            return render(request,"login.html" , {"msg":"you email is not register"})
    else:
        return render(request,"login.html")
        



def forgot_password(request):
    if request.method == "POST":
        try:
            user_data=User.objects.get(email= request.POST["email"])
            request.session['e_email']=request.POST["email"]
            global votp
            votp=random.randint(100000,999999)
            subject = 'EVIB ECOMMERCE OTP VERIFICATION MAIL'
            message = f'YOUR OTP IS  {votp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'],]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,"forgot_otp.html")
        except:
            return render(request,"forgot_password.html", {"msg":"your email is not register please register first"})
    else:
        return render (request,"forgot_password.html")
    

def reset_password(request):
    if request.method == "POST":
        if request.POST["pass"]==request.POST["cpass"]:
            user_data=User.objects.get(email=request.session['e_email'])
            user_data.password=make_password(request.POST["pass"])
            user_data.save()
            return render(request,"homepage.html",{'msg':'password reset Sucessfully'})
        else:
        
            return render(request,"reset_passeord",{"msg":"password not match"})
    else:
        return render(request,"reset_password.html")
    

    

def forgot_otp(request):
    if request.method=="POST":
        if votp == int(request.POST['OTP']):
            return render(request,"reset_password.html",{'msg':'Registraion Sucessfully'})
        else:
            return render (request,"forgot_otp.html",{'msg':'OTP is INCORRECT'})
    else:
        return render(request,"forgot_otp.html")
    


def profile(request):
    try:
        request.session['email']
        session_user_data = User.objects.get(email=request.session['email'])
        user_data=User.objects.get(email=request.session['e_email'])
        if request.method=="POST":
            if request.POST['pass']:
                if check_password(request.POST['opass'],user_data.password):
                    if request.POST['pass']==request.POST['cpass']:
                        user_data=User.objects.get(email=request.session['email'])
                        user_data.fullname=request.POST['fname']
                        user_data.password=make_password (request.POST['pass'])
                        try:
                            request.FILES['propic']
                            user_data.profilepic=request.FILES['propic']
                            user_data.save()
                        except:
                            user_data.save()
                        return render(request,"profile.html",{"user_data":user_data,"msg":"profile updated succsefully!","session_user_data":session_user_data})
                    else:
                        user_data=User.objects.get(email=request.sessinon['email'])
                        return render(request,"profile.html",{"user_data":user_data,"msg":"password and confirm password not match","session_user_data":session_user_data})
                else:
                    return render(request,"profile.html",{"user_data":user_data,"msg":"old pass not match","session_user_data":session_user_data })
            else:
                user_data=User.objects.get(email=request.session['email'])
                user_data.fullname=request.POST['fname']
                try:
                    request.FILES['propic']
                    user_data.profilepic=request.FILES['propic']
                    user_data.save()
                except:
                    user_data.save()

                
                return render(request,"profile.html",{"user_data":user_data,"msg":"profile updated succsefully!","session_user_data":session_user_data })
        else:
            user_data=User.objects.get(email=request.session['email'])
            return render(request,"profile.html",{"user_data":user_data,"session_user_data":session_user_data})
    except:
        return render(request,"index.html")
    
def logout(request):
    try:
        request.session['email']
        del request.sesson['email']
        return render (request, "index.html")
    except:
        return render (request,"index.html")
    

def view_product(request):
    request.session['email']
    session_user_data = User.objects.get(email=request.session['email'])
    product_data=Add_Product.objects.all()
    return render (request,'view_product.html',{"product_data":product_data,"session_user_data":session_user_data})

def product_description(request,pk):
    try:
        request.session['email']
        session_user_data = User.objects.get(email=request.session['email'])
        user_data=User.objects.get(email=request.session['e_email'])
        session_user_data = User.objects.get(email=request.session['email'])
        single_product = Add_Product.objects.get(id=pk)
        return render (request,'product_description.html',{"single_product":single_product,"session_user_data":session_user_data,"session_user_data":session_user_data,"user_data":user_data})
    except:
        return render(request,"index.html")

def add_to_cart(request,pk):
    try:
        request.session['email']
        session_user_data = User.objects.get(email=request.session['email'])
        user_data=User.objects.get(email=request.session['email'])
    
        if request.method == "POST":
            usr = User.objects.get(email=request.session['email'])
            try:
                cart_exist =Cart.objects.get(product=pk, user=usr)
                cart_exist.quantity = cart_exist.quantity+1
                cart_exist.total=int(cart_exist.quantity) * int(cart_exist.product.price)
                cart_exist.save()
            except:
                prod = Add_Product.objects.get(id=pk)
                Cart.objects.create(
                    product=prod,
                    user=usr,
                    quantity=1,
                    total = prod.price

                )
            single_product=Add_Product.objects.get(id=pk)
            return render (request,'product_description.html',{"single_product":single_product,"session_user_data":session_user_data,"msg":'add sucessfully'})
    except:
        return render (request,"index.html")

def view_cart(request):
    try:
        request.session['email']
        session_user_data = User.objects.get(email=request.session['email'])
        user_data=User.objects.get(email=request.session['email'])
        user_data = User.objects.get(email=request.session['email'])
        total_cart = Cart.objects.filter(user=user_data)
        final_total=0
        for i in total_cart:
            final_total+=i.total
        return render(request,"cart.html",{"total_cart":total_cart,"final_total":final_total,"session_user_data":session_user_data})
    except:
        return render(request,"index.html") 
    
def search(request):
    if request.method == "POST":
        query= request.POST['ser']
        product_data=Add_Product.objects.filter( Q(pname__icontains=query) | Q(description__icontains=query))
        session_user_data = User.objects.get(email=request.session['email'])
        return render (request,'view_product.html',{"product_data":product_data,"session_user_data":session_user_data})

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()



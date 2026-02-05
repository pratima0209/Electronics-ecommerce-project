from django.shortcuts import render,redirect
from AdminApp.models import Category,Electronics,Payment
from UserApp.models import UserInfo,MyCart,OrderMaster
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail,EmailMultiAlternatives
import random

# Create your views here.

# Home Page 
def home(request):
    electronics = Electronics.objects.all()
    return render(request,'master.html',{'electronics':electronics})

# Method for cart count
def cartCount(request): 
    cart = 0
    if("uname" in request.session):
        cart = MyCart.objects.filter(user= request.session["uname"]).count()
    return {"cart":cart}

# Item search Method
def search(request):
    q = request.GET['q']
    electronics = Electronics.objects.filter(item_name__icontains = q)
    return render(request,'search.html',{'electronics':electronics})

# contactUs mehtod
def contactUs(request):
    if (request.method == "GET"):
        return render(request,"contactUs.html",{})
    else:
        subject = request.POST["subject"]

        # we will use this mail-id to send the email
        from_email = 'pratimaladkat9@gmail.com' # add user email address to send email

        # this is customers email but here its local host so our sender email is from_email above
        email = request.POST['email']  

        # our message with complaint or enquiry
        message = request.POST['message']

        # at this end our mail will be recived
        to = email

        # sending mail here
        msg = EmailMultiAlternatives(subject,message,from_email,[to])
        msg.content_subtype = 'html'
        msg.send()

        messages.success(request,"Your mail was recieved at our end, you will be soon contacted by our executive, Have a great day Thank You!")
        return render(request,"yourAccount.html",{})
        
        
# Available Products Method
def Products(request,id):
    prod = Category.objects.get(id = id)
    electronics= Electronics.objects.filter(category = id)
    return render(request,'Products.html',{"electronics":electronics,"prod":prod})

# Specific Product Orientation
def getGadjets(request,id):
    # fetching electronic id from Electronics Model
    electronics = Electronics.objects.get(id = id)
    try:
        # fetching cart item with user name and electronic id from MyCart Model
        itemIn_Cart = MyCart.objects.get(user = request.session["uname"],electronics = id)
    except:
        return render(request,"getGadjets.html",{"electronics":electronics})
    else:
        return render(request,"getGadjets.html",{"electronics":electronics,"itemIn_Cart":itemIn_Cart})
        

# Login Method
def masterLogin(request):
    if request.method == "GET":
        return render(request, 'masterLogin.html', {})
    else:
        # global email
        email = request.POST['email']
        # password = request.POST.get('password')
        # print(email)
        try:
            # Fetching email fro UserInfo Model
            user = UserInfo.objects.get(email = email) 
            # print(user)
        except:
            messages.error(request, 'Invalid email was entered')
            return render(request, 'masterLogin.html', {})
        else:
            subject = 'OTP for Logging in your Mini Electronics account'

            # we will use this mail-id to send the email
            from_email = 'pratimaladkat9@gmail.com' # add user email address to send email

            # this is customers email 
            # mail = email
            
            # OTP gerneration using random library
            otp_gen = random.randint(100000,999999)
            
            # Making a global variable for otp validatioon in different method
            global man_otp
            man_otp = otp_gen

            # our message with Otp for customer
            message = str(otp_gen) + ''' is your verification code to log in to your
            Mini electronics account. Please DO NOT SHARE this code with anyone.'''

            # at this end our mail will be recived
            to = email

            # sending mail here
            msg = EmailMultiAlternatives(subject,message,from_email,[to])
            msg.content_subtype = 'html'
            msg.send()
            request.session["email"] = email
            return render(request,"OTP.html",{"user":user})


# Otp validation
def Otp(request):
    val_otp =  request.POST['otp']
    if (int(val_otp) == man_otp):
        user = UserInfo.objects.get(email = request.session["email"])
        request.session["uname"] = user.user_name
        return redirect(home)
    else:
        messages.error(request,"OTP was incorrect")
        return render(request,"OTP.html",{})

def Resend(request):
    subject = 'OTP for Logging in your Mini Electronics account'

    # we will use this mail-id to send the email
    from_email = 'pratimaladkat9@gmail.com' # add user email address to send email

    # OTP gerneration using random library
    otp_gen = random.randint(100000,999999)
    global man_otp
    man_otp = otp_gen

    # our message with Otp for customer
    message = str(otp_gen) + ''' is your verification code to log in to your
    Mini electronics account. Please DO NOT SHARE this code with anyone.'''

    # at this end our mail will be recived
    to = request.session["email"]

    # sending mail here
    msg = EmailMultiAlternatives(subject,message,from_email,[to])
    msg.content_subtype = 'html'
    msg.send()
    messages.success(request,"OTP was sent successfully, check your email")
    return render(request,"OTP.html",{})


# SignUP Method
def masterSignUp(request):
    if (request.method == "GET"):
        return render(request,"masterSignUp.html")

    else:
        uname = request.POST['uname']
        zip_code = request.POST['zip_code']
        mob_no = request.POST['Mobile']
        email = request.POST['email']
        address = request.POST['address']
        try:
            # This will check for username and email in the same row in database
            user = UserInfo.objects.get(user_name = uname)

        except:
            # Suppose anyone is using another user name but the same email  
            dup_mail = UserInfo.objects.filter(email = email).count()
            if (dup_mail >= 1):
                messages.error(request,f'You indicated you are a new customer, but an account already exists with the email {email}')
                return render(request,"masterSignUp.html",{})
            else:
                user = UserInfo(uname,zip_code,mob_no,address,email)
                user.save()
                messages.success(request, 'Your Account was created, Sign in to your account here.')
                return redirect(masterLogin)
        else:
            messages.error(request,'This user name is not available, try creating account with different user name')
            return render(request,"masterSignUp.html",{})

# Add to cart method
def addToCart(request):
    if ("uname" in request.session):
        user = UserInfo.objects.get(user_name = request.session['uname'])
        gadjet_id = request.POST['eid']
        electronics = Electronics.objects.get(id = gadjet_id)
        # Adding Item in cart
        cart = MyCart()
        cart.user = user
        cart.electronics = electronics   
        cart.save()
        return redirect(showCart_Item)
       
    else:
        return redirect(masterLogin)

# method to show cart items
def showCart_Item(request):
    if(request.method == "GET"):
        items = MyCart.objects.filter(user = request.session['uname'])
        total = 0
        quant = 0
        for item in items:
            total += item.electronics.price * item.qty
            quant += item.qty
        request.session['total'] = total
        request.session['quant'] = quant

        return render(request,'showCart_Item.html',{'items':items,'total':total})
    else:
        cart_id = request.POST['cart_id']
        item = MyCart.objects.get(id = cart_id)
        qty = request.POST['qty']
        item.qty = qty
        item.save()
        return redirect(showCart_Item)

# method for cart_item deletion
def deleteCart_item(request,id):            
    item = MyCart.objects.get(id = id)
    item.delete()
    return redirect(showCart_Item)

# method for payment
def makePayment(request):
    if(request.method == "GET"):
        return render(request,"makePayment.html",{})
    else:
        card_no = request.POST["card_no"]
        cvv_no = request.POST["cvv_no"]
        expiry = request.POST["expiry_date"]
        try:
            buyer = Payment.objects.get(card_no = card_no,cvv=cvv_no,expiry=expiry)
        except:
            messages.error(request,"Your card details was incorrect")
            return render(request,"makePayment.html",{})
        else:
            owner = Payment.objects.get(card_no="1122334455667788",cvv="212",expiry="12/2026")
            buyer.balance -= float(request.session["total"])
            owner.balance += float(request.session["total"])
            buyer.save()
            owner.save()
           
            # for maintaining shopping history
            myOrder = OrderMaster()
            user = UserInfo.objects.get(user_name = request.session["uname"])
            myOrder.user = user
            myOrder.amount = request.session["total"]
            # fetching details from Cart
            items = MyCart.objects.filter(user = user)

            details = ""
            for item in items:
                details += item.electronics.item_name +" \n "
                item.delete()
            
            myOrder.details = details
            myOrder.order_id = random.randint(100000,999999)
            myOrder.qty = request.session["quant"]
            myOrder.save()

            info = UserInfo.objects.filter(user_name = request.session["uname"])
            return render(request,'orderStatus.html',{"info":info})

# Customer order details 
def orderDetails(request):
    items = OrderMaster.objects.filter(user= request.session["uname"]).order_by('-id')
    info = UserInfo.objects.get(user_name = request.session["uname"])
    return render(request,'orderDetails.html',{"items":items,"info":info})

# Customer Account
def yourAccount(request):
    if("uname" in request.session):
        return render(request,'yourAccount.html',{})
    else:
        return redirect(masterLogin)

# method for address edit
def address(request):
    items = UserInfo.objects.get(user_name = request.session["uname"])
    if(request.method == "GET"):
        return render(request,"address.html",{"items":items})
    else:
        address = request.POST['address']
        mobile_no = request.POST['mob_no']
        zip_code = request.POST['zip_code']
        items.address = address
        items.mobile_no = mobile_no
        items.zip_code = zip_code
        items.save()
        messages.success(request,'Your address and phone number was updated successfully!')
        return render(request,'yourAccount.html',{})

def cancleOrder(request,id):
    order = OrderMaster.objects.get(id = id)
    return render(request,"requestCancelation.html",{"order":order})

def requestCancelation(request,id):
    order = OrderMaster.objects.get(id = id)

    # getting deatails of customer for refund
    buyer = Payment.objects.get(card_no= "2233445566778899",cvv="112",expiry="12/2026")
    owner = Payment.objects.get(card_no="1122334455667788",cvv="212",expiry="12/2026")
    owner.balance -= float(order.amount)
    buyer.balance += float(order.amount)
    buyer.save()
    owner.save()
    
    # changing order status
    order.orderStatus = "This order was canceled"
    order.save()
    messages.success(request,"Your order was canceled successfully, your refund will be reflected in your account quickly!")
    return render(request,"yourAccount.html",{})


# user making changes in login and password credentials
def login_And_Security(request):
    # object of UserInfo model
    user_info = UserInfo.objects.get(user_name = request.session["uname"])
    if (request.method == "GET"):
       return render(request,'loginAndSecurity.html',{"user_info":user_info})
    else:
        # name = request.POST['name']
        mail = request.POST['eamil']
        # user_info.user_name = name
        user_info.email = mail
        user_info.save()
        
        # Updating MyCart model with new user_name as is foreign key of the UserInfo Model
        # cart = MyCart.objects.filter(user = request.session["uname"])
        # for items in cart:
        #     items.user = user_info
        #     items.save()

        # Updating orderMaster model with new user_name as is foreign key of the UserInfo Model
        # order = OrderMaster.objects.filter(user = request.session["uname"])
        # for items in order:
        #     items.user = user_info
        #     items.save()
        
        # creating session for updated user_name
        
        # request.session["uname"] = user_info.user_name
        messages.success(request,'Your email was updated successfully, Sign in with your updated email')
        request.session.clear()
        return redirect(masterLogin)

# checking login credentials again to validate
def login(request):
    if (request.method == "GET"):
        return render(request,"login.html",{})
    else: 
        mail = request.POST['email']
        # password = request.POST['password']
        if (mail == request.session["email"]):
            try:
                items = UserInfo.objects.get(email = mail)
            except:
                messages.error(request,'Invalid email was entered')
                return render(request,"login.html",{})
            else:
                return redirect(login_And_Security)
        else:
            messages.error(request,'Invalid email was entered, try again')
            return redirect(yourAccount)


# Sign Out
def SignOut(request):
    if ("uname" in request.session):
        request.session.clear()
    return redirect(masterLogin)
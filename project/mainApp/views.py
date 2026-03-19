from django.shortcuts import render , redirect
from .models import *
from django.core.exceptions import ValidationError
from os import name
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from decimal import Decimal
import tensorflow as tf
from .Utils import Utils




def get_user_by_username(username):
    try:
        user = User.objects.get(name=username)
        return user
    except User.DoesNotExist:
        return None
def get_order_by_username(username):
    try:
        order = Order.objects.filter(userName=username).values()
        return order
    except User.DoesNotExist:
        return None

############################################################################
#########################    LOGIN FUNCTIONS   #############################
############################################################################
############################################################################
def index_type_admin(request):
    user = get_user_by_username(request.session['username'])
    return render(request, 'mainApp/orders.html', {'user': user})

def index_type_user(request):
    user = get_user_by_username(request.session['username'])
    return render(request, 'mainApp/index.html', {'user': user})


def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password') 
        user = get_user_by_username(username)
        if user is not None and user.password == password:
            request.session['username'] = user.name
            if user.admin:
                return redirect('index_type_admin')
            else:
                return redirect('index_type_user')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request , 'mainApp/login.html')

def logout(request):
    del request.session['username']
    return render(request , 'mainApp/index.html')

def register(request):
    if request.method == 'POST': 
        username=request.POST.get('name')
        if User.objects.filter(name=username).exists():
            messages.error(request, "Username is already taken.")
        password=request.POST.get('password')
        address=request.POST.get('address')
        governname=request.POST.get('governorate')
        data=User(name=username,password=password,address=address,govername=governname)
        data.save()
        return redirect('login')
    return render(request , 'mainApp/register.html')
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################

############################################################################
#########################    SERVICES FUNCTIONS   ##########################
############################################################################
############################################################################

# model we ->
def sound(request):
    if not('username' in request.session) :
        return redirect('login')
    if request.method == 'POST':
        if 'sound' in request.FILES:
            s = request.FILES["sound"]
            soundFile = SoundFile(sound = s)
            soundFile.save()
            sound_path = soundFile.sound.path

            model_path = r"D:\collage\4_IT\graduation project\FarmerGuide_web\project\mainApp\AI_models\my_model.h5"
            model = Utils.load_keras_model(model_path)
            
            mel_path = Utils.generate_mel_spectrogram_image(sound_path)

            insectType = Utils.predict_keras_sound(model , mel_path)

            return render(request, 'mainApp/soundModel.html' , {'insectType' : insectType})
        else:
            print("no file uploaded")
            return render(request, 'mainApp/soundModel.html', {'error': 'No file uploaded'})

    return render(request , 'mainApp/soundModel.html')

# tree + svm


def soil(request):
    if not('username' in request.session) :
        return redirect('login')
    if request.method == 'POST':

        n = request.POST.get('nitrogin')
        p = request.POST.get('phosphorus')
        k = request.POST.get('potassium')

        model_path = r'D:\collage\4_IT\graduation project\FarmerGuide_web\project\mainApp\AI_models\svm_model.joblib'
        scaler_path = r'D:\collage\4_IT\graduation project\FarmerGuide_web\project\mainApp\AI_models\svm_scaler.joblib'
        encoder_path = r'D:\collage\4_IT\graduation project\FarmerGuide_web\project\mainApp\AI_models\label_encoder.joblib'
        crop = Utils.SVM_model_load_predict( model_path, scaler_path , encoder_path , n , p , k)

        print(crop)

        return render(request , 'mainApp/soilModel.html' , {'crop' : crop})
        # the model output
    return render(request , 'mainApp/soilModel.html')



def image(request):
    if not('username' in request.session) :
        return redirect('login')
    if request.method == 'POST':
        if 'image' in request.FILES:
            image = request.FILES["image"]
            ImageUpload.objects.create(image=image)
            latest_image = ImageUpload.objects.latest('uploaded_at')

            disease_model_path = r"D:\collage\4_IT\graduation project\FarmerGuide_web\project\mainApp\AI_models\Used_Model.h5" # change

            disease_model = Utils.load_keras_model(model_path=disease_model_path)

            # change if needed
            LABELS = {
                0: "CitrusScab",
                1: "Corn_DownyMildew",
                2: "Grape_DownyMildew",
                3: "Grape_PowderyMildew",
                4: "Pepper_PowderyMildew"
            }

            result = Utils.predict_keras(disease_model, latest_image.image.path) # ex [0, 0, 1, 0, 0]

            diseasename = Utils.map_result_to_label(result, LABELS)
            print(diseasename)

            try:
                disease = Disease_Treatment.objects.get(diseaseName = diseasename)
                return render(request, 'mainApp/imageModel.html' , {'disease' : disease})
            except Products_Inventory.DoesNotExist:
                messages.error(request , "We have no treatment for this disease")
                print("no disease")
                return render(request, 'mainApp/imageModel.html', {'diseasename' : diseasename})
        else:
            print("no file uploaded")
            return render(request, 'mainApp/imageModel.html', {'error': 'No file uploaded'})
    return render(request, 'mainApp/imageModel.html')



def segment(request):
    if not('username' in request.session) :
        return redirect('login')
    else:
        print("loged in ")
        percentage_disease = 100
        if request.method == 'POST':
            print("POST")
            if 'image' in request.FILES:
                image = request.FILES["image"]
                ImageUpload.objects.create(image=image)
                latest_image = ImageUpload.objects.latest('uploaded_at')
                print("image")
                
                percentage_disease = Utils.detect_disease_with_background_removal_and_contrast_enhancement(latest_image.image.path)
                print(percentage_disease)

                return render(request, 'mainApp/SegmentationModel.html', {'percentage_disease' : percentage_disease})
            else:
                print("nothing there")
                return render(request, 'mainApp/SegmentationModel.html', {'error': 'No file uploaded'})
        return render(request, 'mainApp/SegmentationModel.html')


def makeOrder(request , proID):
    try:
        pro = Product.objects.get(productid = proID)
        proname = pro.name
        proprice = pro.price
        neworder = Order(productid = proID , productName = proname , productprice = proprice)  
        neworder.save()  
        request.session['orID'] = neworder.id
        print("making order")
        return redirect('order')
    except Product.DoesNotExist:
        print("We have no treatment for this disease")
        # messages.error(request , "We have no treatment for this disease")
def cancelOrder(request , orderID):
    try:
        order = Order.objects.get(id = orderID)  
        order.delete()  
        return render(request, 'mainApp/imageModel.html')
    except Order.DoesNotExist:
        print("We have no treatment for this disease")
        # messages.error(request , "We have no treatment for this disease")
    return render(request, 'mainApp/imageModel.html')
def order(request):
    try:
        myorder = Order.objects.get(id = request.session['orID'])
        if request.method == 'POST':
            orderID=request.session['orID']
            pronum=request.POST.get('pronum')
            user = get_user_by_username(request.session['username'])
            username = user.name
            usergovern = user.govername
            try:
                order = Order.objects.get(id = orderID)
                proprice = order.productprice
                product_num = int(pronum)
                print(pronum)
                total = product_num*proprice
                order.productNum = product_num
                order.totalPrice = total
                order.userName = username
                order.userGovernorate = usergovern
                order.save()  
                del request.session['orID']
                return redirect('my_orders')
            except Product.DoesNotExist:
                print("We have no treatment for this disease")
                # messages.error(request , "We have no treatment for this disease")
    except Order.DoesNotExist:
        pass
    return render(request, 'mainApp/order.html' , {'orderr' : myorder})
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################

############################################################################
#########################    USER FUNCTIONS     ############################
############################################################################
############################################################################
def index(request):
    return render(request , 'mainApp/Index.html')

def my_orders(request):
    order = Order.objects.filter(userName=request.session['username']).values()
    template = loader.get_template('mainApp/my_orders.html')
    context = {
        'order': order,
    }
    return HttpResponse(template.render(context, request))

def edit(request):
    user = get_user_by_username(request.session['username'])
    if request.method == 'POST':
        username=request.POST.get('name')
        if User.objects.filter(name=username).exists():
            messages.error(request, "Username is already taken.")
        password=request.POST.get('password')
        address=request.POST.get('address')
        governname=request.POST.get('governorate')
        user.name=username
        user.password=password
        user.address=address
        user.govername=governname
        user.save()
    return render(request , 'mainApp/edit.html' , {'user': user} )
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################


############################################################################
#########################    ADMIN FUNCTIONS     ############################
############################################################################
############################################################################
def orders(request):
    user = get_user_by_username(request.session['username'])
    mydata = Order.objects.filter(accepted=False , userGovernorate = user.govername).values()
    # template = loader.get_template('orders.html')
    context = {
        'orders': mydata,
    }
    return render(request , 'mainApp/orders.html' , context)
    # return HttpResponse(template.render(context, request))

def accept_order(request , id):
    user = get_user_by_username(request.session['username'])
    order = Order.objects.get(id = id)
    try:
        product = Products_Inventory.objects.get(inventoryID = user.inventoryID , productName = order.productName)
        if product.productnum >= order.productNum:
            order.accepted = True
            order.adminName = user.name
            order.adminAddress = user.address
            order.save()
            product.productnum -= order.productNum
            product.save()
        else:
            messages.error(request , "This product is out of stock")
    except Products_Inventory.DoesNotExist:
        messages.error(request , "This product does not exist in your Inventory")
    return HttpResponseRedirect(reverse('orders'))

def orders_accepted(request):
    mydata = Order.objects.filter(accepted=True , adminName = request.session['username']).values()
    # template = loader.get_template('orders.html')
    context = {
        'orders': mydata,
    }
    return render(request , 'mainApp/orders_accepted.html' , context)


def inventory(request):
    user = get_user_by_username(request.session['username'])
    mydata = Products_Inventory.objects.filter(inventoryID=user.inventoryID).values()
    context = {
        'products': mydata,
    }
    return render(request , 'mainApp/inventory.html' , context)
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################

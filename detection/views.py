from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.http import HttpResponse
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import os
import pandas as pd
import pickle
import io
from django.conf import settings

# Load model once
model_path = os.path.join(settings.BASE_DIR, 'detection', 'brain_tumor_detection_model.h5')
model = tf.keras.models.load_model(model_path)
IMG_SIZE = (150, 150)

def home_view(request):
    return render(request, 'base.html')

def predict_image(request):
    prediction = None

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        img = image.load_img(io.BytesIO(uploaded_image.read()), target_size=IMG_SIZE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        result = model.predict(img_array)[0][0]
        prediction = "No Tumor" if result > 0.5 else "Tumor Detected"
        #return redirect('predict',prediction)
        return redirect('predict', prediction=prediction) 
    return render(request,'predict.html')

    #return render(request, 'predict.html', {'prediction': prediction})
def predict(request,prediction):
    print("DEBUG — prediction received:", prediction)
    return render(request,'output.html',{'prediction':prediction})

def calculator(request):
    result = None
    if request.method == 'POST':
        a = int(request.POST.get("num1"))
        b = int(request.POST.get("num2"))
        op = request.POST.get("oper")
        if op == "add":
            result = a + b
        elif op == "sub":
            result = a - b
        elif op == "mult":
            result = a * b
        elif op == "div":
            result = a / b
        else:
            return render(request, 'home.html', {'error': "Invalid operator"})
        return redirect('hello',result)
    return render(request, 'home.html')

def hello(request, result):
    return render(request, 'result.html', {'result': result})
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        passwor = request.POST.get('password')
        user = authenticate(request,username = username,password=passwor)
        if user is not None:
            login(request,user)
            return redirect('home_page')
        else:
            return render(request,'login.html',{'error':'InvalidUser'})
    return render(request,'login.html')
def home_page(request):
    return render(request,'base.html')
def logout_page(request):
    logout(request)
    return redirect('login_page')
def register_page(request):
    if request.method=='POST':
        username=request.POST.get('name')
        password=request.POST.get('password')
        conpass=request.POST.get('conform_password')
        if password!=conpass:
              return render(request,'register.html',{'error':'error'})
        user = User.objects.create_user(username = username,password=password)
        return redirect('login_page')
    return render(request,'register.html')
def test(request):
    report = None
    if request.method == 'POST':
        model_path = os.path.join(settings.BASE_DIR, 'detection', 'model.pkl')
        scaler_path = os.path.join(settings.BASE_DIR, 'detection', 'scaler.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            ms = pickle.load(f)
        features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        values = [float(request.POST.get(feat)) for feat in features]
        user_input = pd.DataFrame([values], columns=features)
        scaled_input = ms.transform(user_input)
        ans = model.predict(scaled_input)
        report="Diabetes" if ans[0] == 1 else "No Diabetics"
        return redirect('decision',report=report)
    return render(request,'check.html')
def decision(request,report):
    return render(request,'report.html',{'report':report})


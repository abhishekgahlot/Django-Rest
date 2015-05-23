from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest.models import ApiTokens
from libs.api_func import api_token, verify_token, check_email
import datetime
# Rest Endpoints

"""
Rest Endpoints for User

user/signup
user/login
user/logout
user/{id} (to get and update user data)
user/ (save user data)

"""

"""
I am using AES 128 bit for encrypting, probably i can also use Hmac with customizing user db table
and setting it to expire after some time. But Using AES here with username and secret key will
allow us to track time even without saving to database. Still Hmac with random time is more secure.

Key should be 32bits and AES mode is CBC not ECB
"""


def index(request):
    return JsonResponse({'RestAPI':'v1.0'})


def rest_login(request):
    #Uncomment this to only allow get request
    #if request.method is not 'POST':
    #   return JsonResponse({'Forbidden':'Get Request Not Allowed'})

    #Use Post for security and Hmac for api token
    username = str(request.GET.get('user',''))
    password = str(request.GET.get('pass',''))
    if not username or not password:
        return JsonResponse({'response':'error|Username and Password are required.','get_query_parameters':'user,pass'})
    
    try:
        api_db = ApiTokens.objects.get(username=username)
        if api_db.active is not 0:
            return JsonResponse({'token':api_db.token,'validity':'3600sec','id':User.objects.get(username=username).id})
    except:
        pass

    if authenticate(username=username, password=password):
        token = api_token(username)
        api_db = ApiTokens(username=username,token=token,active=1,expiry=datetime.datetime.now() + datetime.timedelta(minutes=60))
        api_db.save()
        return JsonResponse({'token':token,'validity':'3600sec','id':User.objects.get(username=username).id})
    else:
        return JsonResponse({'response':'error|Username or Password are incorrect.'})


def rest_signup(request):
    #Uncomment this to only allow get request
    #if request.method is not 'POST':
    #   return JsonResponse({'Forbidden':'Get Request Not Allowed'})

    username = str(request.GET.get('user',''))
    password = str(request.GET.get('pass',''))
    email = str(request.GET.get('email',''))
    firstname = str(request.GET.get('fname',''))
    lastname = str(request.GET.get('lname',''))
    
    if not username or not password or not email:
        return JsonResponse({'response':'error|Username, Password and Email are required.','get_query_parameters':'user,pass,email,fname,lname'})
    
    if len(username) < 3:
        return JsonResponse({'response': 'error|Username length less than 3 chars.'})

    if len(password) < 6:
        return JsonResponse({'response': 'error|Password should be atleast 6 chars.'})

    if not check_email(email):
        return JsonResponse({'response':'error|email is required'})

    #check if username exist:
    try:
        User.objects.get(username=username)
        return JsonResponse({'error':'Username already exist.'})
    except:
        pass

    #Create user without model.
    user = User.objects.create_user(username, email, password)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    return JsonResponse({'response':'success'})


def rest_user_details(request,id):
    token = str(request.GET.get('token',''))
    if not token:
        return JsonResponse({'response':'error|Api token required'})
    try:
        username = User.objects.get(pk=id)
        decrypted = verify_token(token,str(username))
    except:
        return JsonResponse({'response':'error|username not found'})

    try:
        api_db = ApiTokens.objects.get(username=username,token=token)
    except:
        return JsonResponse({'response':'error|invalid token'})


    if not decrypted or api_db.active is 0:
        return JsonResponse({'response':'error|invalid token'})

    return JsonResponse({'username':str(username),'first_name':username.first_name,'last_name':username.last_name,'email':username.email})


def rest_logout(request):
    username = str(request.GET.get('user',''))
    token = str(request.GET.get('token',''))
    if not username or not token:
        return JsonResponse({'response':'error|Username and Token are required'})
    try:
        api_db = ApiTokens.objects.get(username=username)
    except:
        return JsonResponse({'response':'error|username not found'})
    if api_db.token != token:
        return JsonResponse({'response':'error|invalid token'})
    else:
        api_db.active = 0
        api_db.save()
        return JsonResponse({'response':'success'})

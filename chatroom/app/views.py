import json

from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import UserInfo

def login(req):
    # Redirecting to login page.
    return render(req, "registration.html", dict(page="login"))

def registration_page(req):
    # Redirecting to registration page.
    return render(req, "registration.html", dict(page="registration"))

def register(req):
    '''
    Storing the user registration ifno.
    Creating an entry into the UserInfo table.
    Args:
        username = username, type is string.
        lastname = users lastname, type is string.
        email = user email, type is string.
        password = user password, type is string.
    '''
    try:
        data = json.loads(req.body)
    except:
        data = {}

    username = data.get("username", "")
    lastname = data.get("lastname", "")
    email = data.get("email", "")
    password = data.get("password", "")

    # Checking if all the arguments are there or not,
    if not all([username, lastname, email, password]):
        return JsonResponse(dict(success=False,
                            message="Provide all the required arguments!!"))

    if UserInfo.objects.filter(username=username).first():
        return JsonResponse(dict(success=False,
                            message="User name already exists!!"))

    # Creating an entry into the table.
    UserInfo.objects.create(username=username, last_name=lastname,
        email=email, password=password)

    return JsonResponse(dict(success=True))

def login_user(req):
    '''
    Checking user login details.
    Args:
        email = user email, type is string.
        password = user password, type is string.
    '''
    try:
        data = json.loads(req.body)
    except:
        data = {}

    email = data.get("email", "")
    password = data.get("password", "")

    # Checking if all the arguments are there or not,
    if not all([email, password]):
        return JsonResponse(dict(success=False,
                            message="Provide all the required info!!"))

    user_obj = UserInfo.objects.filter(email=email).first()
    if not user_obj:
        return JsonResponse(dict(success=False,
                            message="User not exists!!"))

    # Checking the given password is matching or not
    if user_obj.password != password:
        return JsonResponse(dict(success=False,
                            message="Invalid password!!"))

    return JsonResponse(dict(success=True, user=user_obj.username))

def home(req):
    # Rendering the home page.
    username = req.GET.get("user", "")
    user_obj = UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return HttpResponse("No user found with {} username".format(username))
    return render(req, "home.html", dict(user=user_obj.username))

def list_users(req):
    '''
    Returns list of users info.
    If we pass any string, it will return the matched users info
    '''
    try:
        data = json.loads(req.body)
    except:
        data = {}

    q = data.get("q", "")
    if q:
        # Fetch users matched with the give query.
        data = UserInfo.objects.filter(username__startswith=q)
    else:
        # Get all the users
        data = UserInfo.objects.all()

    template = loader.get_template("user_info.html")
    html = template.render(dict(users=data), req)

    return JsonResponse(dict(html=html, success=True))

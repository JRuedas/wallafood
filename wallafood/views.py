from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from math import sin, cos, sqrt, atan2, radians
from . import forms
from wallafood.models import Advert, User
import logging, operator
from wallafood.models import Advert, User, Room
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from django.conf import settings
from django.http import JsonResponse

# Create your views here.


def index(request):
    context = {}
    return render(request, "wallafood/login.html", context)

def register(request):
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Account activation.'
            message = render_to_string("wallafood/email_activation.html", {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            messages.info(request,'Check your email for a validation link')
            return redirect("/wallafood/login")
    else:
        form = forms.CreateUserForm()

    return render(request, "wallafood/register.html", {'form': form})

def doLogin (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect("/wallafood/advertisements")
        else:
            try:
                user = User.objects.get_by_natural_key(username)

                if user.is_active:

                    messages.error(request,'The password is not correct')
                else:
                    messages.error(request,'The account is not activated')

                return redirect("/wallafood/login")
            except ObjectDoesNotExist:
                messages.error(request,'The username does not exist')
                return redirect("/wallafood/login") 

@login_required(login_url='/wallafood/login')
def doLogout (request):
    logout(request)
    return redirect("/wallafood/login")

def forbidden(request):
    context = {}
    return render(request, "wallafood/forbidden.html", context)

def redirect_forbidden(request):
    if request.user.is_authenticated:
        return redirect("/wallafood/advertisements")
    else:
        return redirect("/wallafood/login")

@login_required(login_url='/wallafood/login')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("/wallafood/advertisements")
    else:
        form = forms.EditProfileForm(instance=user)
        
    return render(request, "wallafood/edit_profile.html", {'form': form,"user" : user})

@login_required(login_url='/wallafood/login')
def delete_user(request):
    username = request.GET.get('username')

    user = User.objects.get_by_natural_key(username)
    user.delete()
    return redirect("/wallafood/login")

@login_required(login_url='/wallafood/login')
def change_password(request):
    user = request.user

    if request.method == 'POST':
        form = forms.EditPasswordForm(data=request.POST, user=user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)            
            return redirect("/wallafood/advertisements")
    else:
        form = forms.EditPasswordForm(user=user)
    
    return render(request, "wallafood/change_password.html", {'form': form,"user" : user})

@login_required(login_url='/wallafood/login')
def advertisements(request):
    context = {}
    adverts = []
    auxadverts = Advert.objects.all()
    for add in auxadverts:
        if request.user.username != add.vendor:
            adverts.append(add)
    
    context = {
        'adverts': adverts
    } 

    return render(request, "wallafood/advertisements.html", context)

@login_required(login_url='/wallafood/login')
def my_adds(request):
    context = {}

    username = request.user.username
    queary= 'SELECT * FROM wallafood_Advert WHERE vendor LIKE \'%'+username+'%\''
    adverts = list(Advert.objects.raw(queary))
    context = {
        'adverts': adverts
    } 

    return render(request, "wallafood/my_adds.html", context)

@login_required(login_url='/wallafood/login')
def addAdvert(request):
    form = forms.CreateAdvertForm(request.POST)

    if request.method == 'POST':
        form = forms.CreateAdvertForm(request.POST)
        username = request.user.username
        if form.is_valid():
            advert = form.save(commit=False)
            advert.vendor = username
            advert.vote_average = 0
            advert.status = 'In stock'
            if advert.photo_url == '':
                advert.photo_url = "https://www.telemundo.com/sites/nbcutelemundo/files/images/promo/video_clip/2017/12/21/frutas-y-verduras.jpg"
            advert.save()

            Room.objects.create(name=str(advert.id_advert) + advert.vendor, slug=advert.name, description=advert.description)

            return redirect("/wallafood/advertisements")
    else:
        form = forms.CreateAdvertForm()

    return render(request, "wallafood/add_advert.html", {'form': form})

@login_required(login_url='/wallafood/login')
def edit_advert(request):
    id = request.GET.get("id")
    advert = Advert.objects.get(id_advert=id)

    if request.method == 'POST':
        form = forms.EditAdvertForm(request.POST, instance=advert)

        if form.is_valid():
            form.save()
            return redirect("/wallafood/my_adds")
    else:
        form = forms.EditAdvertForm(instance=advert)
        
    return render(request, "wallafood/edit_advert.html", {'form': form,"advert": advert})

@login_required(login_url='/wallafood/login')
def delete_advert(request):
    id = request.GET.get('id')

    advert = Advert.objects.get(id_advert=id)
    advert.delete()
    
    return redirect("/wallafood/my_adds")

@login_required(login_url='/wallafood/login')
def findAdvertisement(request):
    context = {}

    if request.method == 'GET':
        logger = logging.getLogger(__name__)
        text = request.GET['text_search']
        filter = request.GET['filter']
        adverts = []
        if filter != 'location':
            logger.error(text)
            logger.error(filter)
            queary= 'SELECT * FROM wallafood_Advert WHERE '+filter+' LIKE \'%'+text+'%\''
            logger.error(queary)
            auxadverts = list(Advert.objects.raw(queary))
            for add in auxadverts:
                if add.vendor != request.user.username:
                    adverts.append(add)
        else:
            queary= 'SELECT * FROM wallafood_Advert WHERE name LIKE \'%'+text+'%\''
            auxadverts = list(Advert.objects.raw(queary))
            location = request.user.location
            latlong = location.split(',')
            R = 6373.0
            lat1 = float(latlong[0])
            lon1 = float(latlong[1])
            distances = {}
            for add in auxadverts:
                if add.vendor != request.user.username:
                    auxlocation = User.objects.get(username=add.vendor).location
                    auxlatlong = auxlocation.split(',')
                    lat2 = float(auxlatlong[0])
                    lon2 = float(auxlatlong[1])

                    dlon = lon2 - lon1
                    dlat = lat2 - lat1

                    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))

                    distance = R * c
                    distances[add.id_advert] = distance

            logger.error(distances)
            auxshorted = sorted(distances.items(), key=operator.itemgetter(1), reverse=False)
            logger.error(auxshorted)
            for key in auxshorted:
                for add in auxadverts:
                    if add.id_advert == key[0]:
                        adverts.append(add)

        context = {
            'adverts': adverts,
        } 

    return render(request, "wallafood/advertisements.html", context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        messages.info(request,'Account validated')
        return redirect("/wallafood/login")
    else:
        messages.info(request,'Validation link invalid')
        return redirect("/wallafood/login")

@login_required(login_url='/wallafood/login')
def showChats(request):
    rooms = Room.objects.filter(name__icontains=request.user.username)
    return render(request, 'wallafood/chats.html', {'rooms': rooms})

@login_required(login_url='/wallafood/login')
def showChatDetail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'wallafood/chat_detail.html', {'room': room})

def token(request):
    user = request.user
    identity = user.username
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, secret=api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MiniSlackChat:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8')
    }
    return JsonResponse(response)
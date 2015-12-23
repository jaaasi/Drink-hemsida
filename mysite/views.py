import string
from django.core.mail import send_mail
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib import messages
import random
from mysite.models import *
import string
from django.contrib.auth.models import User
from django.template import loader



def homepage(request):
    return render_to_response('homepage.html', context_instance=RequestContext(request))

def profile(request, user_id):
    return render_to_response('profile.html',context_instance=RequestContext(request))




def recept(request):
    drinkList = Drink.objects.all()
    return render_to_response('recept.html', {'drinkList': drinkList}, context_instance=RequestContext(request))


# Confirm that a new account is created
def account_created(request):
    return render_to_response("accountcreated.html", {}, context_instance=RequestContext(request))

def add(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            drinkNamn = request.POST['drinkNamn']
            url = request.POST['url']
            hvRating = request.POST['hv']
            ratingVanlig = request.POST['rating']
            drinkTyp = request.POST['type']
            inst = request.POST['instructions']
            ing1 = request.POST['ingredient1']
            ing2 = request.POST['ingredient2']
            ing3 = request.POST['ingredient3']
            ing4 = request.POST['ingredient4']
            ing5 = request.POST['ingredient5']
            ing6 = request.POST['ingredient6']
            ing7 = request.POST['ingredient7']
            ing8 = request.POST['ingredient8']

            new_drink = Drink(namn = drinkNamn, bildurl = url, hv = hvRating, rating = ratingVanlig, type = drinkTyp, instructions = inst, ingredient1 = ing1, ingredient2=ing2, ingredient3=ing3,ingredient4=ing4, ingredient5=ing5, ingredient6=ing6, ingredient7=ing7, ingredient8=ing8)
            new_drink.save()
            messages.success(request, "Drinken lades till!")
            return HttpResponseRedirect('/recept')
        else:
            return render_to_response("add.html", context_instance=RequestContext(request))
    else:
        return HttpResponse("Please log in.")

# Delete game
def delete(request, id):
    get_object_or_404(Drink, pk=id).delete()
    messages.success(request, "Drinken har tagits bort!")
    return HttpResponseRedirect('/recept')


# Function for creating an account that is inactive, calls send_registration_confirmation function
# and redirects to "accountcreated" page.
def create_account(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.confirmation_code = id_generator(6)
            user = User.objects.get(username=new_user.username)
            new_profile = UserProfile(user=user,
                                      activation_key=new_user.confirmation_code)
            new_profile.save()
            send_registration_confirmation(new_user)

            return HttpResponseRedirect("/accountcreated")
    else:
        form = MyRegistrationForm()

    return render_to_response("createaccount.html", {'form': form, }, context_instance=RequestContext(request))

# Generates a random activation key consisting of alfabethic lower case characters
def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))



# Sends an account confirmation email to the user with a link for activating the account
def send_registration_confirmation(user):
    title = "Account confirmation"
    content = "To activate your account follow the link: https://sol-wsd.herokuapp.com/confirmation/" + str(user.confirmation_code) + "/" + user.username
    send_mail(title, content, '', [user.email], fail_silently=False)


# Activates the account when opening the activation link
def confirmation(request, confirmation_code, username):
    user = User.objects.get(username=username)
    user_profile = get_object_or_404(UserProfile, activation_key=confirmation_code)
    if user_profile.activation_key == confirmation_code:
        if user.is_active:
            messages.warning(request, "Account already activated.")
            return HttpResponseRedirect('/')
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        messages.success(request, "Welcome, the account confirmation was successful, you are now logged in.")
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                messages.error(request, "The account is not active.")
        else:
            messages.error(request, "Invalid credentials supplied. Please try again.")
    else:
        messages.error(request, "Not available")
    return HttpResponseRedirect('/')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
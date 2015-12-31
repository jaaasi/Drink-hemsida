from django.core.mail import send_mail
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib import messages
import random
from mysite.models import *
import string
from django.contrib.auth.models import User



def homepage(request):
    all_events = Event.objects.all()
    return render_to_response('homepage.html', {'events': all_events, 'user': request.user}, context_instance=RequestContext(request))

def profile(request, user_id):
    all_users = User.objects.all()
    return render_to_response('manage.html', {'users': all_users},context_instance=RequestContext(request))


def addEvent(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        if request.method == 'POST':
            eName = request.POST['title']
            elt = request.POST['longText']
            est = request.POST['shortText']
            estartTime = request.POST['startTime']
            eendTime = request.POST['endTime']
            imageUrl = request.POST['imgUrl']
            emaxParticipants = request.POST['maxParticipants']
            newEvent = Event(title = eName, longText = elt, shortText = est, startTime = estartTime, endTime = eendTime, imgUrl = imageUrl, maxParticipants=emaxParticipants)
            newEvent.save()
            messages.success(request, "Event added!")
            return HttpResponseRedirect('/')
        else:
            return render_to_response("addEvent.html", context_instance=RequestContext(request))
    else:
        return HttpResponse("Please log in.")

def editEvent(request, eventID):
    event = Event.objects.get(id=eventID)
    if request.user.is_authenticated() and request.user.is_superuser:
        if request.method == 'POST':
            event.title = request.POST['title']
            event.longText = request.POST['longText']
            event.shortText = request.POST['shortText']
            event.startTime = request.POST['startTime']
            event.endTime = request.POST['endTime']
            event.imgUrl = request.POST['imgUrl']
            event.maxParticipants = request.POST['maxParticipants']
            event.save()
            messages.success(request, "Event edited!")
            return HttpResponseRedirect('/')
    return render_to_response("editEvent.html", {'event': event}, context_instance=RequestContext(request))

def event(request, ID):
    event = Event.objects.get(id=ID)
    participantList = Participant.objects.all().filter(eventID=ID)
    count = len(participantList)
    return render_to_response("event.html", {'event': event, 'participantList': participantList, 'count': count}, context_instance=RequestContext(request))

def eventSignUp(request, eventID):
    eventt = Event.objects.get(id=eventID)
    if request.method == 'POST':
        pname = request.POST['name']
        pemail= request.POST['email']
        pallergies = request.POST['allergies']
        pgreetings = request.POST['greetings']
        peventID = request.POST['id']
        participant=Participant(namn=pname, email = pemail, allergies = pallergies, greetings=pgreetings, eventID=peventID)
        participant.save()
        messages.success(request, 'Sign up succeeded!')
        return HttpResponseRedirect('/')
    return render_to_response("eventSignUp.html", {'event':eventt}, context_instance=RequestContext(request))

def recept(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            if request.method == 'POST':
                drinkToChange = request.POST['drinkID']
                d = Drink.objects.get(id=drinkToChange)
                d.namn = request.POST['drinkNamn']
                d.bildurl = request.POST['url']
                d.hv = request.POST['hv']
                d.rating = request.POST['rating']
                d.type = request.POST['type']
                d.instructions = request.POST['instructions']
                d.ingredient1 = request.POST['ingredient1']
                d.ingredient2 = request.POST['ingredient2']
                d.ingredient3 = request.POST['ingredient3']
                d.ingredient4 = request.POST['ingredient4']
                d.ingredient5 = request.POST['ingredient5']
                d.ingredient6 = request.POST['ingredient6']
                d.ingredient7 = request.POST['ingredient7']
                d.ingredient8 = request.POST['ingredient8']
                d.save()
                messages.success(request, "Drinken endrades!")

    drinkList = Drink.objects.order_by('-rating', '-hv')


    currentUser = request.user
    return render_to_response('recept.html', {'drinkList': drinkList, 'user': currentUser }, context_instance=RequestContext(request))


# Confirm that a new account is created
def account_created(request):
    return render_to_response("accountcreated.html", {}, context_instance=RequestContext(request))

def addDrink(request):
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
            return render_to_response("addDrink.html", context_instance=RequestContext(request))
    else:
        return HttpResponse("Please log in.")


def deleteDrink(request, id):
    if request.user.is_superuser:
        get_object_or_404(Drink, pk=id).delete()
        messages.success(request, "Drinken har tagits bort!")
    return HttpResponseRedirect('/recept')


def deleteEvent(request, id):
    if request.user.is_superuser:
        get_object_or_404(Event, pk=id).delete()
        messages.success(request, "Evenemanget har tagits bort!")
    return HttpResponseRedirect('/')


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
    content = "To activate your account follow the link: localhost:8000/confirmation/" + str(user.confirmation_code) + "/" + user.username
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
                try:
                    user = UserProfile.objects.get(user_id=request.user.id)
                except UserProfile.DoesNotExist:
                    new_user = UserProfile(user_id=request.user.id, is_developer=0)
                    new_user.save()
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

# Demotes user from being superuser
def demotesuper(request, id):
    if request.user.is_superuser == 1:
        user = User.objects.get(id=id)
        user.is_superuser = 0
        user.save()
        return HttpResponseRedirect('/profile/' + str(request.user.id))
    else:
        HttpResponse("Only superusers can promote/demote users")

def promotesuper(request, id):
    if request.user.is_superuser == 1:
        user = User.objects.get(id=id)
        user.is_superuser = 1
        user.save()
        return HttpResponseRedirect('/profile/' + str(request.user.id))

    else:
        HttpResponse("Only superusers can promote/demote users")

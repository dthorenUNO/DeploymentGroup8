from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from myshop import settings
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Profile, Review


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, 'accounts/logIn.html', {'errors': 'Your username and password didn \'t match.Please try again.'})
    else:
        return render(request, 'accounts/logIn.html')

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)

def registerUser(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'],
                             first_name=request.POST['firstname'], last_name=request.POST['lastname'])

            Profile.objects.create(user=user, address=request.POST['address'], zipcode=request.POST['zipcode'], state=request.POST['state'],
                               city=request.POST['city'], phone=request.POST['phone'])


        except Exception as e:
            print(e)
            return render(request, 'accounts/signup.html', {'errors':e.__repr__()})
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return render(request, 'accounts/signup.html')


def review(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/logIn.html', {'errors': 'Please log in to review! '})
    if request.method == 'POST':
        Review.objects.create(user=request.user, contact=request.POST['contact'], message=request.POST['message'], contact_type=request.POST['select2'])
        return render(request, 'accounts/review.html', {"message":"Your review has been submitted!"})
    return render(request, "accounts/review.html")





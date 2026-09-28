from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.http import url_has_allowed_host_and_scheme


from .models import Account
from .forms import RegistrationForm
from apps.carts.models import Cart



def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Generate a unique username from the email prefix
            base_username = email.split("@")[0]
            username = base_username
            counter = 1

            while Account.objects.filter(username=username).exists():
                username = f'{base_username}{counter}'
                counter +=1 

            user = Account.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                phone_number=phone_number
            )
            user.is_active = True
            user.save()

            messages.success(request, "Registration Succeesfull! You may now log in.")
            return redirect("login")

    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("home")

    # 2. Just opening the page (GET): show the form.
    if request.method != "POST":
        return render(request, "accounts/login.html")

    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "")

    # 4. Check the credentials.
    user = auth.authenticate(request, email=email, password=password)

    if user is None:
        messages.error(request, "Invalid email or password. Please try again.")
        return render(request, "accounts/login.html")

    # 5. Remember the guest's session key BEFORE logging in.
    old_session_key = request.session.session_key

    # 6. Log in. Django changes the session key here.
    auth.login(request, user)
    new_session_key = request.session.session_key

    # 7. Move the guest's cart to the new session key.
    if old_session_key:
        Cart.objects.filter(cart_id=old_session_key).update(cart_id=new_session_key)

    messages.success(request, "You are logged in successfully!")

    # 8. Go back to where the user came from (e.g. checkout), else home.
    next_url = request.GET.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("home")


@login_required(login_url="login")
def signout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
    
def change_password(request): pass

def edit_profile():pass


@login_required(login_url="login")
def profile(request): 
    return render(request, "profile/profile.html")
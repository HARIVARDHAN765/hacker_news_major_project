from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from ..forms import (
    RegisterForm,
    LoginForm,
)

from ..models import Profile


def login_view(request):

    if request.method == "POST":

        form = LoginForm(
            request,
            data=request.POST,
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user,
            )

            next_url = request.POST.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("home")

    else:

        form = LoginForm()

    register_form = RegisterForm()

    return render(
        request,
        "home/login.html",
        {
            "login_form": form,
            "register_form": register_form,
        },
    )


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(
            request.POST,
        )

        if form.is_valid():

            user = form.save()

            Profile.objects.create(
                user=user,
            )

            login(
                request,
                user,
            )

            return redirect("home")

        login_form = LoginForm()

        return render(
            request,
            "home/login.html",
            {
                "register_form": form,
                "login_form": login_form,
            },
        )

    return redirect("login")


def logout_view(request):

    logout(request)

    return redirect("home")
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .selectors import get_profile_for_user
from .services import register_user


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = register_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
            email=form.cleaned_data["email"],
        )
        return redirect("accounts:login")

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile_view(request):
    profile = get_profile_for_user(request.user)
    return render(request, "accounts/profile.html", {"profile": profile})

from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, UserProfileForm


@login_required
def update_profile(request):
    form = UserProfileForm(instance=request.user.userprofile)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES or None, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'New post deleted successfully')

            return redirect("accounts:profile")
        else:
            form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
            # context = {
            #     "form":form, 
            # }
            # return render(request, "account/profile.html", context)

    context = {
        "form":form, 
    }
    return render(request, "account/profile.html", context)
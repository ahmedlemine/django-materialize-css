from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, UserProfileForm
# from .models import CustomUser, UserProfile


#old
# @login_required
# @transaction.atomic # prevents saving one form/model without the other.
# def update_profile(request):
#     if request.method == "POST":
#         user_form = CustomUserChangeForm(request.POST, instance=request.user)
#         user_profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
#         if user_form.is_valid() and user_profile_form.is_valid():
#             user_form.save()
#             user_profile_form.save()
#             return redirect("/")
#     else:
#         user_form = CustomUserChangeForm(instance=request.user)
#         user_profile_form = UserProfileForm(instance=request.user.userprofile)
    
#     context = {
#         "u_form":user_form, 
#         "p_form": user_profile_form
#     }
#     return render(request, "account/profile.html", context)


@login_required
def update_profile(request):
    form = UserProfileForm(instance=request.user.userprofile)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES or None, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
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
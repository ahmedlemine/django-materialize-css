from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, UserProfileForm
from posts.models import Post

@login_required
def update_profile(request):
    user = request.user
    form = UserProfileForm(instance=user.userprofile)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES or None, instance=user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

            return redirect("accounts:profile")
        else:
            form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
            # context = {
            #     "form":form, 
            # }
            # return render(request, "account/profile.html", context)

    context = {
        "posts": Post.objects.filter(creator=user),
        "form":form, 
    }
    return render(request, "account/profile.html", context)
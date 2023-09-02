from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from posts.models import Post
from .models import CustomUser

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


    context = {
        "posts": Post.objects.filter(creator=user),
        "form":form, 
    }
    return render(request, "account/profile.html", context)

def public_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    userprofile = user.userprofile
    post_list = Post.objects.filter(creator=user)
    context = {
        'userprofile': userprofile,
        'post_list': post_list
    }
    return render(request, 'account/public_profile.html', context)
import time

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView
from hitcount.views import HitCountDetailView

from .mixins import UserIsOwnerMixin
from .models import Post, Comment
from .forms import PostForm, CommentForm

class Index(ListView):
    paginate_by = 8
    model = Post
    template_name = 'posts/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:5],
        'recent_posts': Post.objects.order_by('-added')[:5]
        })
        return context  

class PostDetail(HitCountDetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:5],
        'recent_posts': Post.objects.order_by('-added')[:5],
        'form': CommentForm()
        })
        return context    
 
class PostDelete(UserIsOwnerMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy('posts:index')

@login_required
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.creator = request.user
            new_post.save()
            messages.success(request, 'New post created successfully')
            return redirect(new_post.get_absolute_url())
        else:
            messages.success(request, 'Please correct errors in form an try agin')
            form = PostForm(request.POST, request.FILES or None)
    
    form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def update_post(request, slug):
    p = Post.objects.get(slug=slug)
    
    if p.creator != request.user:
        messages.error(request, 'Ownership error! You are not allowed to edit this post.')
        return redirect(p.get_absolute_url())
    
    form = PostForm(instance=p)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None, instance=p)
        if form.is_valid():
            p.title = form.cleaned_data['title']
            p.body = form.cleaned_data['body']
            p.image = form.cleaned_data['image']
            p.save()
            messages.success(request, 'Post updated successfully')
            context = {
                'post': p,
                'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:5],
                'recent_posts': Post.objects.order_by('-added')[:5]
            }
            return redirect(p.get_absolute_url())
        else:
            messages.error(request, 'Please correct errors in form an try agin')
            form = PostForm(request.POST, request.FILES or None)
    
    context = {
        'post': p,
        'form': form
    }
    return render(request, 'posts/update_post.html', context)


@login_required
@require_http_methods(['DELETE'])
def delete_post_htmx(request, slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    posts = Post.objects.all()
    context = {
        'post_list': posts
    }
    return render(request, 'posts/_post_list.html', context)


# HTMX form to return in partial template
@login_required
def create_post_form(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            posts = Post.objects.all()
            context = {
                'post_list': posts
            }
            return render(request, 'posts/_post_list.html', context)
        else:
            form = PostForm(request.POST, request.FILES or None)
            context = {
                'form': form
            }
            return render(request, 'posts/create_post.html', context)
    
    form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/_post_form.html', context)


@login_required
def update_post_form(request, slug):
    p = Post.objects.get(slug=slug)
    form = PostForm(instance=p)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            p.title = form.cleaned_data['title']
            p.body = form.cleaned_data['body']
            p.image = form.cleaned_data['image']
            p.save()

            context = {
                'post': p
            }

            return redirect(p.get_absolute_url())
        else:
            form = PostForm(request.POST, request.FILES or None)
    
    context = {
        'post': p,
        'form': form
    }
    return render(request, 'posts/_post_update_form_htmx.html', context)


@login_required
def create_comment_form(request, slug):
    p = Post.objects.get(slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = p
            c.user = request.user
            c.save()
            new_comment = Comment.objects.get(pk=c.pk)
            form = CommentForm()
            context = {
                'comment': new_comment,
            }
            time.sleep(0.3)
            return render(request, 'posts/_comment.html', context)
        else:
            form = CommentForm(request.POST or None)
            context = {
                'post': p,
                'form': form,
            }
            return render(request, 'posts/_comment_form.html', context)
    context = {
        'post': p,
        'form': CommentForm()
    }
    return render(request, 'posts/_comment_form.html', context)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    context = {
        'pk': comment.pk
    }
    if request.method == 'POST':
        if request.user == comment.user:
            time.sleep(0.3)
            comment.delete()
            return render(request, 'posts/htmx/_htmx_comment_deleted.html', context)
        return HttpResponseForbidden('Not Allowed')

    return HttpResponseNotAllowed( ['POST'], 'Not Allowed')


def htmx_post_list(request):
    context = {
        'post_list': Post.objects.all()
    }
    return render(request, 'posts/_post_list.html', context)


def ajax_post_list(request):
    post_list = list(Post.objects.values())
    return JsonResponse(post_list, safe=False)


def search(request):
    qs = Post.objects.all()
    q = request.GET.get('q')
    if q and q != '':
        qs = qs.filter(
                Q(title__icontains=q) |
                Q(body__icontains=q)
                ).distinct()
        context = {
            'post_list': qs,
            'keyword': q
        }
        return render(request, 'posts/search_results.html', context)
        
    context = {
        'post_list': ''
    }
    return render(request, 'posts/search_results.html', context)

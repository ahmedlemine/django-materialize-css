from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView, DeleteView

from .models import Post
from .forms import PostForm

class UserIsOwnerMixin(AccessMixin):
    """Verify that the user is the owner of related object.
        owner_id_field => leave as is. but after '=' put
        the model field realted to owner. like 'user',
        'creator', 'created_by', 'author'. 
    """
    owner_id_field = 'creator'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(self.get_object(), self.owner_id_field) != request.user.pk:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class Index(ListView):
    model = Post
    template_name = 'posts/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context  

class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:5],
        })
        return context    
 
class PostDelete(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
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
            return redirect('/')
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
        return redirect('/')
    
    form = PostForm(instance=p)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        
        if form.is_valid():
            p.title = form.cleaned_data['title']
            p.body = form.cleaned_data['body']
            p.image = form.cleaned_data['image']
            p.save()
            messages.success(request, 'post updated successfully')
            context = {
                'post': p,
                'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:5],
            }
            return render(request, 'posts/post_detail.html', context)
        else:
            messages.success(request, 'Please correct errors in form an try agin')
            form = PostForm(request.POST, request.FILES or None)
    
    context = {
        'form': form
    }
    return render(request, 'posts/update_post.html', context)

# def index_view(request):
#     qs = Post.objects.all()
#     context = {
#         'qs': qs
#     }
    
#     return render(request, 'posts/index.html', context)
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
    # return HttpResponse(f"Post: '{post.title}' successfully deleted.") 


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
            # posts = Post.objects.all()
            context = {
                'post': p
            }
            # return render(request, 'posts/post_detail.html', context)
            return redirect('/')
        else:
            form = PostForm(request.POST, request.FILES or None)
    
    context = {
        'post': p,
        'form': form
    }
    return render(request, 'posts/_post_update_form_htmx.html', context)

def search(request):
    qs = Post.objects.all()
    q = request.GET.get('q')
    if q:
        qs = qs.filter(
                Q(title__icontains=q) |
                Q(body__icontains=q)
                ).distinct()
        context = {
            'post_list': qs
        }
        return render(request, 'posts/_posts_li.html', context)
        # return render(request, 'posts/_post_list.html', context)
    # post_list = {}
    # for post in qs:
    #     post_list[post.title] = 'static/posts/images/user_avatar.jpg'
    # print(post_list)
    # return render(request, 'posts/_post_list.html', {'post_list': qs})

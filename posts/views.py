from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView, DeleteView

from .models import Post
from .forms import PostForm


class Index(ListView):
    model = Post
    # context_object_name = 'objects'
    
    template_name = 'posts/index.html'
    
    # convert views to K or M
    views = 40000
    if views >= 1000000:
        views = "%.0f%s" % (views/1000000.00, 'M')
    else:
        if views >= 1000:
            views = "%.0f%s" % (views/1000.0, 'k')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['views'] = self.views
        return context

class PostDelete(DeleteView):
    model = Post
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy('index')

def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            # title = form.cleaned_data['title']
            # body = form.cleaned_data['body']
            # new_post = Post.objects.create(title=title, body=body)
            # new_post.save()
            form.save()
            return redirect('index')
        else:
            form = PostForm(request.POST or None)
    
    form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)

class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'


def update_post(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            # title = form.cleaned_data['title']
            # body = form.cleaned_data['body']
            # new_post = Post.objects.create(title=title, body=body)
            # new_post.save()
            form.save()
            return redirect('/')
        else:
            form = PostForm(request.POST or None)
    
    context = {
        'form': form
    }
    return render(request, 'posts/post_update.html', context)

# def index_view(request):
#     qs = Post.objects.all()
#     context = {
#         'qs': qs
#     }
    
#     return render(request, 'posts/index.html', context)
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
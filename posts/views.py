from django import forms
from django.forms.fields import ImageField
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .forms import PostForm


def index(request):
    # If the method is POST
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        # If the form is valid
        if form.is_valid():
             # Yes, Save
             form.save()

             # Redirect to Home
             return HttpResponseRedirect('/')

        else:
             # No, Show Error
             return HttpResponseRedirect(form.error.as_json())

    # Get all posts, limit = 20
    posts = Post.objects.all().order_by('-created_at')[:20]
    form = PostForm()

    return render(request, 'posts.html',{'posts': posts})

def delete(request, post_id):
    # Find Post
    post = Post.objects.get(id = post_id)
    post.delete()
    return HttpResponseRedirect('/')

def like(request, post_id):
    newlikecount = Post.objects.get(id=post_id)
    newlikecount.likecount += 1
    newlikecount.save()
    return HttpResponseRedirect('/')

def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect("not valid")
    form = PostForm
    return render(request, "edit.html", {"posts": post})

def LikeView(request, post_id):
    post = Post.objects.get(id=post_id)
    new_value = post.likes + 1
    post.likes = new_value
    post.save()
    return HttpResponseRedirect('/')

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CreatePost, CreateComment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.db.models import Func, F
#Contributers: Derek, Michael

#Login Required Decorator after each page where authentication is needed.
#Renders a page based on the Post (gained from url) and template post.html

@login_required
def dynamic_post_view (request, id):
    post = Post.objects.get(id=id)
    comments = post.comments.all().order_by('-id')
    form = CreateComment()
    if request.method == "POST":
        new  = CreateComment(request.POST)
        if new.is_valid():
            fpost = new.save(commit=False)
            fpost.author = request.user
            fpost.post = post
            fpost.save()
            return HttpResponseRedirect('/post/' + str(post.id) + "#" + str(fpost.id))
        else:
            form = new
            context = {"post": post, "form": form, "comments":comments}
            return render(response, "register.html", context)
    else:
        context = {"post": post, "form": form, "comments":comments}
        return render(request, "post.html", context)

#creates a page based on teh user (gained from url) and template user.html
@login_required
def dynamic_account_view (request, username):
    account = User.objects.get(username=username)
    posts = Post.objects.filter(author=username)
    context = {"account": account,
               "posts":posts,
            }
    return render(request, "user.html", context)

#creates a post if method == POST and returns a page with a form if it is GET.
@login_required
def post_create(request):
    if request.method == "POST":
        form = CreatePost(request.POST)
        print("Created")
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return HttpResponseRedirect('/post/' + str(Post.objects.latest('id').id))
        else:
            context = {'form': form}
            return render(response, "register.html", context)
    else:
        form = CreatePost()
        print("Retrieved")
        context = {'form': form}
    return render(request, 'createpost.html', context)

#Returns a Page with the template feed.html and the posts list of Post objects.
@login_required
def feed(request):
    posts = Post.objects.order_by('-id')[:20]
    context = {"posts": posts}
    return render(request, "feed.html", context)

#Returns a Page with the template maps.html and shows map image. 
@login_required
def maps(request):
    posts = Post.objects.order_by('-id')[:20]
    context = {"posts": posts}
    return render(request, "maps.html", context)

# @login_required
# def maps(request):
#     if request.method == "POST":
#         form = CreatePost(request.POST)
#         print("Created")
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             form.save()
#             return HttpResponseRedirect('/maps/' + str(Post.objects.latest('id').id))
#         else:
#             context = {'form': form}
#             return render(response, "register.html", context)
#     else:
#         form = CreatePost()
#         print("Retrieved")
#         context = {'form': form}
#     return render(request, 'maps.html', context)

#Creates a new User if the response type is POST and redirects to /login. Otherwise, if GET, returns a page with a registration form.
def register(response):
    if response.method == "POST":
        form =  UserCreationForm(response.POST)
        print('Posted')
        if form.is_valid():
            form.save()
            print('Done')
            return HttpResponseRedirect('/login')
        else:
            context = {'form':form}
            return render(response, "register.html", context)
    else:
        form =  UserCreationForm()
        context = {'form':form}
        return render(response, "register.html", context)

#if url is called, it will delelte the specified object based on the dynamic url. However, if the user is not the loged in user, it will deny permission, fixing a possible vunerability.
@login_required
def delete(request, id):
    if str(request.user) == str(Post.objects.get(id=id).author):
        Post.objects.get(id=id).delete()
        return HttpResponseRedirect('/user/' + str(request.user))
    else:
        raise PermissionDenied()

#if url is called, it will delelte the specified object based on the dynamic url. However, if the user is not the loged in user, it will deny permission, fixing a possible vunerability.
@login_required
def comment_delete(request, id):
    if str(request.user) == str(Comment.objects.get(id=id).author):
        c = Comment.objects.get(id=id)
        Comment.objects.get(id=id).delete()
        return HttpResponseRedirect('/post/' + str(c.post.id) + "#" + str(c.post.comments.latest('id').id))
    else:
        raise PermissionDenied()

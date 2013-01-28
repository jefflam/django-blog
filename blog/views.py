from blog.models import Post
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_list_or_404
from django.template import RequestContext


def home(request):
    posts = Post.objects.all().order_by('-pub_date')
    return render_to_response('blog/index.html', {'posts': posts}, context_instance=RequestContext(request))


def post(request, post_slug):
    post = Post.objects.get(slug__exact=post_slug)
    return render_to_response('blog/post.html', {'post': post}, context_instance=RequestContext(request))


def dashboard(request):
    return HttpResponse("Dashboard page showing drafts and published posts.")


def login(request):
    return HttpResponse("Function to log user in.")


def logout(request):
    return HttpResponse("Function to log user out.")

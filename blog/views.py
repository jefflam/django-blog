from blog.models import Post
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import datetime


# Index page, showing all posts
def home(request):
    posts = Post.objects.filter(published=True).order_by('-pub_date')
    return render_to_response('blog/index.html', {'posts': posts}, context_instance=RequestContext(request))


# A single page showing one post in detail
def post(request, post_slug):
    post = Post.objects.get(slug__exact=post_slug)
    return render_to_response('blog/post.html', {'post': post}, context_instance=RequestContext(request))


# Login authentication page
def login(request):
    if request.user.is_authenticated():
        return dashboard(request)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return dashboard(request)
            else:
                return render_to_response('blog/login.html', context_instance=RequestContext(request))
    return render_to_response('blog/login.html', context_instance=RequestContext(request))


# Function to log user out
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('blog.views.home'))


# Dashboard displaying drafts and published posts with links to edit them
@login_required
def dashboard(request):
    posts = Post.objects.filter(published=True).order_by('-pub_date')
    drafts = Post.objects.filter(published=False).order_by('-pub_date')
    return render_to_response('blog/dashboard.html',
                             {'posts': posts,
                              'drafts': drafts},
                              context_instance=RequestContext(request))


# Function to create a new Post object from dashboard page
@login_required
def create(request):
    title = request.POST['post-title']
    if title != "":
        date = (datetime.datetime.now()).strftime("%Y-%m-%d")
        slug = "-".join(title.split()).lower()  # Splits post title, joins them back with a dash and lowercase string
        Post.objects.create(title=title,
                            body="",
                            pub_date=date,
                            published=False,
                            slug=slug)
        return edit(request, slug)


# Page to edit a single post
@login_required
def edit(request, post_slug):
    post = Post.objects.get(slug__exact=post_slug)
    return render_to_response('blog/edit.html', {'post': post}, context_instance=RequestContext(request))


# Function to update a single post from edit page
@login_required
def update(request, post_slug):
    post = Post.objects.get(slug__exact=post_slug)
    try:
        post.title = request.POST['post-title']
        post.body = request.POST['post-body']
        # Set post_published_checbox = "on" if checkbox is checked, if not set to False
        post_published_checkbox = request.POST.get("post-published", False)
        if post_published_checkbox:
            post.published = True
        else:
            post.published = False
        post.pub_date = request.POST['post-date']
        post.slug = request.POST['post-slug']
        post.save()
        print request.POST
        return HttpResponseRedirect(reverse('blog.views.dashboard'))
        # return render_to_response('blog/dashboard.html', {'success': True}, context_instance=RequestContext(request))
    except:
        print "error"
        return HttpResponseRedirect(reverse('blog.views.edit', args=(post_slug,)))
        # return render_to_response('blog/edit.html', {'post': post}, context_instance=RequestContext(request))

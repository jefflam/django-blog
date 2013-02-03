from blog.models import Post
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime


# Index page, showing all posts
def home(request):
    posts = Post.objects.all().order_by('-pub_date')
    return render_to_response('blog/index.html', {'posts': posts}, context_instance=RequestContext(request))


# A single page showing one post in detail
def post(request, post_slug):
    post = Post.objects.get(slug__exact=post_slug)
    return render_to_response('blog/post.html', {'post': post}, context_instance=RequestContext(request))


# Dashboard displaying drafts and published posts with links to edit them
def dashboard(request):
    posts = Post.objects.filter(published=True)
    drafts = Post.objects.filter(published=False)
    # posts = Post.objects.all()
    return render_to_response('blog/dashboard.html',
                             {'posts': posts,
                              'drafts': drafts},
                              context_instance=RequestContext(request))


# Function to create a new Post object from dashboard page
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
def edit(request, post_slug):
    post = Post.objects.get(slug__exact=post_slug)
    return render_to_response('blog/edit.html', {'post': post}, context_instance=RequestContext(request))


# Function to update a single post from edit page
def update(request, post_slug):
    post = Post.objects.get(slug__exact=post_slug)
    try:
        post.title = request.POST['post-title']
        post.body = request.POST['post-body']
        post.published = request.POST['post-draft']
        post.pub_date = request.POST['post-date']
        post.slug = request.POST['post-slug']
        post.save()
        return HttpResponseRedirect(reverse('blog.views.dashboard'))
        # return render_to_response('blog/dashboard.html', {'success': True}, context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('blog.views.edit', args=(post_slug,)))
        # return render_to_response('blog/edit.html', {'post': post}, context_instance=RequestContext(request))


# Login authentication page
def login(request):
    return HttpResponse("Function to log user in.")


# Function to log user out
def logout(request):
    return HttpResponse("Function to log user out.")

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'blog.views.home', name='home'),
    url(r'^login/$', 'blog.views.login', name='login'),
    url(r'^dashboard/$', 'blog.views.dashboard', name='dashboard'),
    url(r'^logout/$', 'blog.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<post_slug>[-\w]+)/$', 'blog.views.post', name='post'),
)

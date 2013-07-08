from django.conf.urls import patterns, include, url
from blog.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),
    url(r'^logged/$', 'blog.views.login', name='home'),
    url(r'^profile/$', 'blog.views.view_profile'),
    url(r'^showpost/$', 'blog.views.showpost'),
    url(r'^add_post/$', 'blog.views.add_post'),
    url(r'^add_post_view/$', 'blog.views.add_post_view'),
    url(r'^add_blog/$', 'blog.views.add_blog'),
    url(r'^add_blog_view/$', 'blog.views.add_blog_view'),
    url(r'^addcomment/(?P<post_id>\d+)/$', 'blog.views.add_comment'),
    # url(r'^simpleblog/', include('simpleblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)

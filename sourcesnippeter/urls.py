############################
# Home Urls Controller
############################

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sourcesnippeter.views.home', name='home'),
    url(r'^signup$', 'sourcesnippeter.views.sign_up', name='signup'),
    url(r'^signin$', 'sourcesnippeter.views.sign_in', name='signin'),
    url(r'^signout$', 'sourcesnippeter.views.sign_out', name='signout'),
    url(r'^social_signout$', 'sourcesnippeter.views.social_signout', name='social_signout'),
    url(r'^', include('snippetmanager.urls', namespace='snippetmanager')),
    # url(r'^sourcesnippeter/', include('sourcesnippeter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'costumes.views.home', name='home'),
    # url(r'^costumes/', include('costumes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^import/', 'main.views.import_req'),
    url(r'^$', 'main.views.index'),
    url('^cat/(?P<cat_id>(.*))/(?P<page>(.*))/', 'main.views.category'),
    url('^id/(?P<id>(.*))/', 'main.views.item'),
    url('^get/(?P<get>(.*))/', 'main.views.get'),
    url('^search/(?P<keyword>(.*))/(?P<page>(.*))/', 'main.views.search'),
    url('^s/(?P<cat_id>(.*))/(?P<sub_id>(.*))/(?P<page>(.*))/', 'main.views.sub_category'),
    url(r'^stats/', include('stats.urls')),

)

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'hackEdukate.core.views.home', name='home'),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'core/cover.html'}, name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup/$', 'hackEdukate.auth.views.signup', name='signup'),
    url(r'^settings/$', 'hackEdukate.core.views.settings', name='settings'),
    url(r'^settings/picture/$', 'hackEdukate.core.views.picture', name='picture'),
    url(r'^settings/upload_picture/$', 'hackEdukate.core.views.upload_picture', name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', 'hackEdukate.core.views.save_uploaded_picture', name='save_uploaded_picture'),
    url(r'^settings/password/$', 'hackEdukate.core.views.password', name='password'),
    url(r'^network/$', 'hackEdukate.core.views.network', name='network'),
    url(r'^feeds/', include('hackEdukate.feeds.urls')),
    url(r'^questions/', include('hackEdukate.questions.urls')),
    url(r'^articles/', include('hackEdukate.articles.urls')),
    url(r'^messages/', include('hackEdukate.messages.urls')),
    url(r'^notifications/$', 'hackEdukate.activities.views.notifications', name='notifications'),
    url(r'^notifications/last/$', 'hackEdukate.activities.views.last_notifications', name='last_notifications'),
    url(r'^notifications/check/$', 'hackEdukate.activities.views.check_notifications', name='check_notifications'),
    url(r'^search/$', 'hackEdukate.search.views.search', name='search'),
    url(r'^questions/isearch/$', 'hackEdukate.questions.views.isearch', name='isearch'),    
    url(r'^(?P<username>[^/]+)/$', 'hackEdukate.core.views.profile', name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

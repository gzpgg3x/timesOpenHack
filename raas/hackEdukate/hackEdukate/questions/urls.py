from django.conf.urls import patterns, include, url

urlpatterns = patterns('hackEdukate.questions.views',
    url(r'^$', 'questions', name='questions'),
    url(r'^isearch/$', 'isearch', name='isearch'),
    url(r'^auto_add_page/$', 'auto_add_page', name='auto_add_page'),    
    # url(r'^search/$', views.isearch, name='search'),    
    url(r'^answered/$', 'answered', name='answered'),
    url(r'^unanswered/$', 'unanswered', name='unanswered'),
    url(r'^all/$', 'all', name='all'),
    url(r'^ask/$', 'ask', name='ask'),
    url(r'^favorite/$', 'favorite', name='favorite'),
    url(r'^answer/$', 'answer', name='answer'),
    url(r'^answer/accept/$', 'accept', name='accept'),
    url(r'^answer/vote/$', 'vote', name='vote'),
    url(r'^(\d+)/$', 'question', name='question'),
)
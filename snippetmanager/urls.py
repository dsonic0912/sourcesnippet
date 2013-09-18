#################################
# SnippetManager Urls Controller
#################################

from django.conf.urls import patterns, include, url

from snippetmanager import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.snippet_world, name='snippetworld'),
    url(r'^snippetworld_sorted$', views.snippet_world_sorted, name='snippet_world_sorted'),
    url(r'^mysnippets$', views.my_snippets, name='mysnippets'),
    url(r'^new_snippet$', views.new_snippet, name='new_snippet'),
    url(r'^(?P<code_id>\d+)/edit_snippet$', views.edit_snippet, name='edit_snippet'),
    url(r'^new_project$', views.new_project, name='new_project'),
    url(r'^my_snippets_sorted$', views.my_snippets_sorted, name='my_snippets_sorted'),
    url(r'^(?P<code_id>\d+)/delete_snippet$', views.delete_snippet, name='delete_snippet'),
    url(r'^(?P<code_id>\d+)/public_snippet_detail$', views.public_snippet_detail, name='public_snippet_detail'),
    url(r'^disqus_comment$', views.disqus_comment, name='disqus_comment'),
    url(r'^(?P<improve_id>\d+)/improved_snippet_detail$', views.improved_snippet_detail, name='improved_snippet_detail'),
    url(r'^(?P<improve_id>\d+)/approve_snippet$', views.approve_snippet, name='approve_snippet'),
    url(r'^(?P<improve_id>\d+)/disapprove_snippet$', views.disapprove_snippet, name='disapprove_snippet'),
    url(r'^facebook_login$', views.facebook_login, name='facebook_login'),
    url(r'^google_login$', views.google_login, name='google_login'),
    url(r'^my_projects$', views.my_projects, name='my_projects'),
    url(r'^(?P<project_id>\d+)/delete_project$', views.delete_project, name='delete_project'),
    url(r'^facebook_like$', views.facebook_like, name='facebook_like'),
    url(r'^facebook_unlike$', views.facebook_unlike, name='facebook_unlike'),
)

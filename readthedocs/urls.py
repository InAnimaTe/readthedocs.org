from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from tastypie.api import Api

from readthedocs.api.base import (ProjectResource, UserResource,
                                  VersionResource, FileResource)
from readthedocs.core.views import HomepageView, SupportView

from readthedocs.core.urls import docs_urls, core_urls, deprecated_urls

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ProjectResource())
v1_api.register(VersionResource())
v1_api.register(FileResource())

admin.autodiscover()

handler500 = 'readthedocs.core.views.server_error'
handler404 = 'readthedocs.core.views.server_error_404'


urlpatterns = patterns(
    '',  # base view, flake8 complains if it is on the previous line.
    url(r'^$', HomepageView.as_view(), name='homepage'),
    url(r'^support/', SupportView.as_view(), name='support'),
    url(r'^security/', TemplateView.as_view(template_name='security.html')),
)

rtd_urls = patterns(
    '',
    url(r'^projects/', include('readthedocs.projects.urls.public')),
    url(r'^bookmarks/', include('readthedocs.bookmarks.urls')),
    url(r'^search/$', 'readthedocs.search.views.elastic_search', name='search'),
    url(r'^dashboard/', include('readthedocs.projects.urls.private')),
    url(r'^profiles/', include('readthedocs.profiles.urls.public')),
    url(r'^accounts/', include('readthedocs.profiles.urls.private')),
    url(r'^accounts/', include('allauth.urls')),
    # For redirects
    url(r'^builds/', include('readthedocs.builds.urls')),
)

api_urls = patterns(
    '',
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/v2/', include('readthedocs.restapi.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^websupport/', include('readthedocs.comments.urls')),
)

i18n_urls = patterns(
    '',
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

admin_urls = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

money_urls = patterns(
    '',
    url(r'^sustainability/', include('readthedocs.donate.urls')),
    url(r'^accounts/gold/', include('readthedocs.gold.urls')),
)

if not getattr(settings, 'USE_SUBDOMAIN', False):
    urlpatterns += docs_urls

urlpatterns += rtd_urls
urlpatterns += api_urls
urlpatterns += core_urls
urlpatterns += i18n_urls
urlpatterns += money_urls
urlpatterns += deprecated_urls

if getattr(settings, 'ALLOW_ADMIN', True):
    urlpatterns += admin_urls

if settings.DEBUG:
    urlpatterns += patterns(
        '',  # base view, flake8 complains if it is on the previous line.
        url('style-catalog/$',
            TemplateView.as_view(template_name='style_catalog.html')),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

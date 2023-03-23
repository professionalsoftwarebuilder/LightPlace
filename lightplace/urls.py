from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    #path('', include('admin.site.urls')),
    path('admin/', admin.site.urls),
    #path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('core.urls', namespace='core')),
    path('', include('contact.urls', namespace='contact')),
    #path('accounts/', include('accounts.urls', namespace='accounts')),
    path('chat/', include('chatApp.urls', namespace='chat')),
    path('avatar/', include('avatar.urls')),
    path('underconstruction/', TemplateView.as_view(template_name='underconstruction.html')),
    path('home/', TemplateView.as_view(template_name='landing.html'), name='home')
]

#urlpatterns += path('ckeditor/', include('ckeditor.urls'))

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

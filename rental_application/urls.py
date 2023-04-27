from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('property/', include('propertyManager.urls')),
    path('sms/', include("notification.urls")),
    path('',TemplateView.as_view(template_name="index.html")),
    path("auth/reset/",include("djoser.urls")),
    path('auth/social/', include('djoser.social.urls')),
    path('auth/token/', include('djoser.urls.jwt')), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

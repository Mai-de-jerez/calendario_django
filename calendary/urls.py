"""
URL configuration for calendary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from empleados.urls import empleados_patterns
from django.conf import settings
from messenger.urls import messenger_patterns
from profiles.urls import profiles_patterns
from eventos.urls import eventos_patterns 
from django.views.generic import RedirectView  

urlpatterns = [
    path("", include("core.urls")),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path("empleados/", include(empleados_patterns)),
    path("admin/", admin.site.urls),
    # Paths de Auth
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("registration.urls")),
    path('profiles/', include(profiles_patterns)),
    path('messenger/', include(messenger_patterns)),
    path('eventos/', include(eventos_patterns)),
    path('favicon.ico', RedirectView.as_view(url='/static/core/img/favicon.ico')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  

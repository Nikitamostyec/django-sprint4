"""
URL configuration for blogium project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from pages import views as pages_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    path("pages/", include("pages.urls", namespace="pages")),
    path(
        "auth/registration/",
        pages_views.RegistationView.as_view(),
        name="registration"
    ),
    path('auth/', include("django.contrib.auth.urls")),
    
    # path('auth/', include("users.urls")),

]


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error_view'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)

"""
URL configuration for main project.

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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns += [
    path('users/', include('apps.users.urls')),
    path('', include('apps.artists.urls')),
    path('', include('apps.tracks.urls')),
    path('', include('apps.playlists.urls')),
    path('', include('apps.podcasts.urls')),
    path('', include('apps.interactions.urls')),
    path('', include('apps.categories.urls')),
    path('', include('apps.subscriptions.urls')),
    path('', include('apps.albums.urls')),
    
    # path('', include('apps.group_sessions.urls')),
    # path('', include('apps.analytics.urls')),
    
]

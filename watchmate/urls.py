from django.contrib import admin
from django.urls import path, include
from watchlist_app.api import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include('watchlist_app.api.urls')),
    path('accounts/', include('user_app.api.urls')),
    # path('api-auth/', include('rest_framework.urls')),
]

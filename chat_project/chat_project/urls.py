from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls', namespace='chat')),
    path('taste/', include('taste_finder.urls')),
    path('destiny/', include('destiny_finder.urls')),
    path('fortune/', RedirectView.as_view(url='/destiny/')),
    path('', RedirectView.as_view(url='/chat/')),
]
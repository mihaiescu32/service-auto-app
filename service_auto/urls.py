from django.contrib import admin
from django.urls import path, include  # include e necesar pentru urls din app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('service.urls')),  # include toate URL-urile din app-ul 'service'
]
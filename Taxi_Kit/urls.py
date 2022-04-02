from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from chat.api.views import *
from taxi.api.views import *
from taxi.api.viewset import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)  # User api
router.register(r'thread', ThreadViewSet)
router.register(r'message', MessageViewSet)
urlpatterns = [
                  path('api/v1/', include(router.urls)),
                  path('api/v1/register/', save_registr),
                  path('api/v1/login/', login_view),
                  path('api/v1/accept/', accept_confirmation),
                  path('admin/', admin.site.urls),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

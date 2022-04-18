from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from chat.api.views import *
from drive.api.payments import ClickUzMerchantAPIView
from drive.api.views import *
from drive.api.viewset import *
from taxi.api.views import *
from taxi.api.viewset import *

router = routers.DefaultRouter()
router.register(r'thread', ThreadViewSet)
router.register(r'message', MessageViewSet)
router.register(r'driver', DriverViewSet)
router.register(r'tellme', TellMeViewSet)
router.register(r'faq', FaqViewSet)
urlpatterns = [
                  path('api/v1/', include(router.urls)),
                  path('api/v1/register/', save_register),
                  path('api/v1/login/', login_view),
                  path('api/v1/update_password/', update_password),
                  path('api/v1/accept/', accept_confirmation),
                  path('api/v1/order_creat/', order_creat),
                  path('api/v1/get-drivers/', get_drivers),
                  path('api/v1/tell/', tell_me),
                  path('api/v1/tell_us/', tell_us),
                  path('api/v1/delete/', delete),
                  path('api/v1/update/', update),
                  path('api/v1/user/', get_user),
                  path('click/', ClickUzMerchantAPIView.as_view()),
                  path('admin/', admin.site.urls),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

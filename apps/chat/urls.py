from django.urls import path, re_path
from apps.chat import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "chat"

urlpatterns = [
    path('room/', views.ChatRoom.as_view(), name="chat-room"),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name="chat-userprofile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

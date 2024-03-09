from django.urls import path
from apps.chat import views

app_name = "chat"

urlpatterns = [
    path('room/', views.ChatRoom.as_view(), name="chat-room"),

    # logout
    path("auth/logout/", views.ChatLogoutView.as_view(), name="logout"),
]

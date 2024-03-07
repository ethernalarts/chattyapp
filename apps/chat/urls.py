from django.urls import path
from apps.chat import views

app_name = "chat"

urlpatterns = [
    path('', views.ChatRoom.as_view(), name="chat-room"),
    # path("room/<int:course_id>/", views.chat_room, name="chat_room"),

    # logout
    path("auth/logout/", views.ChatLogoutView.as_view(), name="logout"),
]

from django.urls import path
from apps.chat import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = "chat"

urlpatterns = [
    path('room/', views.ChatRoom.as_view(), name="chat-room"),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name="chat-userprofile"),
    path('profile/<int:pk>/edit/', views.EditProfileView.as_view(), name="chat-editprofile"),

    # password change
    path(
        "password_change/",
        views.UserPasswordChangeView.as_view(),
        name="password_change",
    ),

    # password change done
    path(
        "password_change_done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),

    # delete account
    path(
        "delete_account/<int:pk>/",
        views.delete_user,
        name="delete-user",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from apps.chat import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("", views.index, name="index"),
    path("chat/", include("apps.chat.urls", namespace="chat")),

    # auth
    path("login/", views.ChatLoginView.as_view(), name="userlogin"),
    path("register/", views.CreateAccountView.as_view(), name="register"),
    path("logout/", views.ChatLogoutView.as_view(), name="userlogout"),

    # reset password
    path(
        "password_reset/",
        views.UserPasswordResetView.as_view(),
        name="password_reset"
    ),

    # password reset done
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    # password reset confirmation
    path(
        "accounts/reset/<uidb64>/<token>/",
        views.UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),

    # password reset complete
    path(
        "password_reset_complete/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # account deleted successfully
    path(
        "account_deleted/",
        TemplateView.as_view(
            template_name="account_deleted_success.html"
        ),
        name="account_deleted",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

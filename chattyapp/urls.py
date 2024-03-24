from django.contrib import admin
from django.urls import path, include
from apps.chat import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),

    path('', views.index, name="index"),
    path('chat/', include('apps.chat.urls', namespace='chat')),

    # auth
    path("login/", views.ChatLoginView.as_view(), name="login"),
    path("register/", views.CreateAccountView.as_view(), name="register"),
    path("logout/", views.ChatLogoutView.as_view(), name="logout"),
    # path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

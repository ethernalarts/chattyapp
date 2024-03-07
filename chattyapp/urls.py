from django.contrib import admin
from django.urls import path, include
from apps.chat import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),

    path('', views.index, name="index"),
    path('chat/', include('apps.chat.urls', namespace='chat')),

    # login
    path("auth/login/", views.ChatLoginView.as_view(template_name="login.html"), name="login"),
]

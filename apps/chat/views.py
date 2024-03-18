from django.contrib.auth import logout

# from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from apps.users.forms import CreateAccountForm


@login_required
def index(request):
    return HttpResponseRedirect(reverse("chat:chat-room"))


class ChatRoom(TemplateView):
    template_name = "chatroom.html"


class ChatLoginView(LoginView):
    redirect_authenticated_user = True
    redirect_field_name = "next"
    success_url = reverse_lazy("chat:chat-room")
    template_name = "login.html"
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            messages.success(
                self.request, f"You are logged in as {str(form.get_user()).upper()}"
            )
            return self.form_valid(form)
        else:
            messages.error(
                self.request,
                "Incorrect username or password. Note that both fields may be case-sensitive",
            )
            return self.form_invalid(form)


class ChatLogoutView(LogoutView):
    # template_name = 'logout-modal.html'
    redirect_field_name = "next"

    def get_success_url(self):
        messages.success(self.request, "You have been logged out")
        return self.request.META.get("HTTP_REFERER") or self.get_default_redirect_url()

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)


class CreateAccountView(CreateView):
    form_class = CreateAccountForm
    success_url = reverse_lazy("login")
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        try:
            # if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(self.request, f'Account has been created for {username}!')
            return self.form_valid(form)
        except Exception as e:
            messages.error(self.request, f'{e}')
            return self.form_invalid(form)
            # return render(request, "register.html", {'form': form})

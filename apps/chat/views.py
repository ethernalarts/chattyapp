from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from apps.users.forms import CreateAccountForm


@login_required
def index(request):
    return HttpResponseRedirect(reverse("chat:chat-room"))


class ChatRoom(TemplateView):
    template_name = "chatroom.html"


class ChatLoginView(LoginView):
    redirect_authenticated_user = True
    redirect_field_name = "next"
    success_url = "chatroom.html"
    template_name = "login.html"
    fields = "__all__"

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, f"{error}")
        return self.render_to_response(self.get_context_data(form=form))


class ChatLogoutView(LogoutView):
    redirect_field_name = "next"

    def get_success_url(self):
        messages.success(self.request, "You have been logged out")
        return self.get_redirect_url() or self.get_default_redirect_url()


class CreateAccountView(CreateView):
    form_class = CreateAccountForm
    success_url = reverse_lazy("login")
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(self.request, f"Account has been created for {username}")
            return self.form_valid(form)
        else:
            for error in form.errors:
                messages.error(self.request, f'{error}')
            return self.form_invalid(form)
            # return render(request, "register.html", {'form': form})

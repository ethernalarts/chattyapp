from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView

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


class CreateAccountView(FormView):
    form_class = CreateAccountForm
    success_url = reverse_lazy("login")
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(self.request, f"Account has been created for {str(username)}")
            return self.form_valid(form)
        else:
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                messages.error(self.request, "Your passwords do not match")
                return self.form_invalid(form)
            for error in form.non_field_errors():
                messages.error(self.request, f"{error}")
            return self.form_invalid(form)


def register_user(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()  # Save user to Database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}!')
            return redirect('login')
        else:
            for error in form.errors():
                messages.error(request, f'{error}')
            form = CreateAccountForm()
    else:
        form = CreateAccountForm()
    return render(request, 'registration/register.html', {'form': form})

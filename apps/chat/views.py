from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib.auth import login

from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from apps.users.models import Profile
from apps.users.forms import CreateAccountForm, UserUpdateForm, ProfileUpdateForm


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
    model = User

    def form_valid(self, form):
        user = form.get_user()
        if user:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())

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
    template_name = "register.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.password_check(form)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"Account has been created for {str(username)}")
        return HttpResponseRedirect(self.get_success_url())

    def password_check(self, form):
        password1 = self.request.POST.get("password1")
        password2 = self.request.POST.get("password2")

        if password1 != password2:
            messages.error(self.request, "Your passwords do not match")
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, f"{error}")
        return self.render_to_response(self.get_context_data(form=form))


class ProfileView(LoginRequiredMixin, UpdateView):
    redirect_authenticated_user = True
    form_class = UserUpdateForm
    second_form_class = ProfileUpdateForm
    template_name = "profile.html"
    redirect_field_name = "next"
    success_url = "chatroom.html"
    model = User

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_success_url(self):
        return self.get_redirect_url() or self.get_default_redirect_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_client"] = True
        if "userform" not in context:
            context["userform"] = self.form_class(self.request.GET)
        if "profileform" not in context:
            context["profileform"] = self.second_form_class(self.request.GET)
        return context

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        userform = self.form_class
        profileform = self.second_form_class
        return self.render_to_response(
            self.get_context_data(
                object=self.object, userform=userform, profileform=profileform
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        userform = self.form_class(request.POST)
        profileform = self.second_form_class(request.POST)

        if userform.is_valid() and profileform.is_valid():
            userdata = userform.save(commit=False)
            userdata.save()
            profiledata = profileform.save(commit=False)
            profiledata.user = userdata
            profiledata.save()
            messages.success(self.request, "Profile Updated")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(userform=userform, profileform=profileform)
            )

    # def form_invalid(self, form):
    #     userform = self.form_class
    #     profileform = self.second_form_class
    #
    #     if userform.non_field_errors(self):
    #         for error in userform.non_field_errors(self):
    #             messages.error(self.request, f"{error}")
    #     if profileform.non_field_errors(self):
    #         for error in userform.non_field_errors():
    #             messages.error(self.request, f"{error}")
    #     return self.render_to_response(
    #         self.get_context_data(userform=userform, profileform=profileform)


@login_required
def profile(request):
    if request.method == "POST":
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your profile has been updated")
            return redirect("chat-profile")  # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "users/profile.html", context)

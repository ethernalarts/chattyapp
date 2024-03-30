from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login

from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (
    TemplateView,
    UpdateView,
    DetailView,
    CreateView,
    FormView,
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from apps.users.forms import *


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
        try:
            user = form.get_user()
            login(self.request, user)
            username = User.objects.get(id=self.request.user.id).username
            messages.success(self.request, f"Welcome, {str(username)}")
            return HttpResponseRedirect(self.get_success_url())
        except ObjectDoesNotExist:
            messages.error(self.request, "This user does not exist")
            return self.form_invalid(form)

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
    second_form_class = ProfileForm
    success_url = reverse_lazy("login")
    template_name = "register.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super(CreateAccountView, self).get_context_data(**kwargs)
        context["form"] = self.form_class(self.request.GET)
        context["profileform"] = self.second_form_class(self.request.GET)
        return context

    def form_valid(self, form):
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        username = form.cleaned_data.get("username")

        self.password_check(password1, password2)

        user = form.save()
        profile_form = self.second_form_class(
            self.request.POST,
            self.request.FILES,
            instance=user.profile
        )

        if profile_form.is_valid():
            profile_form.save()
            messages.success(
                self.request,
                f"Welcome, {str(username)}. Your account has been created, please log in to start chatting",
            )
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(profile_form)

    def password_check(self, password1, password2):
        if password1 != password2:
            messages.error(self.request, "Your passwords do not match")
            return self.render_to_response(
                self.get_context_data(
                    userform=self.form_class(self.request.POST),
                    profileform=self.second_form_class(self.request.POST),
                )
            )

    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, f"{error}")
        return self.render_to_response(
            self.get_context_data(
                userform=self.form_class(self.request.GET),
                profileform=self.second_form_class(self.request.GET),
            )
        )


class ProfileView(DetailView):
    model = User
    form_class = UserUpdateForm
    second_form_class = ProfileForm
    template_name = "profile.html"
    context_object_name = "obj"

    def get_object(self, queryset=None):
        try:
            return User.objects.get(id=self.kwargs["pk"])
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("The request Object does not exist")

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["userform"] = self.form_class(self.request.GET)
        context["profileform"] = self.second_form_class(instance=self.object)
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    redirect_authenticated_user = True
    form_class = UserUpdateForm
    second_form_class = ProfileForm
    template_name = "editprofile.html"
    redirect_field_name = "next"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_object(self, queryset=None):
        try:
            return User.objects.get(id=self.kwargs["pk"])
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("The request Object does not exist")

    def get_success_url(self):
        return self.get_object().profile.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_client"] = True
        if "userform" not in context:
            context["userform"] = self.form_class(self.request.GET)
        if "profileform" not in context:
            context["profileform"] = self.second_form_class(
                instance=self.object.profile
            )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        userform = self.form_class(self.request.POST, instance=self.request.user)
        profileform = self.second_form_class(
            request.POST or None,
            request.FILES or None,
            instance=self.request.user.profile,
        )
        # profile_instance = get_object_or_404(Profile, user=self.request.user)

        if userform.is_valid() and profileform.is_valid():
            userdata = userform.save(commit=False)
            userdata.save()
            profiledata = profileform.save(commit=False)
            profiledata.save()
            messages.success(self.request, "Your profile has been updated")
            return self.form_valid(profileform)
        else:
            return self.form_invalid(profileform)

    def form_invalid(self, profileform):
        for error in profileform.non_field_errors():
            messages.error(self.request, f"{error}")
            return self.render_to_response(
                self.get_context_data(
                    userform=self.form_class(self.request.GET),
                    profileform=self.second_form_class(instance=self.object.profile),
                )
            )

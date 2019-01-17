"""Views for users application."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    """View for a single user."""

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


class UserListView(LoginRequiredMixin, ListView):
    """View for a list of users."""

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user data."""

    model = User
    fields = ["name"]

    def get_success_url(self):
        """URL to route to on successful update."""
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        """Object to perform update with."""
        return User.objects.get(username=self.request.user.username)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """View for redirecting to a user's webpage."""

    permanent = False

    def get_redirect_url(self):
        """URL to redirect to."""
        return reverse("users:detail", kwargs={"username": self.request.user.username})

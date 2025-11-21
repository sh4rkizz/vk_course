from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.contrib import messages

from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy

from sem4.forms import LoginForm, UserForm


def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse("sem4:profile"))

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse("sem4:profile"))
        print(form.errors)

    return render(request, "sem4/pages/better-profile.html", {"form": form})


class LoginView(FormView):
    form_class = LoginForm
    template_name = "sem4/pages/better-profile.html"

    def form_valid(self, form):
        user = auth.authenticate(self.request, **form.cleaned_data)
        if user:
            auth.login(self.request, user)
            return HttpResponseRedirect(reverse("sem4:profile"))

        form.add_error(None, "Неверный логин или пароль")
        return self.form_invalid(form)


@login_required(login_url=reverse_lazy("sem4:login"))
def profile_view(request):
    return render(request, "sem4/pages/profile.html")


class ProfileView(FormView):
    form_class = UserForm
    template_name = "sem4/pages/better-profile.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('sem4:profile')

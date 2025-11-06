from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from rest_framework.generics import RetrieveAPIView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

def index_view(request):
    if request.user.is_authenticated:
        questions = []
        for i in range(50):
            questions.append({
                "id": i,
                "text": f"LONG_TEXT {i}",
                "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Facere sunt reiciendis iure dolor ex, cumque laborum quibusdam repudiandae distinctio ipsum rem aut. Fuga odio nam assumenda amet. Nam, eaque eos."
            })
        page_number = request.GET.get("page", 1)
        page = Paginator(questions, per_page=5)

        object_list = page.page(page_number)
        return render(request, "index.html", context={"object_list": object_list, "page_obj": page})
    return HttpResponseRedirect(reverse("admin:login"))



class ButtonPressenView(ListAPIView):
    permission_classes = [IsAuthenticated]


class DetailView(TemplateView):
    template_name = "detail.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("admin:login"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from gramm.models import Post
from django.db.models import Count


def index_post_view(request):
    # try:
    #     post = Post.objects.get(id=1)
    # except ObjectDoesNotExist:
    #     raise Http404()

    post = Post.objects.filter(id=1, title__icontains="ПОМОГИТЕ").first()

    if post is None:
        raise Http404()

    # posts = Post.objects.visible_for(request.user).order_by("-created_at").only("title", "content")
    # if request.GET.get('hot'):
    #     posts = posts.annotate(comments_cnt=Count("comments")).order_by("-comments_cnt", "-created_at")
    # return render(request, "post_index.html", context={"posts": posts})

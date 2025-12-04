from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sem5.forms import ImageForm
from sem5.models import Image, ImageLike

from rest_framework.views import APIView


@login_required
def index_view(request):
    form = ImageForm(request.user.pk)

    if request.method == "POST":
        form = ImageForm(request.user.pk, request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

    images = Image.objects.filter(author_id=request.user.pk)
    return render(request, template_name="sem5/index.html", context={"form": form, "images": images})


class LikeImageView(APIView):
    def post(self, request, *args, **kwargs):
        image = Image.objects.filter(id=kwargs["id"])
        if image is None:
            raise Http404()

        image.likes_cnt = Image.likes.count()
        image.save(update_fields=["likes_cnt"])

        return JsonResponse({
            "created": True,
            "likes_cnt": image.likes_cnt
        }, status=200)

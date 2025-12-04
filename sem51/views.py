from django.http import Http404, JsonResponse
from django.views import View
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required

from sem51.forms import UserImageForm
from sem51.models import UserImage, UserImageLike

from django.db import IntegrityError




@login_required
def index_view(request):
    form = UserImageForm(request.user.pk)
    if request.method == "POST":
        form = UserImageForm(request.user.pk, request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

    user_images = UserImage.objects \
        .select_related("author") \
        .filter(author_id=request.user.pk)

    return render(request, template_name="sem51/index.html", context={"form": form, "user_images": user_images})


class LikeImageView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404()

        image_id = kwargs["id"]
        image = UserImage.objects.filter(id=image_id).first()

        if image is None:
            raise Http404()

        UserImageLike.objects.leave_like(image=image, user=request.user)
        image.likes_cnt = image.likes.filter(is_active=True).count()
        image.save(update_fields=["likes_cnt"])

        return JsonResponse({"status": "ok", "new_likes_count": image.likes_cnt}, status=200)

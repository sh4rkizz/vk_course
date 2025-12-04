from django import forms
from sem51.models import UserImage


class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ["title", "file"]

    def __init__(self, author_id, *args, **kwargs):
        self.author_id = author_id
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(False)
        instance.author_id = self.author_id

        profile = getattr(instance, "profile", None)
        if profile is None:
            profile = instance.create_profile()

        if commit:
            instance.save()
        return instance

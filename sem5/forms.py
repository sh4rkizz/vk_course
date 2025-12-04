from django import forms

from sem5.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "file"]

    def __init__(self, author_id, *args, **kwargs):
        self.author_id = author_id
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(False)
        instance.author_id = self.author_id
        print(self.author_id)
        if commit:
            instance.save()
        return instance

from django.forms import ModelForm, FileInput, ValidationError
from sheets.models import Attempt, Sheet


class SheetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["img"].label = "Image"

    class Meta:
        model = Sheet
        fields = ["name", "img", "sheet_url"]
        widgets = {
            "img": FileInput(attrs={"accept": "image/png", "label": "Image"}),
        }


class AttemptForm(ModelForm):
    class Meta:
        model = Attempt
        fields = [
            "audio",
        ]
        widgets = {
            "audio": FileInput(attrs={"accept": "audio/*"}),
        }

from django import forms
from .models import task  # importamos todo contenido de la tabla (models): "task"


class TaskForm(forms.ModelForm):
    class Meta:
        model = task
        fields = ["title", "description", "important"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Write a title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write a description",
                    "rows": 5,
                    "cols": 40,
                }
            ),
            "important": forms.CheckboxInput(
                attrs={"class": "form-check-input m-auto inline"}
            ),
        }

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_bootstrap5.bootstrap5 import BS5Accordion
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Task, Team


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Workers"
    )

    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-light border border-dark',
                'rows': 4
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-light border border-dark'
            }),
            'is_complete': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control bg-light border border-dark',
                'type': 'datetime-local'
            }),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now():
            raise forms.ValidationError("Deadline cannot be in the past!")
        return deadline

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))

        self.helper.layout = Layout(
            BS5Accordion(
                Fieldset(
                    "Task Info",
                    Field('name', template="bootstrap5/field.html"),
                    Field('description', template="bootstrap5/field.html"),
                    Field('deadline', template="bootstrap5/field.html"),
                    Field('is_complete', template="bootstrap5/field.html")
                ),
                Fieldset(
                    "Task Details",
                    Field('priority', template="bootstrap5/field.html"),
                    Field('task_type', template="bootstrap5/field.html"),
                    Field('assignees', template="bootstrap5/field.html"),
                    Field('team', template="bootstrap5/field.html")
                )
            )
        )


class TeamForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Workers"
    )

    class Meta:
        model = Team
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-light border border-dark',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-light border border-dark',
                'rows': 4
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))

        self.helper.layout = Layout(
            BS5Accordion(
                Fieldset(
                    "Team Info",
                    Field('name', template="bootstrap5/field.html"),
                    Field('description', template="bootstrap5/field.html"),
                    Field('workers', template="bootstrap5/field.html"),
                )
            )
        )

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from crispy_forms import bootstrap, helper, layout

from myproject.apps.categories2.models import Category

from .models import Idea, RATING_CHOICES

User = get_user_model()


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        exclude = ["author"]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        self.fields["categories"].widget = forms.CheckboxSelectMultiple()

        title_field = layout.Field("title")
        content_field = layout.Field("content", rows="3")
        main_fieldset = layout.Fieldset(_("Main data"), title_field, content_field)

        picture_field = layout.Field("picture")
        format_html = layout.HTML(
            """{% include "ideas2/includes/picture_guidelines.html" %}"""
        )

        picture_fieldset = layout.Fieldset(
            _("Picture"),
            picture_field,
            format_html,
            title=_("Image upload"),
            css_id="picture_fieldset",
        )

        categories_field = layout.Field("categories")
        categories_fieldset = layout.Fieldset(
            _("Categories"), categories_field, css_id="categories_fieldset"
        )

        submit_button = layout.Submit("save", _("Save"))
        actions = bootstrap.FormActions(submit_button)

        self.helper = helper.FormHelper()
        self.helper.form_action = self.request.path
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            main_fieldset,
            picture_fieldset,
            categories_fieldset,
            actions,
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.request.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class IdeaFilterForm(forms.Form):
    author = forms.ModelChoiceField(
        label=_("Author"),
        required=False,
        queryset=User.objects.annotate(
            idea_count=models.Count("authored_ideas")
        ).filter(idea_count__gt=0),
    )
    category = forms.ModelChoiceField(
        label=_("Category"),
        required=False,
        queryset=Category.objects.annotate(
            idea_count=models.Count("category_ideas")
        ).filter(idea_count__gt=0),
    )
    rating = forms.ChoiceField(
        label=_("Rating"), required=False, choices=RATING_CHOICES
    )

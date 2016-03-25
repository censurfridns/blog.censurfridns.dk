from django import forms
from django.conf import settings


class AdminCSVExportForm(forms.Form):
    language = forms.HiddenField()
    next = forms.HiddenField()

    def clean(self):
        cleaned_data = super(SetLanguageForm, self).clean()
        
        ### validate language
        if cleaned_data['language'] not in settings.PRIMARY_LANGUAGE_DOMAINS:
            del cleaned_data["language"]
            self._errors["language"] = self.error_class([_("Invalid language")])

        ### return cleaned_data
        return cleaned_data


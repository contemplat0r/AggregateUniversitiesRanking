from django import forms

class SelectRankingsNamesAndYear(forms.Form):
    select_rankings_names_field = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=())
    select_year_field = forms.ChoiceField(required=False, widget=forms.Select, choices=())

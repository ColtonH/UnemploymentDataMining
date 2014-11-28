from django import forms
from data.models import UsState, UnemploymentByStateMonthly
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django.db.models import Max, Min
from django.core.exceptions import ValidationError

class ClusteringOptionsForm(forms.Form):
    states = forms.ModelMultipleChoiceField(queryset=UsState.objects.all().order_by('name'),required=False)
    years = forms.MultipleChoiceField(choices=(), required=False)
    normalize_data = forms.BooleanField(required=False,initial=False)
    # number_of_clusters = forms.
    def __init__(self, *args, **kwargs):
        year_choices=None
        if 'year_choices' in kwargs.keys():
            year_choices = kwargs.pop('year_choices')
        super(ClusteringOptionsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))
        if year_choices:
            self.fields['years'].choices = year_choices
    def getMinYear(self):
        return self.fields['starting_year'].choices[0][0]
    def getMaxYear(self):
        return self.fields['starting_year'].choices[-1][0]
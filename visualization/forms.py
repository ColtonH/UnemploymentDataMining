from django import forms
from data.models import UsState, UnemploymentByStateMonthly
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django.db.models import Max, Min
from django.core.exceptions import ValidationError

class UsStateSelectForm(forms.Form):
    name = forms.ModelMultipleChoiceField(queryset=UsState.objects.all().order_by('name'))
    def __init__(self, *args, **kwargs):
        super(UsStateSelectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))

# class UsStateSelectFormMortality(forms.Form):
#     name = forms.ModelMultipleChoiceField(queryset=UsState.objects.all().order_by('name'))
#     def __init__(self, *args, **kwargs):
#         super(UsStateSelectForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.form_class = 'form-horizontal'
#         self.helper.label_class = 'col-lg-2'
#         self.helper.field_class = 'col-lg-8'
#         self.helper.form_action = '/visualization/timeseries/num_births'
#         self.helper.add_input(Submit('submit', 'Submit'))

NUM_SAMPLES_CHOICES = (
    ('10', '10'),
    ('25', '20'),
    ('50', '50'),
    ('100', '100'),
    ('200', '200'),
)
K_CHOICES = (
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),      
)

KMEANS_METHOD_CHOICES = (
    ('Basic','Basic kmeans'),
    ('Bisective','Bisecting kmeans'),
)
class kmeansNumSamplesForm(forms.Form):
    num_samples = forms.ChoiceField(choices=NUM_SAMPLES_CHOICES)
    k = forms.ChoiceField(choices=K_CHOICES)
    method = forms.ChoiceField(choices=KMEANS_METHOD_CHOICES)
    def __init__(self, *args, **kwargs):
        super(kmeansNumSamplesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_action = '/visualization/playground/kmeans'
        self.helper.add_input(Submit('submit', 'Submit'))

AGGREGATION_CHOICES=(
    ('mean','Mean (Average)'),
    ('min','Minimum'),
    ('max','Maximum'),
    ('sum','Sum of all values'),
    )

class YearlyMapAggregationForm(forms.Form):
    starting_year = forms.ChoiceField(choices=(),required=False)
    ending_year = forms.ChoiceField(choices=(),required=False)
    aggregation_method = forms.ChoiceField(choices=AGGREGATION_CHOICES,initial='mean')
    def __init__(self, *args, **kwargs):
        year_choices=None
        if 'year_choices' in kwargs.keys():
            year_choices = kwargs.pop('year_choices')
        super(YearlyMapAggregationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))
        if year_choices:
            self.fields['starting_year'].choices = year_choices
            self.fields['ending_year'].choices = year_choices
    def getMinYear(self):
        return self.fields['starting_year'].choices[0][0]
    def getMaxYear(self):
        return self.fields['starting_year'].choices[-1][0]
    def clean_ending_year(self):
        ending_year = self.cleaned_data["ending_year"]
        starting_year = self.cleaned_data["starting_year"]
        if (ending_year<starting_year):
            raise ValidationError("Ending year must be greater or equal than starting year")
        return ending_year
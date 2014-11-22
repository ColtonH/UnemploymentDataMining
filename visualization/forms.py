from django import forms
from data.models import UsState, UnemploymentByStateMonthly
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django.db.models import Max, Min
from django.core.exceptions import ValidationError

class UsStateSelectForm(forms.Form):
    name = forms.ModelChoiceField(queryset=UsState.objects.all().order_by('name'))
    def __init__(self, *args, **kwargs):
        super(UsStateSelectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_action = '/visualization/single/unemployment'
        self.helper.add_input(Submit('submit', 'Submit'))

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
        self.helper.form_action = '/visualization/kmeans'
        self.helper.add_input(Submit('submit', 'Submit'))

AGGREGATION_CHOICES=(
    ('mean','Mean (Average)'),
    ('min','Minimum'),
    ('max','Maximum'),
    ('sum','Sum of all values'),
    )
def getYearChoices():
    max_min_year = UnemploymentByStateMonthly.objects.values('state').annotate( max_year=Max('year'), min_year = Min('year')).values('min_year','max_year')
    year_choices=()
    if max_min_year:
        year_choices= [(i,i) for i in range(int(max_min_year[0]['min_year']),int(max_min_year[0]['max_year']))]
        year_choices.insert(0,('',''))
        year_choices = tuple(year_choices)
    return year_choices
class UnemploymentByStateForm(forms.Form):
    starting_year = forms.ChoiceField(choices=getYearChoices(),initial='',required=False)
    ending_year = forms.ChoiceField(choices=getYearChoices(),initial='',required=False)
    aggregation_method = forms.ChoiceField(choices=AGGREGATION_CHOICES,initial='mean')
    def __init__(self, *args, **kwargs):
        super(UnemploymentByStateForm, self).__init__(*args, **kwargs)
        self.ini_year = getYearChoices()[1][0]
        self.end_year = getYearChoices()[-1][0]
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-8'
        self.helper.form_action = '/visualization/unemployment_map'
        self.helper.add_input(Submit('submit', 'Submit'))
    def getMinYear(self):
        return self.ini_year
    def getMaxYear(self):
        return self.end_year
    def clean_ending_year(self):
        ending_year = self.cleaned_data["ending_year"]
        starting_year = self.cleaned_data["starting_year"]
        if (ending_year<starting_year):
            raise ValidationError("Ending year must be greater or equal than starting year")
        return ending_year
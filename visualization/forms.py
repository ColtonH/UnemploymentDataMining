from django import forms
from data.models import UsState
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

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
class kmeansNumSamplesForm(forms.Form):
    num_samples = forms.ChoiceField(choices=NUM_SAMPLES_CHOICES)
    k = forms.ChoiceField(choices=K_CHOICES)
    def __init__(self, *args, **kwargs):
        super(kmeansNumSamplesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_action = '/visualization/kmeans'
        self.helper.add_input(Submit('submit', 'Submit'))
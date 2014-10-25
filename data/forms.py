from django import forms
from models import UsState
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

# class UsStateForm(ModelForm):
#     name = forms.ModelChoiceField(queryset=UsState.objects.all().order_by('name'))
#     def __init__(self, *args, **kwargs):
#         super(UsStateForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-exampleForm'
#         self.helper.form_class = 'blueForms'
#         self.helper.form_method = 'post'
#         self.helper.form_action = '.'

#         self.helper.add_input(Submit('submit', 'Submit'))
#     class Meta:
#         model = UsState
#         # fields=['name',]
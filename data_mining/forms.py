from django import forms
from data.models import UsState, UnemploymentByStateMonthly, Crisis
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django.db.models import Max, Min
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div

CLUSTERING_CHOICES=(
    ('AgglomerativeClustering','Agglomerative Clustering (WARD,with kneighbours connectivity)'),
    ('KMeans','k-means'),
    # ('DBSCAN','DBSCAN'), #Not ready
    ('AffinityPropagation','Affinity Propagation'),
    ('MeanShift','Mean Shift'),
)
MAX_NUM_CLUSTERS = 10

class ClusteringOptionsForm(forms.Form):
    states = forms.ModelMultipleChoiceField(queryset=UsState.objects.all().order_by('name'),required=False)
    years = forms.MultipleChoiceField(choices=(), required=False)
    normalize_data = forms.BooleanField(label='Normalize data (Featue scaling)',required=False,initial=True)
    unemployment_difference = forms.BooleanField(required=False,initial=False)
    variable_difference = forms.BooleanField(required=False,initial=True)
    clustering_algorithm = forms.ChoiceField(choices=CLUSTERING_CHOICES, initial='AgglomerativeClustering')
    number_of_clusters = forms.IntegerField(initial=2)
    def __init__(self, *args, **kwargs):
        year_choices=None
        if 'year_choices' in kwargs.keys():
            year_choices = kwargs.pop('year_choices')
        if 'form_url' in kwargs.keys():
            form_url = kwargs.pop('form_url')
        else:
            form_url = ''

        super(ClusteringOptionsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_action = form_url
        # self.helper.add_input(Submit('submit', 'Submit'))
        if year_choices:
            self.fields['years'].choices = year_choices
        self.helper.layout = Layout(
            Fieldset(
               '',
               'states',
               'years',
               'normalize_data','unemployment_difference','variable_difference',
               'clustering_algorithm','number_of_clusters',
            ),
            Div(
               Submit('submit', 'Submit', css_class='btn btn-default'),
               css_class='col-lg-offset-4 col-lg-8',
            )
        )
    def getMinYear(self):
        return self.fields['starting_year'].choices[0][0]
    def getMaxYear(self):
        return self.fields['starting_year'].choices[-1][0]
    def clean_number_of_clusters(self):
        number_of_clusters = self.cleaned_data['number_of_clusters']
        if number_of_clusters>MAX_NUM_CLUSTERS or number_of_clusters<1:
            raise ValidationError('The number of clusters must be >=1 and <=%d'%(MAX_NUM_CLUSTERS))
        return number_of_clusters
    def clean_years(self):
        cleaned_years = self.cleaned_data['years']
        selected = len(cleaned_years)
        if selected>0 and selected<5:
            raise ValidationError('Please select at least 5 years')
        for i in range (1,selected):
            if int(cleaned_years[i])-int(cleaned_years[i-1])!=1:
                raise ValidationError('Years must be consecutive')
        return cleaned_years
class SingleUsStateSelectForm(forms.Form):
    name = forms.ModelChoiceField(queryset=UsState.objects.all().order_by('name'))
    def __init__(self, *args, **kwargs):
        super(SingleUsStateSelectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))

Z_THRESHOOLD_CHOICES = (
    (1.5,'1.5 standard deviations'),
    (3.0,'3 standard deviations')
    )
class SingleCrisisYearSelectForm(forms.Form):
    cData = Crisis.objects.values('year').filter(crisis=True).order_by('year')
    cYears = []
    for item in cData:
        cYears.append((str(item['year']),str(item['year'])))
    year = forms.ChoiceField(choices=cYears, initial=cYears[0])
    threshold = forms.ChoiceField(choices=Z_THRESHOOLD_CHOICES,required=True, initial = 1.5)
   
    def __init__(self, *args, **kwargs):
        super(SingleCrisisYearSelectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))
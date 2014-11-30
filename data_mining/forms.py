from django import forms
from data.models import UsState, UnemploymentByStateMonthly
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django.db.models import Max, Min
from django.core.exceptions import ValidationError

CLUSTERING_CHOICES=(
    ('KMeans','k-means'),
    ('DBSCAN','DBSCAN'),
    ('AffinityPropagation','Affinity Propagation'),
    ('AgglomerativeClustering','Agglomerative Clustering (WARD,with kneighbours connectivity)'),
    ('MeanShift','Mean Shift'),
)
MAX_NUM_CLUSTERS = 8

class ClusteringOptionsForm(forms.Form):
    states = forms.ModelMultipleChoiceField(queryset=UsState.objects.all().order_by('name'),required=False)
    years = forms.MultipleChoiceField(choices=(), required=False)
    normalize_data = forms.BooleanField(required=False,initial=False)
    clustering_algorithm = forms.ChoiceField(choices=CLUSTERING_CHOICES, initial='KMeans')
    number_of_clusters = forms.IntegerField(initial=2)
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
    def clean_number_of_clusters(self):
        number_of_clusters = self.cleaned_data['number_of_clusters']
        if number_of_clusters>MAX_NUM_CLUSTERS or number_of_clusters<2:
            raise ValidationError('The number of clusters must be >=2 and <=%d'%(MAX_NUM_CLUSTERS))
        return number_of_clusters
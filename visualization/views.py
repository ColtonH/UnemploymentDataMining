from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from data.models import UnemploymentByStateMonthly, UsState
from forms import UsStateSelectForm, kmeansNumSamplesForm, UnemploymentByStateForm
from django.template import RequestContext
from django.db.models import Avg, Max, Min, Sum
import numpy
# Import Michael's implementation for kmeans
import kmeans
def index(request):
    return render_to_response('visualization/index.html', {
        }, context_instance=RequestContext(request))


def single_unemployment(request):
    state=None
    data = None
    form = UsStateSelectForm()
    if request.method == 'POST':
        form = UsStateSelectForm(request.POST)
        if form.is_valid():
            state = get_object_or_404(UsState, name=form.cleaned_data['name'])
            data = UnemploymentByStateMonthly.objects.filter(state= state ).order_by('year','month')
    
    return render_to_response('visualization/linechart.html', {
        'data': data,
        'form':form,
        'state': state
        }, context_instance=RequestContext(request))

def kmeans_test(request):
    data = None
    form = kmeansNumSamplesForm()
    k=None
    sample_size=None
    grouped_data = None
    clusters = None
    error_list = None
    if request.method=='POST':
        form = kmeansNumSamplesForm(request.POST)
        if form.is_valid():
            sample_size = int(form.cleaned_data['num_samples'])
            k = int(form.cleaned_data['k'])
            # Generate random data
            data = numpy.random.random((sample_size, 2)) 
            # Calculate kmeans
            if form.cleaned_data['method']=='Basic':
                grouped_data, clusters, error_list = kmeans.kmeans(data,num_clusters=k, min_error=0.01, max_iter=100)
            else:
                grouped_data, clusters, error_list = kmeans.bisecting_kmeans(data,k=k, min_error=0.01, max_iter=50)
    return render_to_response('visualization/kmeans.html', {
        'data': grouped_data,
        'clusters': clusters,
        'error_list': error_list,
        'form':form,
        'k': k,
        'sample_size': sample_size,
        }, context_instance=RequestContext(request))

def unemployment(request):
    form = UnemploymentByStateForm()
    max_year = form.getMaxYear()
    min_year = form.getMinYear()
    
    if request.method=='POST':
        form = UnemploymentByStateForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["starting_year"]!='':
                min_year = form.cleaned_data["starting_year"]
            if form.cleaned_data["ending_year"]!='':        
                max_year = form.cleaned_data["ending_year"]
            data = UnemploymentByStateMonthly.objects.filter(year__gte=min_year,year__lte=max_year).select_related('state__code').values('state','state__code')
            method = form.cleaned_data["aggregation_method"]
            if method=='mean':
                data=data.annotate(value=Avg('value'))
            elif method=="min":
                data=data.annotate(value=Min('value'))
            elif method=="max":
                data=data.annotate(value=Max('value'))
            elif method=="sum":
                data=data.annotate(value=Sum('value'))

        else:
            return render_to_response('visualization/unemployment_map.html', {
                'data': None,
                'form':form,
                'title':"Please check form errors",
                }, context_instance=RequestContext(request))
        
    else:    
        data = UnemploymentByStateMonthly.objects.select_related('state__code').values('state','state__code').annotate(value=Avg('value'))
    title = "Unemployment in the US ("+str(min_year)+"-"+str(max_year)+") [Average]" 
    return render_to_response('visualization/unemployment_map.html', {
        'data': data,
        'form':form,
        'title':title,
        }, context_instance=RequestContext(request))

def unemployment_json(request):
    pass
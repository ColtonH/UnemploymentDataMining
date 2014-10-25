from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from data.models import UnemploymentByStateMonthly, UsState
from forms import UsStateSelectForm, kmeansNumSamplesForm
from django.template import RequestContext
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
            grouped_data, clusters, error_list = kmeans.kmeans(data,num_clusters=k, min_error=0.01, max_iter=100)
    return render_to_response('visualization/kmeans.html', {
        'data': grouped_data,
        'clusters': clusters,
        'error_list': error_list,
        'form':form,
        'k': k,
        'sample_size': sample_size,
        }, context_instance=RequestContext(request))
from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from data.models import UnemploymentByStateMonthly, UsState, NatalityByStateYearly, MortalityByStateYearly
from forms import ClusteringOptionsForm, SingleUsStateSelectForm
from visualization.forms import UsStateSelectForm
from sklearn.cluster import KMeans, DBSCAN, AffinityPropagation, AgglomerativeClustering,MeanShift, Ward
from sklearn.cluster.bicluster import SpectralCoclustering
import numpy as np
import matplotlib.pyplot as plt
import os
import uuid
from itertools import cycle
from django.conf import settings
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics import pairwise_distances
from django.db.models import Avg, Max, Min, Sum
#DB queries from Michael
import dbqueries
# Statistical Association from John
import stat_association
PLOTS_TEMP_FOLDER = 'tmp/plots/'
def index(request):
    return render_to_response('data_mining/index.html', {}, context_instance=RequestContext(request))



# Clustering uses library scikit-learn, view http://scikit-learn.org/stable/modules/clustering.html
def cluster_data(data,clustering_method,num_clusters):
    cluster_centers = labels_unique = labels = extra = None
    if clustering_method == 'KMeans':
        # http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
        k_means = KMeans(n_clusters=num_clusters,init='k-means++',n_init=10,max_iter=100,tol=0.0001,
                                precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
        k_means.fit(data)
        labels = k_means.labels_
        cluster_centers = k_means.cluster_centers_
    elif clustering_method == 'MeanShift':
        ms =  MeanShift( bin_seeding=True,cluster_all=False)
        ms.fit(data)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_
    elif clustering_method == 'AffinityPropagation':
        af = AffinityPropagation().fit(data)
        cluster_centers = [data[i] for i in  af.cluster_centers_indices_]
        labels = af.labels_
    elif clustering_method == "AgglomerativeClustering":
        n_neighbors=max(10,len(data)/4)
        connectivity = kneighbors_graph(data, n_neighbors=n_neighbors)
        ward = AgglomerativeClustering(n_clusters=num_clusters, connectivity=connectivity,
                               linkage='ward').fit(data)
        labels = ward.labels_
    elif clustering_method == "DBSCAN":
        db = DBSCAN().fit(data)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        extra = core_samples_mask
        labels = db.labels_

    if labels is not None:
        labels_unique = np.unique(labels)
    return labels,cluster_centers,labels_unique,extra
def clustering_unemp_var_raw(request, model,variable ):
    # Initialize all variables to None, they will be assigned if they are used
    data = dataset = title = legend = min_val = max_val = dataset = cluster_year_freq=  None
    relative_file_path = relative_file_path2 = ''
    states = years = None
    normalize_data=True
    clustering_method = 'KMeans'
    num_clusters = 2
    title = "Unemployment Vs. "+ variable
    x_axis_name = 'unemployment'
    y_axis_name = variable
    # Get all possible years
    choices,min_year,max_year = dbqueries.getAvailableYearChoices(model,variable)
    # Initialize form, if method is post this will be overwritten
    form = ClusteringOptionsForm(year_choices=choices)
    # Check wether user posted the formulary
    if request.method=='POST':
        form = ClusteringOptionsForm(request.POST, year_choices=choices)
        if form.is_valid():
            states = form.cleaned_data['states']
            years = form.cleaned_data['years']
            normalize_data = form.cleaned_data['normalize_data']
            if normalize_data:
                x_axis_name += ' (normalized)'
                y_axis_name += ' (normalized)'
                title += ' (normalized)'
            unemp_difference = form.cleaned_data['unemployment_difference']
            unemployment_difference = form.cleaned_data['unemployment_difference']
            variable_difference = form.cleaned_data['variable_difference']
            num_clusters = form.cleaned_data['number_of_clusters']
            clustering_method =form.cleaned_data['clustering_algorithm'] 
            # Get data
            data = dbqueries.get_unemp_vs_var_from_database_paired(model,variable,min_year,max_year,states,years,normalize_data,unemployment_difference,variable_difference)
            # Adapt data for clustering algorithms as a numbpy array of 2D
            prepared_data = np.array([[float(row['unemployment']),float(row['variable'])] for row in data])  
            year_labels = np.array([int(row['year']) for row in data])
            # Get clustering results
            labels,cluster_centers,labels_unique,extra = cluster_data(prepared_data,clustering_method, num_clusters)
            # Plot results using matplotlib
            colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
            
            # Count all frequency of years for each cluster
            cluster_year_freq = {}
            num_clusters = sum(labels_unique!=-1)
            for k,col in zip(range(num_clusters),colors):
                my_members = labels == k
                
            for k, col in zip(labels_unique, colors):
                my_members = labels == k
                if k == -1:
                    col2 = 'k'
                    plt.plot(prepared_data[my_members, 0], prepared_data[my_members, 1], col2 + '.',markersize=8)
                else:
                    y = np.bincount(year_labels[my_members])
                    ii = np.nonzero(y)[0]
                    cluster_year_freq[k]={'id':k}
                    cluster_year_freq[k]['color'] = col
                    cluster_year_freq[k]['years']=zip(ii,y[ii])
                    if clustering_method=="DBSCAN":
                        core_samples_mask =extra
                        xy = prepared_data[my_members & core_samples_mask]
                        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                                 markeredgecolor='k', markersize=14)
                        xy = prepared_data[my_members & ~core_samples_mask]
                        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                                     markeredgecolor='k', markersize=8)
                    else:
                        plt.plot(prepared_data[my_members, 0], prepared_data[my_members, 1], col + '.',markersize=8)
                        if cluster_centers is not None:
                            cluster_center = cluster_centers[k]  
                            plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                                     markeredgecolor='k', markersize=14)
                            if clustering_method=="AffinityPropagation":
                                for x in prepared_data[my_members]:
                                    plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

            # plt.title('Estimated number of clusters: %d' % n_clusters_)
            relative_file_path =os.path.join( PLOTS_TEMP_FOLDER,str(uuid.uuid4())+'.png')
            path = os.path.join(settings.MEDIA_ROOT,relative_file_path)
            plt.tight_layout()
            plt.savefig(path)
            plt.close()

            dist_out = pairwise_distances(prepared_data, metric="euclidean")
            dist_out = dist_out[np.argsort(labels)]
            plt.matshow(dist_out, cmap=plt.cm.autumn)
            plt.title('Similarity Matrix (euclidian dist.) reordered by cluster')
            relative_file_path2 =os.path.join( PLOTS_TEMP_FOLDER,str(uuid.uuid4())+'.png')
            path = os.path.join(settings.MEDIA_ROOT,relative_file_path2)
            plt.savefig(path)
            plt.close()

            

    return render_to_response('data_mining/clustering.html', {
        'data': data,
        'form':form,
        'title':title,
        'min_val':min_val,
        'x_axis_name':x_axis_name,
        'y_axis_name':y_axis_name,
        'max_val':max_val,
        'dataset':dataset,
        'variable':variable,
        'clustering_img':'/media/'+relative_file_path,
        'coclustering_img':'/media/'+relative_file_path2,
        'cluster_year_freq':cluster_year_freq
        
        }, context_instance=RequestContext(request))
		
		
def association_mortality(request):
	state=None
	data = None
	form = SingleUsStateSelectForm()
	title=yaxis=None
	rules = ['a','b','c']
	if request.method=='POST':
		form = SingleUsStateSelectForm(request.POST)
		if form.is_valid():
			states = form.cleaned_data['name']
			states_id = [ int(state.id) for state in states  ]
			if (len(states_id)>0):
				data = MortalityByStateYearly.objects.filter(state__id__in= states_id).values('state','year').select_related('state__name').annotate(value=Sum('crude_rate'))	
				data = data.filter(crude_rate__isnull=False ).order_by('state','year').values('state','state__name','year','value')
				title = "Crude Rate (yearly)"
	return render_to_response('data_mining/association.html', {
		'data': data,
		'form':form,
		'rules':rules,
		'state': state,
		'title': title,
		'subtitle': '',
		'yaxis':yaxis
		}, context_instance=RequestContext(request))
		
def association_natality(request):
	state=None
	data = None
	form = SingleUsStateSelectForm()
	title=yaxis=None
	rules = None
	stateName = None
	type='natality'
	if request.method=='POST':
		form = SingleUsStateSelectForm(request.POST)
		if form.is_valid():
			state = form.cleaned_data['name']
			uData = UnemploymentByStateMonthly.objects.filter(state=state).values('state','year').select_related('state_name').annotate(value=Avg('value')).order_by('year')
			data = NatalityByStateYearly.objects.filter(state= state).values('state','year').select_related('state__name').annotate(value=Sum('birth_rate'))	
			data = data.filter(birth_rate__isnull=False ).order_by('state','year').values('state','state__name','year','value')
			list = []
			stateName = UsState.objects.filter(id=data[0]['state'])[0].name
			for item in uData:
				sID = item['state']
				y = item['year']
				val = item['value']
				nvals = data.filter(year=y)
				if(len(nvals)==0):
					continue
				nVal = nvals[0]['value']
				if (nVal is None):
					continue
				list.append((sID,y,1,val,nVal))
			info = stat_association.stat_association(list)
			rules = info['rules']
			data = info['values']
			title = "Birth Rate (yearly)"
			yaxis = "Birth Rate (per 1000 people)"
	return render_to_response('data_mining/association.html', {
		'data': data,
		'rules':rules,
		'form':form,
		'stateName':stateName,
		'type':type,
		'state': state,
		'title': title,
		'subtitle': '',
		'yaxis':yaxis
		}, context_instance=RequestContext(request))
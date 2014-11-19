from django.contrib import admin
from models import UsState,UnemploymentByStateMonthly, Crisis, Race,NatalityByStateYearly
import csv
from django.http import HttpResponse

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
        
        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode('utf-8') for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv

@admin.register(UsState)
class UsStateAdmin(admin.ModelAdmin):
    list_display = ('name','code',)
    list_search= ['name',]
    actions = [export_as_csv_action("Export selected data to CSV", fields= list_display, header=True),]
@admin.register(UnemploymentByStateMonthly)
class UnemploymentByStateMonthlyAdmin(admin.ModelAdmin):
    list_display = ('state','year','month','value')
    list_filter =['state','year']
    actions = [export_as_csv_action("Export selected data to CSV", fields= list_display, header=True),]
@admin.register(Crisis)
class CrisisAdmin(admin.ModelAdmin):
    list_display = ('year',)
    list_filter =['year',]
    actions = [export_as_csv_action("Export selected data to CSV", fields= list_display, header=True),]
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [export_as_csv_action("Export selected data to CSV", fields= list_display, header=True),]

@admin.register(NatalityByStateYearly)
class NatalityByStateYearlyAdmin(admin.ModelAdmin):
    list_display = ('state','year','race','birth_rate','num_births','total_population',)
    list_filter= ['state','year','race',]
    actions = [export_as_csv_action("Export selected data to CSV", fields= list_display, header=True),]

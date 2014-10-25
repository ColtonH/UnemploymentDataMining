from django.db import models
# Create your models here.

class UsState(models.Model):
    name = models.CharField(null=False,blank=False,max_length=100)
    code = models.CharField(max_length=2)
    class Meta():
        unique_together = (('name',),)
    def __unicode__(self):
        return u'%s' %(self.name)
class UnemploymentByStateMonthly(models.Model):
    state = models.ForeignKey('UsState')
    year = models.PositiveIntegerField(null=False)
    month = models.PositiveIntegerField(null=False)
    value = models.FloatField(null=False)
    def Meta():
        unique_together=(('state','year','month'),)


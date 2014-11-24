from django.db import models
# Create your models here.

#
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

class Race(models.Model):
    name = models.CharField(null=False,blank=False,max_length=100)
    race_code = models.CharField(null=True,blank=False,max_length=30)
    class Meta():
        unique_together = (('name',),)
    def __unicode__(self):
        return u'%s' %(self.name)

class NatalityByStateYearly(models.Model):
    state = models.ForeignKey('UsState')
    year = models.PositiveIntegerField(null=False)
    race = models.ForeignKey('Race')
    num_births = models.PositiveIntegerField(null=False)
    total_population = models.PositiveIntegerField(null=True)
    birth_rate = models.FloatField(null=True)  
    fertility_rate = models.FloatField(null=True)
    
class MortalityByStateYearly(models.Model):
    state = models.ForeignKey('UsState')
    year = models.PositiveIntegerField(null=False)
    race = models.ForeignKey('Race')
    num_deaths = models.PositiveIntegerField(null=False)
    total_population = models.PositiveIntegerField(null=True)
    crude_rate = models.FloatField(null=True)  
#========================================================
class Crisis(models.Model):
    year = models.PositiveIntegerField(null=False)
    crisis = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%d:%s' %(self.year,self.crisis)
    class Meta():
        unique_together = (('year',),)

from django.db import models
from datetime import datetime
from django.utils import timezone
#from django.conf import settings

#""" def get_default():
   # return str(settings.MEDIA_ROOT) + '/BLANK.pdf' """

# Create your models here.

how_choices=[
        ('Online','Online'),
        ('Offline','Offline'),
        
    ]

class Planner(models.Model):
    plan_date= models.DateField(default=datetime.now, verbose_name='Date:',  null=True, blank=True)
    plan_time= models.TimeField(default=datetime.now, verbose_name='Time: ', null=True, blank=True)
    plan_text= models.TextField(verbose_name='Details of Programme: ', null=True, blank=True)
    plan_venue= models.CharField(max_length=100, verbose_name='Venue: ', null=True, blank=True)
    plan_file = models.FileField(upload_to='planner', null=True, blank=True, verbose_name='Related Correspondance (.pdf):')
    plan_how = models.CharField(max_length=60, verbose_name='How to Join: ', null=True, blank=True, choices=how_choices)
    plan_remarks= models.CharField(max_length=200,verbose_name='Remarks: ', null=True, blank=True)
    plan_updated = models.DateTimeField(auto_now=True)
    plan_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['plan_date','plan_time' ]
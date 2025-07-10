from django.db import models




#for validation 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_mobile(value):
    if len(str(value).strip()) != 10:
        raise ValidationError(
            _("%(value)s shoud be of 10 digits"),
            params={"value": value},
        )
# Create your models here.

class Visitor(models.Model):
    vis_date= models.DateField(null=True, blank=True, verbose_name='Date:')
    vis_time= models.TimeField(null=True, blank=True ,verbose_name='Time:')
    vis_name= models.CharField(max_length=200, null=True, blank=True, verbose_name="Visitor's Name:")
    vis_address= models.TextField(null=True, blank=True, verbose_name='Address:')
    vis_mobile= models.PositiveBigIntegerField(null=True, blank=True, validators=[validate_mobile],verbose_name='Mobile:')
    vis_email= models.EmailField(null=True, blank=True, verbose_name='Email:')
    vis_reason= models.TextField(null=True, blank=True, verbose_name='Purpose of Visit:')
    
    vis_photo=models.ImageField(upload_to='visitor', null=True, blank=True, verbose_name='Photograph of Visitor:', default="../static/images/No_Image.jpg")
    vis_remarks=models.TextField(null=True, blank=True, verbose_name='Remarks:')
    vis_met=models.BooleanField(default=False, verbose_name='  Met with DHR (Yes/No):')
    vis_face_encoding = models.BinaryField(blank=True, null=True) 
    vis_updated = models.DateTimeField(auto_now=True)
    vis_created = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return f'{self.vis_name}'
    


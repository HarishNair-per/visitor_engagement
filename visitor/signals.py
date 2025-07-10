# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Visitor
# from .utils import train_lbph_model

# @receiver(post_save, sender=Visitor)
# def retrain_model_after_save(sender, instance, **kwargs):
#     if instance.vis_photo:
#         train_lbph_model()
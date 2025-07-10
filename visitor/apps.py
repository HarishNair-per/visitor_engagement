from django.apps import AppConfig
# from .cache import load_face_encodings

class VisitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visitor'

    # def ready(self):
    #     load_face_encodings()


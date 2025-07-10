import os
import face_recognition
import numpy as np
from PIL import Image
from .models import Visitor

from django.conf import settings

def encode_faces():
    encodings = []
    visitors = []

    for visitor in Visitor.objects.exclude(vis_photo=''):
        try:
            image_path = visitor.vis_photo.path
            if not os.path.exists(image_path):
                continue

            image = face_recognition.load_image_file(image_path)
            face_enc = face_recognition.face_encodings(image)
            if face_enc:
                encodings.append(face_enc[0])
                visitors.append(visitor)
        except Exception as e:
            print(f"Error encoding face for {visitor.id}: {e}")
    return encodings, visitors

def find_matching_visitor_from_blob(blob_data, threshold=0.5):
    known_encodings, known_visitors = encode_faces()
    unknown_img = face_recognition.load_image_file(blob_data)
    unknown_encodings = face_recognition.face_encodings(unknown_img)

    if unknown_encodings:
        unknown_encoding = unknown_encodings[0]
        distances = face_recognition.face_distance(known_encodings, unknown_encoding)

        if len(distances) > 0:
            best_match_index = np.argmin(distances)
            if distances[best_match_index] < threshold:
                return known_visitors[best_match_index]
    return None


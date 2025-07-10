import os
import numpy as np
from django.core.management.base import BaseCommand
from visitor.models import Visitor
import face_recognition


class Command(BaseCommand):
    help = "Populates vis_face_encoding for visitors without encodings"

    def handle(self, *args, **kwargs):
        updated_count = 0
        skipped = 0

        visitors = Visitor.objects.filter(vis_face_encoding__isnull=True)
        self.stdout.write(f"Found {visitors.count()} visitor(s) without encoding.")

        for visitor in visitors:
            try:
                image_path = visitor.vis_photo.path
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    visitor.vis_face_encoding = encodings[0].tobytes()
                    visitor.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"✓ Updated: {visitor.vis_name}"))
                else:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(f"⚠ No face found for {visitor.vis_name}"))
            except Exception as e:
                skipped += 1
                self.stdout.write(self.style.ERROR(f"✗ Error processing {visitor.vis_name}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"\nCompleted. {updated_count} updated, {skipped} skipped."))
import numpy as np
# from visitor.models import Visitor

encoding_cache = []

def load_face_encodings():
    from visitor.models import Visitor  # Delayed import
    global encoding_cache
    encoding_cache = []
    visitors = Visitor.objects.exclude(vis_face_encoding__isnull=True)
    for v in visitors:
        try:
            enc = np.frombuffer(v.vis_face_encoding, dtype=np.float64)
            encoding_cache.append((v, enc))
        except Exception as e:
            print(f"Failed to load encoding for {v.id}: {e}")

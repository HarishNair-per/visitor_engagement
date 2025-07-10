import base64
import cv2
import numpy as np
import face_recognition
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VisitorForm
from .models import Visitor
#from visitor.cache import encoding_cache
from django.core.files.base import ContentFile

@login_required
def visitor_table(request):
    visitors= Visitor.objects.all() #filter(vis_date=datetime.now().date(), vis_met=False)
    context ={'visitors': visitors,'today': datetime.now().date()}
    return render(request,'visitor/visitors_table.html', context)



@csrf_exempt
@login_required
def visitor_form_view(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        captured_image = request.POST.get('captured_image')

        if form.is_valid() and captured_image:
            format, imgstr = captured_image.split(';base64,')
            img_bytes = base64.b64decode(imgstr)
            img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)

            if not encodings:
                return JsonResponse({'status': 'error', 'message': 'No face detected in form submission.'})

            visitor = form.save(commit=False)
            visitor.vis_date = datetime.now().date()
            visitor.vis_time = datetime.now().time()
            visitor.vis_photo.save(f"visitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg", ContentFile(img_bytes))
            visitor.vis_face_encoding = encodings[0].tobytes()
            visitor.save()

            from visitor.cache import load_face_encodings
            load_face_encodings()

            return redirect('visitor:visitor_table')
    else:
        form = VisitorForm()

    return render(request, 'visitor/visitor_register.html', {'form': form})

# @login_required
# def visitor_form_view(request):
#     if request.method == 'POST':
#         form = VisitorForm(request.POST)
#         if form.is_valid():
#             visitor = form.save(commit=False)
#             visitor.vis_date = datetime.now().date()
#             visitor.vis_time = datetime.now().time()

#             image_data = request.POST.get('captured_image')
#             if image_data:
#                 format, imgstr = image_data.split(';base64,')
#                 img_bytes = base64.b64decode(imgstr)
#                 file_name = f"visitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
#                 image_file = ContentFile(img_bytes, name=file_name)
#                 visitor.vis_photo = image_file
            
#             visitor.save()
#             return redirect('visitor:visitor_table')
#     else:
#         form = VisitorForm()
#     return render(request, 'visitor/visitor_register.html', {'form': form})

@csrf_exempt
@login_required
def visitor_register(request):
    if request.method != 'POST':
        return redirect('visitor:visitor_form')

    image_data = request.POST.get('captured_image')
    if image_data:
        format, imgstr = image_data.split(';base64,')
        img_bytes = base64.b64decode(imgstr)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        small_img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb_small_img)
        if not encodings:
            return JsonResponse({'status': 'error', 'message': 'No face detected.'})

        new_encoding = encodings[0]
        matched = None

        all_visitors = Visitor.objects.all()

        for visitor in all_visitors:
            try:
                if visitor.vis_face_encoding:
                    stored_encoding = np.frombuffer(visitor.vis_face_encoding, dtype=np.float64)
                else:
                    existing_img = face_recognition.load_image_file(visitor.vis_photo.path)
                    encs = face_recognition.face_encodings(existing_img)
                    if not encs:
                        continue
                    stored_encoding = encs[0]
                    visitor.vis_face_encoding = stored_encoding.tobytes()
                    visitor.save()

                is_match = face_recognition.compare_faces([stored_encoding], new_encoding, tolerance=0.55)[0]
                if is_match:
                    matched = visitor
                    break
            except Exception as e:
                print(f"Encoding error for visitor {visitor.id}: {e}")

        if matched:
            return JsonResponse({
                'status': 'matched',
                'message': 'Visitor matched.',
                'visitor': {
                    'vis_name': matched.vis_name,
                    'vis_address': matched.vis_address,
                    'vis_mobile': matched.vis_mobile,
                    'vis_email': matched.vis_email
                },
                'captured_image': image_data
            })
        else:
            return JsonResponse({
                'status': 'new',
                'message': 'New visitor. Please fill the form.'
            })

    return JsonResponse({'status': 'error', 'message': 'No image captured.'})
 
 



""" def visitor_register(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': f'Invalid request method: {request.method}'})

    image_data = request.POST.get('captured_image')
    if not image_data:
        return JsonResponse({'status': 'error', 'message': 'No image captured.'})

    format, imgstr = image_data.split(';base64,')
    img_bytes = base64.b64decode(imgstr)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    small_img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb_small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)

    encodings = face_recognition.face_encodings(rgb_small_img)
    if not encodings:
        return JsonResponse({'status': 'error', 'message': 'No face detected.'})

    new_encoding = encodings[0]
    matched = None

    for v, stored_encoding in encoding_cache:
        try:
            is_match = face_recognition.compare_faces([stored_encoding], new_encoding, tolerance=0.55)[0]
            if is_match:
                matched = v
                break
        except Exception as e:
            print(f"Matching error: {e}")

    if matched:
        file_name = f"visitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        matched.vis_photo.save(file_name, ContentFile(img_bytes))
        matched.vis_time = datetime.now().time()
        matched.vis_date = datetime.now().date()
        matched.vis_face_encoding = new_encoding.tobytes()
        matched.pk = None  # create new record
        matched.save()
        return JsonResponse({
            'status': 'matched',
            'message': 'Visitor matched and new entry created.',
            'visitor': {
                'vis_name': matched.vis_name,
                'vis_address': matched.vis_address,
                'vis_mobile': matched.vis_mobile,
                'vis_email': matched.vis_email
            },
            'captured_image': image_data
        })
    else:
        return JsonResponse({
            'status': 'new',
            'message': 'New visitor. Please fill the form.'
        })
 """




# def visitor_register(request):
#     if request.method == 'POST':
#         print("POST:", request.POST)
#         print("FILES:", request.FILES)
#         form = VisitorForm(request.POST, request.FILES)
#         if form.is_valid():
#             visitor = form.save(commit=False)
#             visitor.vis_date = datetime.now().date()
#             visitor.vis_time = datetime.now().time()
#             # If vis_photo is missing from form.cleaned_data due to excluded form fields
#             """ if 'No_Image.jpg' not in visitor.vis_photo and 'vis_photo' in request.FILES:
#                 visitor.vis_photo = request.FILES['vis_photo'] """
#             visitor.save()
#             return redirect('visitor:visitor_table')
#         else:
#             print("Form errors:", form.errors)
#     else:
#         form = VisitorForm()
#     return render(request, 'visitor/visitor_register.html', {'form': form}) 

@login_required    
@csrf_exempt
def visitor_update(request,pk):
    visitor = get_object_or_404(Visitor,id=pk)
    form = VisitorForm(request.POST or None, request.FILES or None, instance=visitor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('visitor:visitor_table')
    context = {
        'form': form,
        }
    return render(request, 'visitor/visitor_update.html', context)


""" def visitor_register(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST, request.FILES)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.vis_date = datetime.now().date()
            visitor.vis_time = datetime.now().time()
            visitor.save()
            print("FILES:", request.FILES)
            
            return redirect('visitor:success')
    else:
        form = VisitorForm()
    return render(request, 'visitor/visitor_register.html', {'form': form})
 """
def success(request):
    return render(request, 'visitor/success.html')

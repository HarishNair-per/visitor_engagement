from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Planner
from .forms import PlannerForm



# Create your views here.


def home(request):
    
    return render(request,'planner/home.html')


@login_required
def planner_table(request):
    plans= Planner.objects.filter(plan_date__gte=datetime.now().date())
    context ={'plans': plans,'today': datetime.now().date()}
    return render(request,'planner/planner_table.html', context)

@login_required
@csrf_exempt
def planner_entry(request):
    if request.method == 'POST':
       
        form = PlannerForm(request.POST, request.FILES)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.save()
            return redirect('planner:planner_table')
        else:
            print("Form errors:", form.errors)
    else:
        form = PlannerForm()
    return render(request, 'planner/planner_entry.html', {'form': form})
    

@login_required
@csrf_exempt
def planner_update(request,pk):
    visitor = get_object_or_404(Planner,id=pk)
    form = PlannerForm(request.POST or None, request.FILES or None, instance=visitor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('planner:planner_table')
    context = {
        'form': form,
        }
    return render(request, 'planner/planner_update.html', context)

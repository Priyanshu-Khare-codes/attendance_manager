from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AttendanceForm
import json

# Create your views here.

def index(request):
    return render(request, 'index.html')

def calculate_attendance(total_classes, attended_classes, holiday_classes, daily_classes, classes_per_day):
    attendance_analysis = []
    running_total = total_classes
    running_attended = attended_classes
    current_percentage = (attended_classes/total_classes) * 100

    for day in range(1, holiday_classes + 1):
        day_classes = daily_classes.get(f"day{day}", 7)
        running_total += classes_per_day
        running_attended += (classes_per_day - day_classes)
        new_percentage = (running_attended/running_total) * 100
        decrement = current_percentage - new_percentage
        
        attendance_analysis.append({
            'day': day,
            'decreased_percentage': round(new_percentage, 2),
            'decrement_per_day': round(decrement, 2)
        })
        current_percentage = new_percentage

    return attendance_analysis

def attendance_calculater(request):  # Changed spelling to match urls.py
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            daily_classes_json = data['daily_classes']

            try:
                if daily_classes_json:
                    daily_classes = json.loads(daily_classes_json)
                else:
                    daily_classes = {f"day{i+1}": data['classes_per_day'] 
                                   for i in range(data['holiday_classes'])}

                request.session.update({
                    'daily_classes': daily_classes,
                    'total_classes': data['total_classes'],
                    'attended_classes': data['attended_classes'],
                    'holiday_classes': data['holiday_classes'],
                    'classes_per_day': data['classes_per_day'],
                    'result': f"Your Current Attendance: {(data['attended_classes']/data['total_classes']) * 100:.2f}%"
                })
                return redirect('attendance_result')
                
            except json.JSONDecodeError:
                messages.error(request, "Invalid daily classes configuration")
                return redirect('attendance_calculater')
    else:
        form = AttendanceForm()
    
    return render(request, 'index.html', {'form': form})

def attendance_result(request):
    session_data = {
        'result': request.session.get('result'),
        'total_classes': request.session.get('total_classes'),
        'attended_classes': request.session.get('attended_classes'),
        'holiday_classes': request.session.get('holiday_classes'),
        'classes_per_day': request.session.get('classes_per_day', 7),
        'daily_classes': request.session.get('daily_classes', {})
    }

    if all(session_data.values()):
        attendance_analysis = calculate_attendance(
            session_data['total_classes'],
            session_data['attended_classes'],
            session_data['holiday_classes'],
            session_data['daily_classes'],
            session_data['classes_per_day'],
        )
        
        for key in session_data:
            request.session.pop(key, None)
    else:
        attendance_analysis = []

    return render(request, 'result.html', {
        **session_data,
        'attendance_analysis': attendance_analysis
    })

def about(request):
    return render(request, 'about.html')

def developers(request):
    return render(request, 'developers.html')
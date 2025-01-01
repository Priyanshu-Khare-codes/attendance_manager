from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AttendanceForm
import json

# Create your views here.

def index(request):
    return render(request, 'index.html')

# def attendance_calculater(request):
#     result = None
#     if request.method == 'POST':
#         form = AttendanceForm(request.POST)
#         if form.is_valid():
#             total_classes = form.cleaned_data['total_classes']
#             attended_classes = form.cleaned_data['attended_classes']
#             holiday_classes = form.cleaned_data['holiday_classes']

#             if attended_classes > total_classes:
#                 result = "No. of classes cannot be more than Total no. of classes."
#                 return redirect('attendance_calculater')

#             else:
#                 percentage = (attended_classes/total_classes) * 100
#                 result = f"Your Current Attendace : {percentage:.2f}%"

#             # Storing data in the session
#             request.session['result'] = result
#             request.session['total_classes'] = total_classes
#             request.session['attended_classes'] = attended_classes
#             request.session['holiday_classes'] = holiday_classes

#             return redirect('attendance_result')
#     else:
#         form = AttendanceForm()
    
#     return render(request, 'index.html', {'form':form})

# def attendance_result(request):
#     result = request.session.get('result')
#     total_classes = request.session.get('total_classes')
#     attended_classes = request.session.get('attended_classes')
#     holiday_classes = request.session.get('holiday_classes')

#     if total_classes and attended_classes and holiday_classes is not None:
#         attendance_analysis = []
#         for i in range(holiday_classes):
#             new_total_classes = total_classes + ((i+1)*7)
#             decreased_percentage = (attended_classes/new_total_classes)*100
#             decrement_per_day = (attended_classes/(total_classes + (i*7)))*100 - decreased_percentage

#             attendance_analysis.append({
#                 'day' : i+1,
#                 'decreased_percentage' : round(decreased_percentage, 2),
#                 'decrement_per_day' : round(decrement_per_day, 2)
#             })
    
#     else:
#         attendance_analysis = []

#     # Pass the data to the template
#     return render(request, 'result.html', {
#         'result': result,
#         'total_classes': total_classes,
#         'attended_classes': attended_classes,
#         'holiday_classes': holiday_classes,
#         'attendance_analysis': attendance_analysis
#     })

# def attendance_calculater(request):
#     if request.method == 'POST':
#         form = AttendanceForm(request.POST)
#         if form.is_valid():
#             total_classes = form.cleaned_data['total_classes']
#             attended_classes = form.cleaned_data['attended_classes']
#             holiday_classes = form.cleaned_data['holiday_classes']
#             classes_per_day = form.cleaned_data['classes_per_day']
#             daily_classes_json = form.cleaned_data['daily_classes']

#             if attended_classes > total_classes:
#                 result = "No. of classes cannot be more than Total no. of classes."
#                 return redirect('attendance_calculater')

#             # Process daily classes if configured manually
#             if daily_classes_json:
#                 daily_classes = json.loads(daily_classes_json)
#                 request.session['daily_classes'] = daily_classes
#                 request.session['using_manual_config'] = True
#             else:
#                 request.session['using_manual_config'] = False

#             percentage = (attended_classes/total_classes) * 100
#             result = f"Your Current Attendace : {percentage:.2f}%"

#             request.session['result'] = result
#             request.session['total_classes'] = total_classes
#             request.session['attended_classes'] = attended_classes
#             request.session['holiday_classes'] = holiday_classes
#             request.session['classes_per_day'] = classes_per_day

#             return redirect('attendance_result')
#     else:
#         form = AttendanceForm()
    
#     return render(request, 'index.html', {'form':form})

# def attendance_result(request):
#     result = request.session.get('result')
#     total_classes = request.session.get('total_classes')
#     attended_classes = request.session.get('attended_classes')
#     holiday_classes = request.session.get('holiday_classes')
#     classes_per_day = request.session.get('classes_per_day', 7)
#     using_manual_config = request.session.get('using_manual_config', False)
#     daily_classes = request.session.get('daily_classes', {})

#     if all(x is not None for x in [total_classes, attended_classes, holiday_classes]):
#         attendance_analysis = []
#         running_total = total_classes
        
#         for i in range(holiday_classes):
#             if using_manual_config and f"day{i+1}" in daily_classes:
#                 day_classes = daily_classes[f"day{i+1}"]
#             else:
#                 day_classes = classes_per_day

#             new_total_classes = running_total + day_classes
#             decreased_percentage = (attended_classes/new_total_classes)*100
#             prev_percentage = (attended_classes/running_total)*100
#             decrement_per_day = prev_percentage - decreased_percentage

#             attendance_analysis.append({
#                 'day': i+1,
#                 'decreased_percentage': round(decreased_percentage, 2),
#                 'decrement_per_day': round(decrement_per_day, 2)
#             })
#             running_total = new_total_classes
    
#     else:
#         attendance_analysis = []

#     return render(request, 'result.html', {
#         'result': result,
#         'total_classes': total_classes,
#         'attended_classes': attended_classes,
#         'holiday_classes': holiday_classes,
#         'attendance_analysis': attendance_analysis
#     })


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
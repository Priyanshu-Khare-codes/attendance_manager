from django import forms

# class AttendanceForm(forms.Form):
#     total_classes = forms.IntegerField(label="Total No. of Classes", min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control p-2'}))
#     attended_classes = forms.IntegerField(label="Present Classes", min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control p-2'}))
#     holiday_classes = forms.IntegerField(label="No. of Holidays", min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control p-2'}))

class AttendanceForm(forms.Form):
    total_classes = forms.IntegerField(
        label="Total No. of Classes", 
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control p-2'})
    )
    attended_classes = forms.IntegerField(
        label="Present Classes", 
        min_value=0, 
        widget=forms.NumberInput(attrs={'class': 'form-control p-2'})
    )
    holiday_classes = forms.IntegerField(
        label="No. of Holidays", 
        min_value=0, 
        widget=forms.NumberInput(attrs={'class': 'form-control p-2', 'id': 'holidayInput'})
    )
    classes_per_day = forms.IntegerField(
        label="Classes Per Day",
        initial=7,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control p-2', 'id': 'classesPerDay'})
    )
    daily_classes = forms.CharField(
        required=False, 
        widget=forms.HiddenInput(attrs={'id': 'dailyClassesData'})
    )

    def clean(self):
        cleaned_data = super().clean()
        attended_classes = cleaned_data.get('attended_classes')
        total_classes = cleaned_data.get('total_classes')
        
        if attended_classes and total_classes:
            if attended_classes > total_classes:
                raise forms.ValidationError("Attended classes cannot exceed total classes")
        
        return cleaned_data

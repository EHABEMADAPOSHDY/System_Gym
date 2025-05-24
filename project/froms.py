from django import forms
from .models import Training_name, Subscriber

class Training_nameForm(forms.ModelForm):
    class Meta:
        model = Training_name
        fields = '__all__'
        # يمكنك إضافة widgets إذا رغبت

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = [
            'name',
            'mobil1',
            'mobil2',
            'Length_umber',
            'National_ID',
            'the_address',
            'Type_of_training',
            'Number_of_sessions',
            'Start_date',
            'Daytime_date',
            'the_rest'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'ادخل الاسم بالكامل'
            }),
            'mobil1': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'ادخل رقم الموبايل الأساسي'
            }),
            'mobil2': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'ادخل رقم الموبايل الاحتياطي'
            }),
            'Length_umber': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'ادخل رقم الطوارئ'
            }),
            'National_ID': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'ادخل رقم الهوية الوطنية'
            }),
            'the_address': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'ادخل العنوان بالتفصيل'
            }),
            'Type_of_training': forms.Select(attrs={
                'class': 'form-control mb-3'
            }),
            'Number_of_sessions': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'عدد الجلسات'
            }),
            'Start_date': forms.DateInput(attrs={
                'class': 'form-control mb-3',
                'type': 'date'
            }),
            'Daytime_date': forms.DateInput(attrs={
                'class': 'form-control mb-3',
                'type': 'date'
            }),
           'the_rest': forms.DateInput(attrs={
                'class': 'form-control mb-3',
                'type': 'الباقي'
            }),
        }

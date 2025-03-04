# forms.py
from django import forms
from django.contrib.auth.models import User

from .models import Patients, Doctor, Appointment, Admin, OperationSchedule


class PatientForm(forms.ModelForm):
    p_password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = Patients
        fields = [
            'p_name', 'p_age', 'p_gender', 'p_contact_no', 'p_address',
            'p_blood_group', 'p_photo', 'p_hms', 'p_user_id', 'p_password'
        ]
        labels = {
            'p_name': 'Name',
            'p_age': 'Age',
            'p_gender': 'Gender',
            'p_contact_no': 'Contact No',
            'p_address': 'Address',
            'p_blood_group': 'Blood Group',
            'p_photo': 'Photo',
            'p_hms': 'HMS',
            'p_user_id': 'User ID',
            'p_password': 'Password',
        }
        widgets = {
            'p_name': forms.TextInput(attrs={'class': 'form-control'}),
            'p_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'p_gender': forms.Select(
                choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                attrs={'class': 'form-control'}
            ),
            'p_contact_no': forms.TextInput(attrs={'class': 'form-control'}),
            'p_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'p_blood_group': forms.TextInput(attrs={'class': 'form-control'}),
            'p_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'p_hms': forms.TextInput(attrs={'class': 'form-control'}),
            'p_user_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DoctorForm(forms.ModelForm):
    d_gender = forms.ChoiceField(
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('N', 'Prefer not to say')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Gender"
    )

    class Meta:
        model = Doctor
        fields = [
            'd_name', 'd_specialty', 'd_contact_no', 'd_photo', 'd_age',
                    'd_hms', 'd_user_id', 'd_password', 'd_gender'
        ]
        widgets = {
            'd_name': forms.TextInput(attrs={'class': 'form-control'}),
            'd_specialty': forms.TextInput(attrs={'class': 'form-control'}),
            'd_contact_no': forms.TextInput(attrs={'class': 'form-control'}),
            'd_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'd_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'd_hms': forms.TextInput(attrs={'class': 'form-control'}),
            'd_user_id': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AppointmentForm(forms.ModelForm):
    a_patient = forms.ModelChoiceField(
        queryset=Patients.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['a_patient', 'a_doctor', 'a_appointment_date', 'a_status', 'a_hms']
        widgets = {
            'a_doctor': forms.Select(attrs={'class': 'form-control'}),
            'a_appointment_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'a_status': forms.Select(
                choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
                attrs={'class': 'form-control'}
            ),
            'a_hms': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AdminForm(forms.ModelForm):
    a_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")

    class Meta:
        model = Admin
        fields = ['a_username', 'a_password', 'a_roles', 'a_hms', 'a_photo']
        widgets = {
            'a_username': forms.TextInput(attrs={'class': 'form-control'}),
            'a_roles': forms.TextInput(attrs={'class': 'form-control'}),
            'a_hms': forms.TextInput(attrs={'class': 'form-control'}),
            'a_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class OperationScheduleForm(forms.ModelForm):
    class Meta:
        model = OperationSchedule
        fields = ['patient', 'doctor', 'theater', 'operation_type', 'scheduled_date', 'status']
        widgets = {
                        'scheduled_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'})
        }

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patients  # Ensure the correct model name
        fields = [  'p_user_id','p_password']
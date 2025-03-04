from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils import timezone

class Patients(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=250)
    p_age = models.IntegerField()
    p_gender = models.CharField(max_length=10)
    p_contact_no = models.CharField(max_length=10)
    p_address = models.TextField()
    p_blood_group = models.CharField(max_length=5)
    p_photo = models.ImageField(upload_to='patients_photos/', blank=True, null=True)
    p_hms = models.CharField(max_length=100)
    p_user_id = models.CharField(max_length=12, unique=True)
    p_password = models.CharField(max_length=255)

    def __str__(self):
        return self.p_name

class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    d_id = models.AutoField(primary_key=True)
    d_name = models.CharField(max_length=255)
    d_specialty = models.CharField(max_length=255)
    d_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    d_contact_no = models.CharField(max_length=10)
    d_photo = models.ImageField(upload_to='doctors_photos/', blank=True, null=True)
    d_age = models.IntegerField()
    d_hms = models.CharField(max_length=100)
    d_user_id = models.CharField(max_length=12, unique=True)
    d_password = models.CharField(max_length=255)

    def __str__(self):
        return f"Doctor: {self.d_name} ({self.d_specialty}) {self.get_d_gender_display()}"

class Appointment(models.Model):
    a_appointment_id = models.AutoField(primary_key=True)
    a_patient = models.ForeignKey(Patients, on_delete=models.CASCADE)  # ✅ Correct
    a_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    a_appointment_date = models.DateTimeField()
    a_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    a_hms = models.CharField(max_length=100)

    def __str__(self):
        return f"Appointment: {self.a_patient} with {self.a_doctor} on {self.a_appointment_date.strftime('%Y-%m-%d')} at {self.a_appointment_date.strftime('%H:%M')}"

class OperationTheater(models.Model):
    name = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class OperationSchedule(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    theater = models.IntegerField()
    operation_type = models.CharField(max_length=255)
    scheduled_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Scheduled'
    )

    def __str__(self):
        return f"{self.operation_type} for {self.patient.p_name} on {self.scheduled_date} at {self.scheduled_time}"

class Admin(models.Model):
    a_admin_id = models.AutoField(primary_key=True)
    a_username = models.CharField(max_length=255, unique=True)
    a_password = models.CharField(max_length=255)
    a_roles = models.CharField(max_length=255)
    a_hms = models.CharField(max_length=100)
    a_photo = models.ImageField(upload_to='admin_photos/', blank=True, null=True)

    def __str__(self):
        return self.a_username

    def set_password(self, raw_password):
        """Hashes the password before saving."""
        self.a_password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Checks if the provided password matches the stored hash."""
        return check_password(raw_password, self.a_password)

    def __str__(self):
        return self.a_username


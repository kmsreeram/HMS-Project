from django.contrib import admin
from .models import Patients, Doctor, Appointment, Admin

admin.site.register(Patients)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Admin)

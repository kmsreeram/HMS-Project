from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import patient_record, add_doctor, admin_login, patient_login, login_ind, all_appointments, doctor_shedule, \
    patient_appointments_view

urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    # path('signin/', views.signin, name='signin'),
    path('',views.index, name='index'),
    path('user_dashboard/',views.user_dashboard,name ='user_dashboard'),
    path('patient_dashboard/',views.patient_dashboard, name ='patient_dashboard'),
    path('user_dashboard/add_patient/', views.add_patient, name='add_patient'),
    path('user_dashboard/patient_record/', views.patient_record, name='patient_record'),
    path('user_dashboard/doctors_list/add_doctor/',   add_doctor, name='add-doctor'),
    path('user_dashboard/doctors_list/', views.doctors_list, name='doctors_list'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor_dashboard/user_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('edit_doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('user_dashboard/add_doctor/',   add_doctor, name='add-doctor'),
    path('patient_login/',  patient_login, name='patient_login'),
    path('Login_ind/', login_ind, name='Login_ind'),
    path('user_dashboard/add_appointment_d/', views.add_appointment_d, name='add_appointment_d'),
path('doctor_dashboard/doctor_appointment_view/', views.patient_appointments_view, name='doctor_appointment_view'),
    path("admin-login/", admin_login, name="admin_login"),  # URL pattern
    path('doctor_dashboard/user_dashboard/appointments/', all_appointments, name='all_appointments'),
    path('doctor_dashboard/user_dashboard/operation_list', views.operation_list, name='operation_list'),
    path('user_dashboard/shedule_operation', views.shedule_operation, name='shedule_operation'),
    path('doctor_dashboard/doctor_schedule/', views.doctor_shedule, name='doctor_schedule'),
    path('patient_dashboard/patient_appointments/', patient_appointments_view, name='patient_appointments'),
    path('user_dashboard/operation_list', views.operation_list, name='operation_list'),
    path('user_dashboard/appointments/', all_appointments, name='all_appointments'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
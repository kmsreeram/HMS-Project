from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from pyexpat.errors import messages

from .forms import PatientForm, DoctorForm, AppointmentForm, OperationScheduleForm
from .models import Patients, Doctor, Appointment, Admin, OperationSchedule


# def signup(request):
#     if request.method=='POST':
#         username = request.POST['username']
#         fname = request.POST['username']
#         lname = request.POST['fname']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#
#         myuser=User.objects.create_user(username=username,password=password1,email=email)
#         myuser.first_name=fname
#         myuser.last_name=lname
#         myuser.save()
#         return redirect('signin')
#     return render(request,'signup.html')
#
# def signin(request):
#     if request.method =='POST':
#         username=request.POST['username']
#         password1=request.POST['password1']
#         user=authenticate(username=username,password=password1)
#         if user is not None:
#             login(request, user)
#             fname=user.first_name
#             lname=user.last_name
#             return render(request,'user_dashboard.html',{'fname':fname,'lname':lname})
#         else:
#             messages.error(request," login again")
#             return redirect('signin')
def index(request):
    return render(request,'index.html')
#     return render(request,'signin.html')


def user_dashboard(request):
    # Ensure the admin is logged in
    admin_user = None
    if "admin_id" in request.session:
        try:
            admin_user = Admin.objects.get(a_admin_id=request.session["admin_id"])
        except Admin.DoesNotExist:
            return redirect("admin_login")

    return render(request, "user_Dashboard.html", {"admin": admin_user})
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save()
            return redirect('user_dashboard')

    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})


# def patient_record(request):
 # Fetch all patient records
#     return render(request, 'patient_record.html', {'patient': patient})
#
# def patient_record(request):
#     patients = Patient.objects.all()  # Fetch all patient records
#     if request.method == 'POST':
#         form = PatientForm(request.POST, request.FILES)  # Handle form submission
#         if form.is_valid():
#             form.save()  # Save the new patient
#             return redirect('patient_record')  # Refresh the page to show the updated list
#     else:
#         form = PatientForm()  # Empty form for GET request
#     return render(request, 'patient_record.html', {'patients': patients, 'form': form})
def patient_record(request):
    patients = Patients.objects.all()
    return render(request, 'patient_record.html', {'patients': patients})

def patient_dashboard(request):

    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('patient_login')

    patient = Patients.objects.get(p_id=patient_id)

    return render(request, 'patient_dashboard.html', {'patient': patient})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DoctorForm


def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, "Doctor has been added successfully!")
            return redirect('user_dashboard')
    else:
        form = DoctorForm()

    return render(request, 'add_doctor.html', {'form': form})


def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors_list.html', {'doctors': doctors})
def doctor_login(request):
    if request.method == "POST":
        hms_id = request.POST.get('hms_id')
        hms_password = request.POST.get('hms_password')

        try:
            doctor = Doctor.objects.get(d_user_id=hms_id)
            if doctor.d_password == hms_password:
                request.session['doctor_id'] = doctor.d_user_id
                return redirect('doctor_dashboard')
            else:
                return render(request, 'doctor_login.html', {'error': 'Invalid password'})
        except Doctor.DoesNotExist:
            return render(request, 'doctor_login.html', {'error': 'User not found'})

    return render(request, 'doctor_login.html')
def doctor_dashboard(request):
    if 'doctor_id' in request.session:
        try:
            doctor = Doctor.objects.get(d_user_id=request.session['doctor_id'])
            appointments = Appointment.objects.filter(a_doctor=doctor)

            return render(request, 'doctor_dashboard.html', {
                'doctor': doctor,
                'appointments': appointments
            })
        except Doctor.DoesNotExist:
            return redirect('doctor_login')

    return redirect('doctor_login')


def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, d_id=doctor_id)

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctors_list')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'edit_doctor.html', {'form': form})

def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, d_id=doctor_id)
    doctor.delete()
    messages.success(request, "Doctor deleted successfully!")
    return redirect('doctors_list')


def add_appointment_d(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor_id = request.POST.get('a_doctor')

            try:
                doctor = Doctor.objects.get(d_id=int(doctor_id))

                appointment = form.save(commit=False)
                appointment.a_doctor_id = doctor.d_id
                appointment.save()

                messages.success(request, "Appointment successfully added!")
                return redirect('user_dashboard')
            except Doctor.DoesNotExist:
                messages.error(request, "Doctor ID not found. Please check again.")

    else:
        form = AppointmentForm()

    doctors = Doctor.objects.all()
    return render(request, 'add_appointment_d.html', {'form': form, 'doctors': doctors})

def patient_appointments_view(request):
    if 'patient_id' in request.session:  # Check if patient is logged in (via session)
        try:
            patient = Patients.objects.get(id=request.session['patient_id'])
            appointments = Appointment.objects.filter(a_patient__p_user_id=request.user.username)

            return render(request, 'home/patient_appointments.html', {
                'patient': patient,
                'appointments': appointments
            })
        except Patients.DoesNotExist:
            return redirect('patient_login')  # Redirect if patient does not exist

    return redirect('patient_login')


def admin_login(request):
    error_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            admin_user = Admin.objects.get(a_username=username)

            if admin_user.a_password == password:
                request.session["admin_id"] = admin_user.a_admin_id
                return redirect("user_dashboard")

            else:
                error_message = "Invalid password"

        except Admin.DoesNotExist:
            error_message = "Admin not found"

    return render(request, "admin_login.html", {"error_message": error_message})

def patient_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            patient = Patients.objects.get(p_user_id=username, p_password=password)
            request.session['patient_id'] = patient.p_id
            return redirect('patient_dashboard')
        except Patients.DoesNotExist:
            error_message = "Invalid username or password"
            return render(request, 'patient_login.html', {'error': error_message})

    return render(request, 'patient_login.html')

def login_ind(request):
    return render(request, 'Login_ind.html')


def all_appointments(request):  # Changed function name
    appointments = Appointment.objects.all()
    return render(request, 'Appointment.html', {'appointments': appointments})


def shedule_operation(request):
    if request.method == "POST":
        form = OperationScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = OperationScheduleForm()
    return render(request, 'shedule_operation.html', {'form': form})

def operation_list(request):
    operations = OperationSchedule.objects.all().order_by('-scheduled_date',)
    return render(request, 'operation_list.html', {'operations': operations})

def doctor_shedule(request):
    if 'doctor_id' in request.session:  # Check if doctor is logged in
        try:
            doctor = Doctor.objects.get(d_user_id=request.session['doctor_id'])  # Get doctor using unique ID
            schedules = OperationSchedule.objects.filter(doctor=doctor).order_by('-scheduled_date')

            return render(request, 'doctor_schedule.html', {
                'doctor': doctor,
                'schedules': schedules
            })
        except Doctor.DoesNotExist:
            return redirect('doctor_login')

    return redirect('doctor_login')

def patient_appointments(request):
    patient_id = request.session.get('patient_id')  # Get patient ID from session

    if not patient_id:
        return redirect('login')  # Redirect to login if not logged in

    try:
        patient = Patients.objects.get(p_id=request.session['patient_id'])  # Use 'p_id' instead of 'id'
        appointments = Appointment.objects.filter(a_patient=Patients)
        return render(request, 'appointments.html', {'appointments': appointments})
    except Patients.DoesNotExist:
        return redirect('patient_dashboard')  # Redirect if patient not found
def doctor_appointment_view(request):
    if 'doctor_id' in request.session:
        try:

            doctor = Doctor.objects.get(p_id=request.session['doctor_id'])
            print(f"Doctor found: {doctor}")  # Debugging

            appointments = Appointment.objects.filter(doctor=doctor)  # Change 'a_doctor' to actual field name
            print(appointments.query)  # Debugging

            return render(request, 'doctor_appointment_view.html', {
                'doctor': doctor,
                'appointments': appointments
            })
        except Doctor.DoesNotExist:
            return redirect('doctor_login')

    return redirect('doctor_login')


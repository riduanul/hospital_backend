from django.contrib import admin
from appointment.models import Appointment

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import Http404
# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [ 'patient_name', 'doctor_name', 'appointment_types', 'appointment_status','symptoms', 'time']

    def patient_name(self, obj):
        return obj.patient.user.first_name
    
    def doctor_name(self, obj):
        return obj.doctor.user.last_name
    
    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.appointment_status == 'Running' and obj.appointment_types == 'Online':
            email_subject = "Your Online Doctor Appointment"
            email_body = render_to_string('admin_email.html', {'user': obj.patient.user, 'doctor': obj.doctor})
           
            email = EmailMultiAlternatives(email_subject, '', to={obj.patient.user.email})
            email.attach_alternative(email_body, 'text/html')
            email.send()

admin.site.register(Appointment, AppointmentAdmin)

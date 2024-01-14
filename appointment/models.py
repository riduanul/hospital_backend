from django.db import models
from doctor.models import Doctor, AvailableTime
from patient.models import Patient
# Create your models here.

APPOINTMENT_STATUS = [
    ('Completed', 'Completed' ),
    ('Pending', 'Pending' ),
    ('Running', 'Running' ),
]

APPOINTMENT_TYPES = [
    ('Offline', 'Offline' ),
    ('Online', 'Online' ),
]
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE )
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE )
    appointment_types = models.CharField(choices = APPOINTMENT_TYPES, max_length = 10)
    appointment_status = models.CharField(choices = APPOINTMENT_STATUS, max_length = 10, default = "Pending")
    symptoms = models.TextField()
    time = models.ForeignKey(AvailableTime, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    cancel = models.BooleanField(default = False)

    def __str__(self):
        return f'Doctor: {self.doctor.user.first_name},  Patient:{self.patient.user.first_name} '

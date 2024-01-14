from django.shortcuts import render
from rest_framework import viewsets, filters, pagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly 
from doctor.models import Doctor, Designation, Specialization, AvailableTime, Review
from doctor.serializers import DoctorSerializer, ReviewSerializer, DesignationSerializer, SpecializationSerializer, AvailableTimeSerializer

# Create your views here.
class DoctorPagination(pagination.PageNumberPagination):
    page_size = 1 #items per page
    page_size_query_param = page_size
    max_page_size = 100

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__email', 'designation__name', 'specialization__name']
    pagination_class = DoctorPagination


class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

class AvailableTimeForSpecificDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        doctor_id = request.query_params.get('doctor_id')
        if doctor_id :
            return query_set.filter(doctor = doctor_id)
        return query_set

class AvailableTimeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer
    filter_backends =[ AvailableTimeForSpecificDoctor]




class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


from rest_framework import routers, serializers, viewsets
from contact_us.models import ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
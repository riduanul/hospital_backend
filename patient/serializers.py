from rest_framework import serializers
from patient.models import Patient
from django.contrib.auth.models import User


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Patient
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def save(self):
        username = self.validated_data['username']
        firstName = self.validated_data['first_name']
        lastName = self.validated_data['last_name']
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password :
            raise serializers.ValidationError({'Error': 'Password Not Matched'})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'Error': "Email Already Exists"})
        
        account = User(username = username, first_name = firstName, last_name = lastName, email = email)
        account.set_password(password)
        account.is_active = False
        account.save()
        print(account)
        return account

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField( required = True)
    password = serializers.CharField( required = True)
    
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from patient.models import Patient
from patient.serializers import PatientSerializer, RegistrationSerializer, UserLoginSerializer

#for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import Http404
# Create your views here.

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class UserRegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            print('token', token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid)
            confirm_link = f"http://127.0.0.1:8000/patient/active/{uid}/{token}/"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
           
            email = EmailMultiAlternatives(email_subject, '', to={user.email})
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response("Check Your Email For Confirmation")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk = uid)
        print(uid, user)
    except (User.DoesNotExist):
        user = None
        raise Http404("Invalid activation link")

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username= username, password= password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': 'Invalid Credential'})
    
        return Response(serializer.error)

class UserLogoutApiView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')

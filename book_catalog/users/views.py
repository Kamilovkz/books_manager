from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (UserRegistrationSerializer, UserLoginSerializer)

###########
# FOR THIS TASK USUALLY USE mailgun
###########
from django.core.mail import send_mail
###########


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Realization of email confirmation
            # send_mail(
            #     'Account Confirmation',
            #     'Thank you for registering. Please click the link to confirm your email.',
            #     'noreply@example.com',
            #     [user.email],
            #     fail_silently=False,
            # )
            
            return Response({'message': 'User registered successfully'})
        return Response(serializer.errors, status=400)



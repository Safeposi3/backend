from rest_framework import permissions, serializers,validators
from api.models import CustomUser
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # use your custom User model
        fields = ('email', 'first_name', 'last_name', 'password',)  # adjust the fields as needed

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    validators.UniqueValidator(
                        queryset=CustomUser.objects.all(),  # use your custom User model
                        message='A user with that email already exists.'
                    )
                ]
            }
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(AuthTokenSerializer):
    username = None
    email = serializers.EmailField()

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'birthdate',
            'phonenumber',
            'country',
            'address',
            'postal_code',
            'city',
            'dni',
        ]
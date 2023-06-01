from rest_framework import permissions, serializers,validators
from api.models import CustomUser
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'birthdate', 'phonenumber', 'country', 'address', 'postal_code', 'city', 'dni')
        
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    validators.UniqueValidator(
                        queryset=CustomUser.objects.all(),
                        message='A user with that email already exists.'
                    )
                ]
            },
            'birthdate': {'required': False},
            'phonenumber': {'required': False},
            'country': {'required': False},
            'address': {'required': False},
            'postal_code': {'required': False},
            'city': {'required': False},
            'dni': {'required': False},
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birthdate=validated_data['birthdate'],
            phonenumber=validated_data['phonenumber'],
            country=validated_data['country'],
            address=validated_data['address'],
            postal_code=validated_data['postal_code'],
            city=validated_data['city'],
            dni=validated_data['dni'],
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
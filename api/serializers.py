from django.contrib.auth.models import User
from rest_framework import serializers, validators

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), 'A user with that Email already exists'
                    )
                ]
            }
        }

    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        
        user.save()
        return user

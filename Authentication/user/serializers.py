from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        error_messages={
            'min_length': 'Password must be at least 6 characters.',
            'blank': 'Password cannot be empty.',
            'required': 'Password is required.',
        }
    )
    email = serializers.EmailField(
        error_messages={
            'invalid': 'Please enter a valid email address.',
            'required': 'Email address is required.',
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {
                'error_messages': {
                    'required': 'Username is required.',
                    'blank': 'Username cannot be empty.',
                    'unique': 'This username is already taken.',
                }
            },
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value.lower()

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate_password(self, value):
        if value.isdigit():
            raise serializers.ValidationError('Password cannot be entirely numeric.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(
        error_messages={
            'invalid': 'Please enter a valid email address.',
            'required': 'Email address is required.',
            'blank': 'Email cannot be empty.',
        }
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password cannot be empty.',
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def validate(self, attrs):
        email = attrs.get('email', '').lower()
        password = attrs.get('password')

        # User existence check
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'No account found with this email address.'
            )

        # Password check
        if not check_password(password, user.password):
            raise serializers.ValidationError(
                'Incorrect password. Please try again.'
            )

        # Active check
        if not user.is_active:
            raise serializers.ValidationError(
                'Your account has been disabled. Please contact support.'
            )

        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': user.email,
        }
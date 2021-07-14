from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True)

    # we are declaring password2 separately as because we passed this field in our serializer

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password !=  password2:
            raise serializers.ValidationError({'error': 'password does not matches'})

        # here with our password2 we passes the functionality that both password and password2 should be same
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({
                'error': 'Already exists, Use another Email'
            })

        # creating an instance called account to store email and username 
        # from user to this instance

        account = User(
            email=self.validated_data['email'], 
            username=self.validated_data['username']
            )
        # we have created an instance called account in which we are fetching emails and username form User
        account.set_password(password)
        account.save()
        # In the above line we are setting password for our account instance. and later saved that

        return account
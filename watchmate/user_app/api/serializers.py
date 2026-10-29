from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def save(self):
      password = self.validated_data['password']
      password2 = self.validated_data['password2']
      if password != password2:
          raise serializers.ValidationError({'password': 'Passwords must match.'})
      
      if User.objects.filter(email=self.validated_data['email']).exists():
          raise serializers.ValidationError({'email': 'Email already exists.'}) 
      
      account = User(
        username=self.validated_data['username'],email=self.validated_data['email']
      )
      account.set_password(password) #set_password is a method provided by Django's User model that hashes the password before saving it to the database. This ensures that the password is stored securely and not in plain text.
      account.save()
      return account
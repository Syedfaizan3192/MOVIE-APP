from asyncore import write
from dataclasses import field
from pyexpat import model
from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password2  = serializers.CharField(style={"input_type": "password"}, write_only = True)

    class Meta:
       model =  User
       fields = ["username", "password", "email", "password2"]
       write_only_fields = "password2",
       
    def save(self):
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'Passsword not matched'})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'Email already exists'})
        
        account = User(email = self.validated_data['email'], username = self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account
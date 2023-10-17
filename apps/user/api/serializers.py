from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TestUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, username):
        # custom validation
        if 'yostintejaxun' in username:
            raise serializers.ValidationError('username is already being used')
        return username

    def validate_email(self, email):
        # custom validation
        if email == '':
            raise serializers.ValidationError('Email is required')

        # context
        if self.validate_username(self.context.get('username')) in self.context.get('email'):
            raise serializers.ValidationError('email could not contain name')

        return email

    def validate(self, data):
        # if data['username'] in data['email']:
        #     raise serializers.ValidationError('email could not contain name')
        return data
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)

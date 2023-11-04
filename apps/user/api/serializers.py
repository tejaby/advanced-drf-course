from rest_framework import serializers

from django.contrib.auth.models import User


"""
Serializer general para la obtencion y creacion de usuarios

"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


"""
Serializer para la actualización de usuarios
= No hace falta el metodo update para encriptar el password en este serializador

"""


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    # def update(self, instance, validated_data):
    #     update_user = super().update(instance, validated_data)
    #     update_user.set_password(validated_data['password'])
    #     update_user.save()
    #     return update_user


"""
Serializer para listar usuarios.
- Con values(): QuerySet seria de diccionarios. se accederia intance['username']
- Sin values(): la QuerySet seria de objetos (instancias de modelos). se accederia intance.username


"""


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):

        return {'id': instance['id'],
                'username': instance['username'],
                'email': instance['email'],
                'first_name': instance['first_name'],
                'last_name': instance['last_name']}


"""
Serializer para obtencion de los datos del usuario autenticado

"""


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


"""
Serializer para validar el inicio de sesión utilizando email en lugar de username.
- Se podria hacer con authenticate en lugar de hacer la consulta a User pero hay que modificar el metodo 


"""


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                attrs['user'] = user  # user autenticado se almacena en attrs
            else:
                raise serializers.ValidationError(
                    'email or password are incorrect')
        else:
            raise serializers.ValidationError(
                'must include email and password')
        return attrs


# class TestUserSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField()

#     def validate_username(self, username):
#         # custom validation
#         if 'yostintejaxun' in username:
#             raise serializers.ValidationError('username is already being used')
#         return username

#     def validate_email(self, email):
#         # custom validation
#         if email == '':
#             raise serializers.ValidationError('Email is required')

#         # context
#         # if self.validate_username(self.context.get('username')) in self.context.get('email'):
#         #     raise serializers.ValidationError('email could not contain name')

#         return email

#     def validate(self, data):
#         # if data['username'] in data['email']:
#         #     raise serializers.ValidationError('email could not contain name')
#         return data

#     def create(self, validated_data):
#         return User.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.email = validated_data.get('email', instance.email)
#         instance.save()
#         return instance

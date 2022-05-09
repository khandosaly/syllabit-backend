import json

import requests
from rest_framework import serializers
from .models import User


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('keystore', 'password')
        extra_kwargs = {
            "keystore": {"required": True},
            "password": {"required": True},
        }

    def create(self, validated_data):
        response = requests.post(
            'http://127.0.0.1:8001/api/v1.0/info',
            verify=False,
            data=json.dumps(validated_data),
            headers={
                'Content-Type': 'application/json',
                'Accept-Encoding': 'gzip, deflate, br'
            }
        )
        user = User.objects.get_or_create(
            response.json().get('iin'),
            response.json().get('subject'),
        )
        return user


import re
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = [
            'email',
            'username',
            'password',
        ]

    def validate_password(self, password):
        """
        validate password
        :param password:
        :return:
        """
        if re.search(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$", password) is not None:
            return password
        raise serializers.ValidationError(
            'Password must be at least six characters, '
            'alphanumeric character and must contain at least one special character'
        )

    def validate_email(self, email):
        """
        validate email
        :param email:
        :return:
        """
        if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is not None:
            return email
        raise serializers.ValidationError(
            'Enter a valid email address'
        )

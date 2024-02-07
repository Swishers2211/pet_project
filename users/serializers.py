from rest_framework import serializers

from users.models import User, Portfolio

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['active_role', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['active_role', 'username', 'email', 'description', 'phone']

# class PortfolioPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PortfolioPhoto
#         fields = [
#             "image",
#         ]

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ["title", "user", "descriptions", "link", "images"]

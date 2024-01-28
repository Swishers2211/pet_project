from rest_framework import serializers

from home.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'user', 'image', 'main_category', 'category', 'sub_category', 'price']

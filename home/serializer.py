from rest_framework import serializers

from home.models import Project, Respond

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'client', 'image', 'main_category', 'category', 'sub_category', 'price']

class RespondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respond
        fields = ['project', 'master', 'published']


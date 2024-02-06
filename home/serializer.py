from rest_framework import serializers

from home.models import Project, Respond

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'client', 'image', 'main_category', 'category', 'sub_category', 'price']
        
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'image', 'main_category', 'category', 'sub_category', 'price']
        
        def validate(self, attrs):
            attrs = super().validate(attrs)
            attrs['client'] = self.context['client']
            return attrs


class RespondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respond
        fields = ['project', 'master', 'description', 'published']
        
class RespondCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respond
        fields = ['description', 'published']
        
        def validate(self, attrs):
            attrs = super().validate(attrs)
            attrs['project'] = self.context['project']
            attrs['master'] = self.context['master']
            return attrs

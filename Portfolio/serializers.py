from rest_framework import serializers
from .models import Education, Experience, Project, Skill


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'proficiency')
        read_only_fields = ('id',)

class SkillSerializer(OwnerSerializer):
    class Meta(OwnerSerializer.Meta): model = Skill

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education; exclude = ('user', 'created_at')
        read_only_fields = ('id',)

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience; exclude = ('user', 'created_at')
        read_only_fields = ('id',)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project; exclude = ('user', 'created_at')
        read_only_fields = ('id',)

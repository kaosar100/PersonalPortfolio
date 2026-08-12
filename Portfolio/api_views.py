"""DRF API views for portfolio data.

Each endpoint is restricted to the authenticated user's own portfolio records.
"""

from rest_framework import generics, mixins, permissions

from .models import Education, Experience, Project, Skill
from .serializers import (
    EducationSerializer,
    ExperienceSerializer,
    ProjectSerializer,
    SkillSerializer,
)


class OwnerAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Provide CRUD actions only for records owned by the logged-in user."""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SkillAPI(OwnerAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class EducationAPI(OwnerAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class ExperienceAPI(OwnerAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ProjectAPI(OwnerAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

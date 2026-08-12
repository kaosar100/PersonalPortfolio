"""URL patterns for the Portfolio REST API."""

from django.urls import path

from . import api_views


urlpatterns = [
    path('skills/', api_views.SkillAPI.as_view(), name='api_skills'),
    path('skills/<int:pk>/', api_views.SkillAPI.as_view(), name='api_skills_detail'),
    path('education/', api_views.EducationAPI.as_view(), name='api_education'),
    path('education/<int:pk>/', api_views.EducationAPI.as_view(), name='api_education_detail'),
    path('experience/', api_views.ExperienceAPI.as_view(), name='api_experience'),
    path('experience/<int:pk>/', api_views.ExperienceAPI.as_view(), name='api_experience_detail'),
    path('projects/', api_views.ProjectAPI.as_view(), name='api_projects'),
    path('projects/<int:pk>/', api_views.ProjectAPI.as_view(), name='api_projects_detail'),
]

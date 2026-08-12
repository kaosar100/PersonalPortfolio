from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), path('login/', views.LoginView.as_view(), name='login'), path('register/', views.RegisterView.as_view(), name='register'), path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'), path('dashboard/profile/', views.ProfileUpdateView.as_view(), name='profile_edit'), path('resume/', views.ResumeView.as_view(), name='resume'), path('contact/', views.ContactView.as_view(), name='contact'),
    path('api/', include('Portfolio.api_urls')),

    # Skill
    path('dashboard/skills/add/', views.SkillCreate.as_view(), name='skills_add'),
    path('dashboard/skills/<int:pk>/edit/', views.SkillUpdate.as_view(), name='skills_edit'),
    path('dashboard/skills/<int:pk>/delete/', views.SkillDelete.as_view(), name='skills_delete'),

    # Education
    path('dashboard/education/add/', views.EducationCreate.as_view(), name='education_add'),
    path('dashboard/education/<int:pk>/edit/', views.EducationUpdate.as_view(), name='education_edit'),
    path('dashboard/education/<int:pk>/delete/', views.EducationDelete.as_view(), name='education_delete'),

    # Experience 
    path('dashboard/experience/add/', views.ExperienceCreate.as_view(), name='experience_add'),
    path('dashboard/experience/<int:pk>/edit/', views.ExperienceUpdate.as_view(), name='experience_edit'),
    path('dashboard/experience/<int:pk>/delete/', views.ExperienceDelete.as_view(), name='experience_delete'),

    # Project
    path('dashboard/projects/add/', views.ProjectCreate.as_view(), name='projects_add'),
    path('dashboard/projects/<int:pk>/edit/', views.ProjectUpdate.as_view(), name='projects_edit'),
    path('dashboard/projects/<int:pk>/delete/', views.ProjectDelete.as_view(), name='projects_delete'),
]

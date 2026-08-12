from django.contrib import admin
from .models import ContactMessage, Education, Experience, Profile, Project, Skill

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): list_display = ('full_name', 'user', 'headline')

@admin.register(Skill, Education, Experience, Project)
class OwnedAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'created_at')
    list_filter = ('user',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read',)

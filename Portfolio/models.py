from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolio_profile')
    full_name = models.CharField(max_length=120, blank=True)
    headline = models.CharField(max_length=180, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return self.full_name or self.user.get_username()


class OwnedModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Skill(OwnedModel):
    name = models.CharField(max_length=80)
    proficiency = models.PositiveSmallIntegerField(default=75, help_text='0 to 100')

    class Meta:
        ordering = ['-proficiency', 'name']
        constraints = [models.UniqueConstraint(fields=['user', 'name'], name='unique_user_skill')]

    def __str__(self): return self.name


class Education(OwnedModel):
    institution = models.CharField(max_length=180)
    degree = models.CharField(max_length=180)
    field_of_study = models.CharField(max_length=180, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    class Meta: ordering = ['-start_date']
    def __str__(self): return f'{self.degree} — {self.institution}'


class Experience(OwnedModel):
    company = models.CharField(max_length=180)
    role = models.CharField(max_length=180)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    class Meta: ordering = ['-start_date']
    def __str__(self): return f'{self.role} at {self.company}'


class Project(OwnedModel):
    title = models.CharField(max_length=180)
    summary = models.TextField()
    technologies = models.CharField(max_length=255, help_text='Separate technologies with commas')
    live_url = models.URLField(blank=True)
    repository_url = models.URLField(blank=True)
    completed_on = models.DateField(blank=True, null=True)
    class Meta: ordering = ['-completed_on', '-created_at']
    def __str__(self): return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f'{self.subject} — {self.name}'

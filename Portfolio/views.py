from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView
from .forms import ContactForm, EducationForm, ExperienceForm, LoginForm, ProfileForm, ProjectForm, RegistrationForm, SkillForm
from .models import Education, Experience, Profile, Project, Skill


def profile_for(user):
    return Profile.objects.get_or_create(user=user)[0]


class HomeView(TemplateView):
    template_name = 'Portfolio/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if owner:
            context.update(profile=profile_for(owner), skills=Skill.objects.filter(user=owner), projects=Project.objects.filter(user=owner)[:3])
        return context


class LoginView(View):
    template_name = 'Portfolio/login.html'
    def get(self, request): return render(request, self.template_name, {'form': LoginForm()})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            username = User.objects.filter(email__iexact=identifier).values_list('username', flat=True).first() or identifier
            user = authenticate(request, username=username, password=form.cleaned_data['password'])
            if user:
                login(request, user); return redirect('dashboard')
            form.add_error(None, 'Username/email or password is incorrect.')
        return render(request, self.template_name, {'form': form})


class RegisterView(CreateView):
    
    form_class = RegistrationForm
    template_name = 'Portfolio/register.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        profile_for(self.object)
        login(self.request, self.object)
        messages.success(self.request, 'Welcome! Your portfolio is ready to personalise.')
        return response


class LogoutView(View):
    
    def post(self, request): 
        logout(request) 
        return redirect('home')


class DashboardView(LoginRequiredMixin, TemplateView):
    
    template_name = 'Portfolio/dashboard.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = self.request.user
        data.update(profile=profile_for(user), 
                    skills=Skill.objects.filter(user=user), 
                    educations=Education.objects.filter(user=user), 
                    experiences=Experience.objects.filter(user=user), 
                    projects=Project.objects.filter(user=user))
        
        return data


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    
    form_class = ProfileForm 
    template_name = 'Portfolio/form.html' 
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'Edit your profile'}
    
    
    def get_object(self, queryset=None): 
        return profile_for(self.request.user)


class OwnedQuerysetMixin(LoginRequiredMixin):
    
    def get_queryset(self): 
        
        return self.model.objects.filter(user=self.request.user)

class OwnedCreateView(LoginRequiredMixin, CreateView):
    
    template_name = 'Portfolio/form.html'; success_url = reverse_lazy('dashboard')
    def form_valid(self, form): 
        
        form.instance.user = self.request.user 
        
        return super().form_valid(form)

class OwnedUpdateView(OwnedQuerysetMixin, UpdateView):
    
    template_name = 'Portfolio/form.html'; success_url = reverse_lazy('dashboard')

class OwnedDeleteView(OwnedQuerysetMixin, DeleteView):
    
    template_name = 'Portfolio/confirm_delete.html'; success_url = reverse_lazy('dashboard')


class SkillCreate(OwnedCreateView):
    
    model = Skill
    form_class = SkillForm 
    extra_context = {'title': 'Add a skill'}


class SkillUpdate(OwnedUpdateView): 
    
    model = Skill; form_class = SkillForm 
    extra_context = {'title': 'Edit skill'}
    
    
class SkillDelete(OwnedDeleteView): 
    
    model = Skill 
    extra_context = {'title': 'Delete skill'}
    
class EducationCreate(OwnedCreateView): 
    
    model = Education
    
    form_class = EducationForm 
    extra_context = {'title': 'Add education'}
    
    
class EducationUpdate(OwnedUpdateView):
    
    model = Education
    form_class = EducationForm
    extra_context = {'title': 'Edit education'}
    
    
class EducationDelete(OwnedDeleteView): 
    
    model = Education
    extra_context = {'title': 'Delete education'}
    
    
class ExperienceCreate(OwnedCreateView):
    
    model = Experience 
    form_class = ExperienceForm 
    extra_context = {'title': 'Add experience'}
    
    
class ExperienceUpdate(OwnedUpdateView):
    
    model = Experience
    form_class = ExperienceForm
    extra_context = {'title': 'Edit experience'}
    
    
class ExperienceDelete(OwnedDeleteView):
    
    model = Experience 
    extra_context = {'title': 'Delete experience'}
    
    
class ProjectCreate(OwnedCreateView): 
    
    model = Project
    form_class = ProjectForm
    extra_context = {'title': 'Add project'}
    
    
class ProjectUpdate(OwnedUpdateView): 
    
    model = Project
    form_class = ProjectForm
    extra_context = {'title': 'Edit project'}
    
    
class ProjectDelete(OwnedDeleteView): 
    
    model = Project
    extra_context = {'title': 'Delete project'}


class ResumeView(LoginRequiredMixin, TemplateView):
    
    template_name = 'Portfolio/resume.html'
    
    def get_context_data(self, **kwargs):
        user = self.request.user; data = super().get_context_data(**kwargs)
        data.update(profile=profile_for(user), skills=Skill.objects.filter(user=user), educations=Education.objects.filter(user=user), experiences=Experience.objects.filter(user=user), projects=Project.objects.filter(user=user))
        return data

class ContactView(View):
    
    template_name = 'Portfolio/contact.html'
    
    def get(self, request): 
        return render(request, self.template_name, {'form': ContactForm()})
    
    
    def post(self, request):
        
        form = ContactForm(request.POST)
        
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Thanks — your message has been sent.'); return redirect('contact')
        
        return render(request, self.template_name, {'form': form})


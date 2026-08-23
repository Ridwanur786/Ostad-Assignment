from django.shortcuts import render
from .models import Project

# Create your views here.

def home(request):
    projects = Project.objects.all()[:3]  # Show top 3 projects on homepage
    return render(request, 'core/index.html', {'projects': projects})

def about(request):
    return render(request, 'core/about.html')

def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'core/projects.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'core/project_detail.html', {'project': project})

def contact(request):
    return render(request, 'core/contact.html')

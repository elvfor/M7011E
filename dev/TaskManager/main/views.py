from django.db.models import Count
from django.shortcuts import render
from organization.models import Organization
from project.models import Project

def organizations_view(request):
    """Display a list of organizations and their users."""
    context = {
        'organizations': Organization.objects.all()
        #'organizations': Organization.objects.prefetch_related('users').all()
    }
    return render(request, 'pages/organizations.html', context)


def projects_view(request):
    """Display a list of projects and their organization."""
    context = {
        #'projects': Project.objects.all()
        'projects': Project.objects.select_related('pages/organization').all()

    }
    return render(request, 'pages/projects.html', context)

def organization_users_view(request):
    """Display a list of organizations and their number of users."""
    context = {
        #'organizations': Organization.objects.all()
        'organizations':  Organization.objects.annotate(user_count=Count('users'))

    }
    return render(request, 'pages/organization_users.html', context)


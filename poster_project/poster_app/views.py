from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Project, Design

def landing_page(request):
    return render(request, 'poster_app/landing_page.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'poster_app/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        Project.objects.create(
            user=request.user,
            name=request.POST['name'],
            description=request.POST['description']
        )
    return redirect('project_list')

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == 'POST':
        project.delete()
    return redirect('project_list')

@login_required
def design_page(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    # Mock chat history and design data
    mock_chat_history = [
        {'sender': 'user', 'message': 'Make a poster for a summer music festival.'},
        {'sender': 'bot', 'message': 'Sure! What style are you thinking of?'},
        {'sender': 'user', 'message': 'Something vibrant and retro.'},
    ]

    mock_design_data = {
        'background_color': '#FFC107',
        'title_text': 'Summer Fest',
        'title_font': 'Arial',
        'body_text': 'Feat. The Sunny Tones, The Cool Breezes, and more!',
    }

    context = {
        'project': project,
        'chat_history': mock_chat_history,
        'design_data': mock_design_data,
    }
    return render(request, 'poster_app/design_page.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Project, Design
from django.http import JsonResponse
import json

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
def profile_page(request):
    return render(request, 'poster_app/profile_page.html')

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
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == 'POST':
        project.name = request.POST['name']
        project.description = request.POST['description']
        project.save()
        return redirect('project_list')
    return render(request, 'poster_app/project_update.html', {'project': project})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == 'POST':
        project.delete()
    return redirect('project_list')

@login_required
def design_page(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    design, created = Design.objects.get_or_create(
        project=project,
        defaults={'design_data': {'chat_history': [], 'design': {}}}
    )

    context = {
        'project': project,
        'chat_history': design.design_data.get('chat_history', []),
        'design_data': design.design_data.get('design', {}),
    }
    return render(request, 'poster_app/design_page.html', context)

@login_required
def chat_message(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id, user=request.user)
        design = Design.objects.get(project=project)

        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Add user message to history
        design.design_data['chat_history'].append({'sender': 'user', 'message': user_message})

        # Mock bot response and design update
        bot_message = "I'm not sure how to do that. Try 'change background to blue'."
        design_update = {}

        if 'background' in user_message.lower():
            color = user_message.lower().split(' to ')[-1]
            bot_message = f"Okay, I've changed the background to {color}."
            design_update = {'background_color': color}
        elif 'title' in user_message.lower():
            title_text = user_message.replace('title', '').strip()
            bot_message = "Title updated!"
            design_update = {'title_text': title_text}

        # Add bot message to history and update design
        design.design_data['chat_history'].append({'sender': 'bot', 'message': bot_message})
        design.design_data['design'].update(design_update)
        design.save()

        return JsonResponse({
            'sender': 'bot',
            'message': bot_message,
            'design_update': design_update
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

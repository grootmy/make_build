from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Project, Design
from django.http import JsonResponse, HttpResponse
import json
import re

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
def project_clone(request, project_id):
    original_project = get_object_or_404(Project, id=project_id, user=request.user)

    # Create new project
    new_project = Project.objects.create(
        user=request.user,
        name=f"{original_project.name} (Copy)",
        description=original_project.description
    )

    # Clone design if it exists
    try:
        original_design = Design.objects.get(project=original_project)
        Design.objects.create(
            project=new_project,
            design_data=original_design.design_data
        )
    except Design.DoesNotExist:
        pass # No design to clone

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
        design, _ = Design.objects.get_or_create(project=project, defaults={'design_data': {'chat_history': [], 'design': {}}})

        data = json.loads(request.body)
        user_message = data.get('message', '')
        design.design_data['chat_history'].append({'sender': 'user', 'message': user_message})

        # Extended Mock bot logic
        bot_message = "Sorry, I didn't understand. Try 'set title to...', 'change background to...', 'set font size to 32px', 'align text to left'."
        design_update = {}

        msg_lower = user_message.lower()

        # Match background color
        if 'background' in msg_lower:
            color_match = re.search(r'to\s+([a-zA-Z]+|#[0-9a-fA-F]{6})', msg_lower)
            if color_match:
                color = color_match.group(1)
                bot_message = f"Background color changed to {color}."
                design_update['background_color'] = color

        # Match title text
        elif 'title to' in msg_lower:
            title_text = user_message.split('to', 1)[-1].strip()
            bot_message = "Title updated."
            design_update['title_text'] = title_text

        # Match font size
        elif 'font size' in msg_lower:
            size_match = re.search(r'(\d+)(px|pt|em)', msg_lower)
            if size_match:
                size = size_match.group(1) + size_match.group(2)
                bot_message = f"Font size set to {size}."
                design_update['font_size'] = size

        # Match text alignment
        elif 'align text' in msg_lower:
            align_match = re.search(r'to\s+(left|center|right)', msg_lower)
            if align_match:
                alignment = align_match.group(1)
                bot_message = f"Text aligned to {alignment}."
                design_update['text_align'] = alignment

        design.design_data['chat_history'].append({'sender': 'bot', 'message': bot_message})
        design.design_data['design'].update(design_update)
        design.save()

        return JsonResponse({
            'sender': 'bot',
            'message': bot_message,
            'design_update': design_update
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

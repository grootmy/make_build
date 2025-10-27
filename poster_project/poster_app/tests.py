from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Project, Design

class PosterAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.project = Project.objects.create(user=self.user, name='Test Project')

    def test_project_creation(self):
        """Test if a logged-in user can create a project."""
        response = self.client.post('/projects/create/', {'name': 'New Test Project', 'description': 'A test description.'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name='New Test Project').exists())

    def test_project_list_view(self):
        """Test the project list view."""
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

    def test_project_clone(self):
        """Test the project cloning functionality."""
        Design.objects.create(project=self.project, design_data={'test': 'data'})
        response = self.client.post(f'/projects/{self.project.id}/clone/')
        self.assertEqual(response.status_code, 302)

        cloned_project = Project.objects.get(name='Test Project (Copy)')
        self.assertIsNotNone(cloned_project)
        self.assertTrue(Design.objects.filter(project=cloned_project).exists())
        self.assertEqual(Design.objects.get(project=cloned_project).design_data, {'test': 'data'})

    def test_chat_font_size_command(self):
        """Test the chat API for font size command."""
        response = self.client.post(
            f'/projects/{self.project.id}/chat/',
            data='{"message": "set font size to 32px"}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['design_update']['font_size'], '32px')

    def test_chat_text_align_command(self):
        """Test the chat API for text align command."""
        response = self.client.post(
            f'/projects/{self.project.id}/chat/',
            data='{"message": "align text to right"}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['design_update']['text_align'], 'right')

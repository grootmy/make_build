from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Project

class PosterAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_project_creation(self):
        """Test if a logged-in user can create a project."""
        response = self.client.post('/projects/create/', {'name': 'New Test Project', 'description': 'A test description.'})
        self.assertEqual(response.status_code, 302) # Should redirect to project list
        self.assertTrue(Project.objects.filter(name='New Test Project').exists())

    def test_project_list_view(self):
        """Test the project list view for a logged-in user."""
        Project.objects.create(user=self.user, name='My First Project')
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My First Project')

    def test_chat_message_api(self):
        """Test the chat message API endpoint."""
        project = Project.objects.create(user=self.user, name='Chat Project')
        response = self.client.post(
            f'/projects/{project.id}/chat/',
            data='{"message": "change background to blue"}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['sender'], 'bot')
        self.assertIn('background_color', json_response['design_update'])

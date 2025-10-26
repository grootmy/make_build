from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Design(models.Model):
    project = models.ForeignKey(Project, related_name='designs', on_delete=models.CASCADE)
    design_data = models.JSONField()  # To store chat messages and design parameters
    preview_image = models.ImageField(upload_to='designs/previews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Design for {self.project.name} - {self.created_at.strftime('%Y-%m-%d')}"

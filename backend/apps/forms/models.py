import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone

User = get_user_model()

class Form(models.Model):
	STATUS_CHOICES = [
		('draft', 'Draft'),
		('published', 'Published'),
		('archived', 'Archived'),
	]

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	schema = models.JSONField(default=dict)  # Store form structure as JSON
	version = models.PositiveIntegerField(default=1)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	published_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ['-updated_at']
	def __str__(self) -> str:
		return self.title
	
	def save(self, *args, **kwargs):
		if self.status == 'published' and self.published_at is None:
			self.published_at = timezone.now()
		super().save(*args, **kwargs)

class FormVersion(models.Model):
	form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='versions')
	version = models.PositiveIntegerField()
	schema = models.JSONField(default=dict)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('form', 'version')
		ordering = ['-version']
	def __str__(self) -> str:
		return f"{self.form.title} - v{self.version}"
	
class FormTheme(models.Model):
    name = models.CharField(max_length=100)
    primary_color = models.CharField(max_length=7, validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$')])
    secondary_color = models.CharField(max_length=7, validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$')])
    font_family = models.CharField(max_length=100, default='Arial, sans-serif')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
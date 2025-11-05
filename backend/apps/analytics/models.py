# apps/analytics/models.py
from django.db import models
from django.contrib.auth import get_user_model
from apps.forms.models import Form

User = get_user_model()

class FormAnalytics(models.Model):
    form = models.OneToOneField(Form, on_delete=models.CASCADE, related_name='analytics')
    views = models.PositiveIntegerField(default=0)
    submissions = models.PositiveIntegerField(default=0)
    completion_rate = models.FloatField(default=0.0)
    average_completion_time = models.FloatField(default=0.0)  # in seconds
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.form.title}"

class FieldAnalytics(models.Model):
    form_analytics = models.ForeignKey(FormAnalytics, on_delete=models.CASCADE, related_name='field_analytics')
    field_id = models.CharField(max_length=100)  # ID of the field in the form schema
    field_type = models.CharField(max_length=50)
    response_count = models.PositiveIntegerField(default=0)
    abandonment_rate = models.FloatField(default=0.0)
    average_time_spent = models.FloatField(default=0.0)  # in seconds
    
    class Meta:
        unique_together = ['form_analytics', 'field_id']
        indexes = [
            models.Index(fields=['form_analytics', 'field_id']),
            models.Index(fields=['field_type']),
        ]
    
    def __str__(self):
        return f"Analytics for field {self.field_id} in {self.form_analytics.form.title}"
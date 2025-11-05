from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Form
from apps.analytics.models import FormAnalytics


@receiver(post_save, sender=Form)
def create_form_analytics(sender, instance: Form, created: bool, **kwargs):
    if created:
        FormAnalytics.objects.get_or_create(form=instance)



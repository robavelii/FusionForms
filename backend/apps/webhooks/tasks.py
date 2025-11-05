# apps/webhooks/tasks.py
from celery import shared_task
from .views import trigger_webhooks

@shared_task
def process_webhook(form_id, event_type, data):
    """Process webhooks asynchronously"""
    trigger_webhooks(form_id, event_type, data)
    return f"Processed {event_type} webhook for form {form_id}"
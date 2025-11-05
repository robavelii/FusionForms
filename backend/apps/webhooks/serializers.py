# apps/webhooks/serializers.py
from rest_framework import serializers
from .models import Webhook, WebhookLog

class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class WebhookLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookLog
        fields = '__all__'
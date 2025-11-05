# apps/analytics/serializers.py
from rest_framework import serializers
from .models import FormAnalytics, FieldAnalytics

class FieldAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldAnalytics
        fields = '__all__'

class FormAnalyticsSerializer(serializers.ModelSerializer):
    field_analytics = FieldAnalyticsSerializer(many=True, read_only=True)
    
    class Meta:
        model = FormAnalytics
        fields = '__all__'
# apps/submissions/serializers.py
from rest_framework import serializers
from .models import Submission, SavedForm

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('id', 'is_spam', 'created_at')

class SavedFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedForm
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
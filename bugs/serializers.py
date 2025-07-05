from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bug
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['contact_number', 'address', 'role']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']

class DeveloperStatsSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()
    in_progress = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'profile', 'completed', 'pending', 'in_progress']

    def get_completed(self, obj):
        return Bug.objects.filter(fixed_by=obj, status='Fixed').count()
    
    def get_pending(self, obj):
        # Bugs assigned to this developer that are still open
        return Bug.objects.filter(fixed_by=obj, status='Open').count()
    
    def get_in_progress(self, obj):
        return Bug.objects.filter(fixed_by=obj, status='In Progress').count()
    
class BugSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    fixed_by_username = serializers.CharField(source='fixed_by.username', read_only=True, allow_null=True)
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True, allow_null=True)

    class Meta:
        model = Bug
        fields = ['id', 'bugcode', 'info', 'status', 'created_at', 'updated_at', 'duration', 
                 'fixed_by', 'fixed_by_username', 'updated_by', 'updated_by_username']

    def get_duration(self, obj):
        if obj.created_at and obj.updated_at:
            return (obj.updated_at - obj.created_at).total_seconds() // 60 // 60
        return None
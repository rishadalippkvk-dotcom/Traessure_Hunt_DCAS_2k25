"""
REST API Serializers for Treasure Hunt Backend
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, GameSession, LevelProgress, Achievement, UserAchievement, Leaderboard, Question


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'total_score', 'games_played', 
                  'best_streak', 'rank', 'created_at', 'last_login_at']
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            data['user'] = user
        else:
            raise serializers.ValidationError("Must provide username and password")
        
        return data


class GameSessionSerializer(serializers.ModelSerializer):
    """Serializer for GameSession model"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = GameSession
        fields = ['id', 'username', 'session_token', 'started_at', 'completed_at',
                  'is_active', 'current_level', 'score', 'hints_used', 'current_streak',
                  'max_streak', 'perfect_levels', 'combo_multiplier', 'riddle_solved',
                  'wrong_attempts', 'security_wrong_attempts', 'finished']
        read_only_fields = ['id', 'session_token', 'started_at']


class LevelProgressSerializer(serializers.ModelSerializer):
    """Serializer for LevelProgress model"""
    # Add related fields for better display in admin dashboard
    username = serializers.CharField(source='session.user.username', read_only=True)
    session_id = serializers.IntegerField(source='session.id', read_only=True)
    
    class Meta:
        model = LevelProgress
        fields = ['id', 'session', 'session_id', 'username', 'level_number', 'question_category', 'difficulty',
                  'points_earned', 'bonus_points', 'riddle_attempts', 'security_attempts',
                  'hint_used', 'security_hint_used', 'riddle_solved', 'level_completed',
                  'completed_at', 'time_spent']
        read_only_fields = ['id', 'created_at']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model"""
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'icon', 'points']


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for UserAchievement model"""
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement', 'unlocked_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'username', 'final_score', 'total_time', 'completion_date',
                  'rank_achieved', 'accuracy', 'speed_score']
        read_only_fields = ['id', 'completion_date']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model - read-only for players, editable for admins"""
    class Meta:
        model = Question
        fields = ['level_number', 'question', 'answer', 'security_riddle', 
                  'security_key', 'hint', 'security_hint', 'category', 
                  'difficulty', 'points', 'is_active']
        
    def __init__(self, *args, **kwargs):
        # Check if this is for an update operation
        self.is_update = kwargs.pop('is_update', False)
        
        # Make fields read-only for non-admin users
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user') and not request.user.is_staff:
            # For non-admin users, make all fields read-only
            for field_name in self.fields:
                self.fields[field_name].read_only = True
        elif self.is_update:
            # For update operations, level_number should be read-only
            self.fields['level_number'].read_only = True
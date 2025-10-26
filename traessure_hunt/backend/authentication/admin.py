"""
Django Admin Configuration for Treasure Hunt Models
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, GameSession, LevelProgress, Achievement, UserAchievement, Leaderboard, Question


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'total_score', 'games_played', 'best_streak', 'rank', 'created_at']
    list_filter = ['rank', 'created_at', 'is_staff']
    search_fields = ['username', 'email']
    ordering = ['-total_score']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Game Stats', {
            'fields': ('total_score', 'games_played', 'best_streak', 'rank', 'last_login_at')
        }),
    )


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_token_short', 'current_level', 'score', 'is_active', 'finished', 'started_at']
    list_filter = ['is_active', 'finished', 'started_at']
    search_fields = ['user__username', 'session_token']
    readonly_fields = ['session_token', 'started_at']
    
    def session_token_short(self, obj):
        return f"{obj.session_token[:12]}..."
    session_token_short.short_description = 'Session Token'


@admin.register(LevelProgress)
class LevelProgressAdmin(admin.ModelAdmin):
    list_display = ['session', 'level_number', 'question_category', 'difficulty', 'points_earned', 'level_completed', 'time_spent']
    list_filter = ['difficulty', 'level_completed', 'hint_used']
    search_fields = ['session__user__username', 'question_category']
    ordering = ['session', 'level_number']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'points', 'description']
    search_fields = ['name', 'description']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'unlocked_at', 'session']
    list_filter = ['unlocked_at', 'achievement']
    search_fields = ['user__username', 'achievement__name']
    ordering = ['-unlocked_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'final_score', 'rank_achieved', 'total_time_formatted', 'accuracy', 'completion_date']
    list_filter = ['rank_achieved', 'completion_date']
    search_fields = ['user__username']
    ordering = ['-final_score', 'total_time']
    
    def total_time_formatted(self, obj):
        minutes = int(obj.total_time // 60)
        seconds = int(obj.total_time % 60)
        return f"{minutes}m {seconds}s"
    total_time_formatted.short_description = 'Total Time'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for managing game questions - admin only"""
    list_display = ['level_number', 'category', 'difficulty', 'points', 'is_active', 'updated_at']
    list_filter = ['difficulty', 'is_active', 'category']
    search_fields = ['question', 'category', 'answer']
    ordering = ['level_number']
    
    fieldsets = (
        ('Level Information', {
            'fields': ('level_number', 'category', 'difficulty', 'points', 'is_active')
        }),
        ('Main Riddle', {
            'fields': ('question', 'answer', 'hint')
        }),
        ('Security Challenge', {
            'fields': ('security_riddle', 'security_key', 'security_hint')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete questions
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        # Only superusers can add new questions
        return request.user.is_superuser

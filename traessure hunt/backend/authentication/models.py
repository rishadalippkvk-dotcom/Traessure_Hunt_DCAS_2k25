"""
Django Models for FOSS Treasure Hunt Authentication and Game Progress
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model for treasure hunt players
    """
    # Additional fields beyond default Django User
    total_score: int = models.IntegerField(default=0)  # type: ignore[assignment]
    games_played: int = models.IntegerField(default=0)  # type: ignore[assignment]
    best_streak: int = models.IntegerField(default=0)  # type: ignore[assignment]
    rank: str = models.CharField(max_length=100, default="🔰 BEGINNER CODER")  # type: ignore[assignment]
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:  # type: ignore[misc]
        db_table = 'users'
        ordering = ['-total_score']
    
    def __str__(self):
        return self.username


class GameSession(models.Model):
    """
    Tracks individual game sessions for each player
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_sessions')
    session_token = models.CharField(max_length=255, unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # type: ignore[assignment]
    
    # Game Stats
    current_level = models.IntegerField(default=0)  # type: ignore[assignment]
    score = models.IntegerField(default=0)  # type: ignore[assignment]
    hints_used = models.IntegerField(default=0)  # type: ignore[assignment]
    current_streak = models.IntegerField(default=0)  # type: ignore[assignment]
    max_streak = models.IntegerField(default=0)  # type: ignore[assignment]
    perfect_levels = models.IntegerField(default=0)  # type: ignore[assignment]
    combo_multiplier = models.FloatField(default=1.0)  # type: ignore[assignment]
    
    # Progress tracking
    riddle_solved = models.BooleanField(default=False)  # type: ignore[assignment]
    wrong_attempts = models.IntegerField(default=0)  # type: ignore[assignment]
    security_wrong_attempts = models.IntegerField(default=0)  # type: ignore[assignment]
    finished = models.BooleanField(default=False)  # type: ignore[assignment]
    game_completed_permanently = models.BooleanField(default=False, help_text="Game completed - no replay allowed")  # type: ignore[assignment]
    
    class Meta:
        db_table = 'game_sessions'
        ordering = ['-started_at']
    
    def __str__(self) -> str:
        return f"{self.user.username} - Session {self.session_token[:8]}"  # type: ignore[attr-defined]


class LevelProgress(models.Model):
    """
    Tracks progress for each level in a game session
    """
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='level_progress')
    level_number = models.IntegerField()
    
    # Level details
    question_category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    points_earned = models.IntegerField(default=0)
    bonus_points = models.IntegerField(default=0)
    
    # Attempt tracking
    riddle_attempts = models.IntegerField(default=0)
    security_attempts = models.IntegerField(default=0)
    hint_used = models.BooleanField(default=False)
    security_hint_used = models.BooleanField(default=False)
    
    # Completion status
    riddle_solved = models.BooleanField(default=False)
    level_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.FloatField(default=0)  # in seconds
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'level_progress'
        unique_together = ['session', 'level_number']
        ordering = ['level_number']
    
    def __str__(self):
        return f"Level {self.level_number} - {self.session.user.username}"


class Achievement(models.Model):
    """
    Achievements that players can unlock
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=10)
    points = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'achievements'
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class UserAchievement(models.Model):
    """
    Tracks which achievements each user has unlocked
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(GameSession, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'user_achievements'
        unique_together = ['user', 'achievement']
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class Leaderboard(models.Model):
    """
    Leaderboard entries for tracking top players
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    
    final_score = models.IntegerField()
    total_time = models.FloatField()  # in seconds
    completion_date = models.DateTimeField(auto_now_add=True)
    
    rank_achieved = models.CharField(max_length=100)
    accuracy = models.FloatField()  # percentage
    speed_score = models.FloatField()  # percentage
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['-final_score', 'total_time']
    
    def __str__(self):
        return f"{self.user.username} - Score: {self.final_score}"


class Question(models.Model):
    """
    Permanent storage for game questions/riddles
    Only editable by administrators
    """
    level_number = models.IntegerField(unique=True, help_text="Level number (0-indexed)")
    question = models.TextField(help_text="The riddle text")
    answer = models.CharField(max_length=255, help_text="Correct answer (case-insensitive)")
    security_riddle = models.TextField(help_text="Phase 2 security question")
    security_key = models.CharField(max_length=255, help_text="Phase 2 correct answer")
    hint = models.TextField(help_text="Hint for main riddle")
    security_hint = models.TextField(help_text="Hint for security question")
    category = models.CharField(max_length=100, help_text="Question category")
    difficulty = models.CharField(
        max_length=20,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='medium'
    )
    points = models.IntegerField(default=10, help_text="Base points for this question")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Whether this question is active")
    
    class Meta:
        db_table = 'questions'
        ordering = ['level_number']
    
    def __str__(self):
        return f"Level {self.level_number + 1}: {self.category} ({self.difficulty})"

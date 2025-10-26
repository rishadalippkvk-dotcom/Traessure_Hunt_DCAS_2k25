"""
URL Configuration for Authentication API
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.get_user_profile, name='profile'),
    
    # Game Sessions
    path('game/start/', views.create_game_session, name='start_game'),
    path('game/session/', views.get_active_session, name='active_session'),
    path('game/session/<int:session_id>/', views.update_game_session, name='update_session'),
    path('game/session/<int:session_id>/progress/', views.get_session_progress, name='session_progress'),
    path('game/session/<int:session_id>/progress/clear/', views.clear_session_progress, name='clear_session_progress'),
    
    # Level Progress
    path('game/level/', views.save_level_progress, name='save_level'),
    path('game/progress/all/', views.get_all_level_progress, name='all_level_progress'),
    
    # Leaderboard
    path('leaderboard/', views.get_leaderboard, name='leaderboard'),
    path('leaderboard/submit/', views.submit_to_leaderboard, name='submit_leaderboard'),
    
    # Achievements
    path('achievements/', views.get_user_achievements, name='user_achievements'),
    path('achievements/all/', views.list_all_achievements, name='all_achievements'),
    
    # Questions
    path('questions/', views.get_all_questions, name='all_questions'),
    path('questions/<int:level_number>/', views.get_question_by_level, name='question_by_level'),
    path('questions/create/', views.create_question, name='create_question'),
    path('questions/<int:level_number>/update/', views.update_question, name='update_question'),
    path('questions/<int:level_number>/delete/', views.delete_question, name='delete_question'),
    
    # Game Completion
    path('game/mark_completed/', views.mark_game_completed_permanently, name='mark_game_completed'),
]
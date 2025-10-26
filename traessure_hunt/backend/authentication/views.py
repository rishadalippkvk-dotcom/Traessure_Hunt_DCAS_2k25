"""
REST API Views for Treasure Hunt Authentication & Game Management
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.utils import timezone
from django.db.models import Q
import secrets

from .models import User, GameSession, LevelProgress, Achievement, UserAchievement, Leaderboard, Question
from .serializers import (
    UserSerializer, UserRegistrationSerializer, LoginSerializer,
    GameSessionSerializer, LevelProgressSerializer, AchievementSerializer,
    UserAchievementSerializer, LeaderboardSerializer, QuestionSerializer
)


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user
    POST /api/auth/register/
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'message': 'Registration successful',
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user and return authentication token
    POST /api/auth/login/
    Body: {"username": "...", "password": "..."}
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        
        # Update last login
        user.last_login_at = timezone.now()
        user.save()
        
        return Response({
            'success': True,
            'message': f'Welcome, {user.username}!',
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Invalid credentials',
        'errors': serializer.errors
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout user and delete token
    POST /api/auth/logout/
    """
    try:
        request.user.auth_token.delete()
        return Response({
            'success': True,
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get current user profile
    GET /api/auth/profile/
    """
    serializer = UserSerializer(request.user)
    return Response({
        'success': True,
        'user': serializer.data
    })


# ═══════════════════════════════════════════════════════════════════════════════
# GAME SESSION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_game_session(request):
    """
    Create a new game session for the user
    POST /api/auth/game/start/
    """
    # Deactivate any existing active sessions
    GameSession.objects.filter(user=request.user, is_active=True).update(is_active=False)
    
    # Create new session
    session = GameSession.objects.create(
        user=request.user,
        session_token=secrets.token_urlsafe(32)
    )
    
    return Response({
        'success': True,
        'message': 'Game session created',
        'session': GameSessionSerializer(session).data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_session(request):
    """
    Get user's active game session
    GET /api/auth/game/session/
    """
    try:
        session = GameSession.objects.get(user=request.user, is_active=True)
        return Response({
            'success': True,
            'session': GameSessionSerializer(session).data
        })
    except GameSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'No active session found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_game_session(request, session_id):
    """
    Update game session progress
    PUT /api/auth/game/session/<id>/
    """
    try:
        session = GameSession.objects.get(id=session_id, user=request.user)
        serializer = GameSessionSerializer(session, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # If game is finished, update user stats
            if request.data.get('finished'):
                session.completed_at = timezone.now()
                session.save()
                
                user = request.user
                user.total_score += session.score
                user.games_played += 1
                user.best_streak = max(user.best_streak, session.max_streak)
                user.save()
            
            return Response({
                'success': True,
                'session': serializer.data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except GameSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL PROGRESS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_level_progress(request):
    """
    Save progress for a specific level
    POST /api/auth/game/level/
    """
    try:
        # Get the active session for the user
        session = GameSession.objects.get(user=request.user, is_active=True)
        
        # Get the current question data
        level_number = request.data.get('level', 0)
        if level_number > 0:  # Adjust for 0-based indexing
            level_number -= 1
        
        # Get question details if available
        questions = Question.objects.filter(level_number=level_number, is_active=True)
        question = questions.first() if questions.exists() else None
        
        # Create or update level progress
        level_progress_data = {
            'session': session.id,
            'level_number': level_number,
            'question_category': question.category if question else 'Unknown',
            'difficulty': question.difficulty if question else 'medium',
            'points_earned': request.data.get('score', 0),
            'bonus_points': 0,  # Calculate based on streak/combo if needed
            'riddle_attempts': request.data.get('wrong_attempts', 0),
            'security_attempts': request.data.get('security_wrong_attempts', 0),
            'hint_used': request.data.get('hints_used', 0) > 0,
            'security_hint_used': False,  # Track this separately if needed
            'riddle_solved': True,  # Since we're saving after level completion
            'level_completed': True,
            'completed_at': timezone.now(),
            'time_spent': 0  # Calculate if needed
        }
        
        # Check if level progress already exists
        try:
            existing_progress = LevelProgress.objects.get(
                session=session, 
                level_number=level_number
            )
            # Update existing progress
            for key, value in level_progress_data.items():
                setattr(existing_progress, key, value)
            existing_progress.save()
            level_progress = existing_progress
        except LevelProgress.DoesNotExist:
            # Create new progress
            serializer = LevelProgressSerializer(data=level_progress_data)
            if serializer.is_valid():
                level_progress = serializer.save()
            else:
                return Response({
                    'success': False,
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True,
            'level_progress': LevelProgressSerializer(level_progress).data
        }, status=status.HTTP_201_CREATED)
        
    except GameSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'No active game session found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_session_progress(request, session_id):
    """
    Get all level progress for a session
    GET /api/auth/game/session/<id>/progress/
    """
    levels = LevelProgress.objects.filter(session_id=session_id, session__user=request.user)
    serializer = LevelProgressSerializer(levels, many=True)
    
    return Response({
        'success': True,
        'progress': serializer.data
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_session_progress(request, session_id):
    """
    Clear all level progress for a session
    DELETE /api/auth/game/session/<id>/progress/
    """
    try:
        # Verify session belongs to user
        session = GameSession.objects.get(id=session_id, user=request.user)
        # Delete all level progress for this session
        LevelProgress.objects.filter(session=session).delete()
        
        return Response({
            'success': True,
            'message': 'Progress cleared successfully'
        })
        
    except GameSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_level_progress(request):
    """
    Get all level progress for admin dashboard
    GET /api/auth/game/progress/all/
    """
    # Only admins can access this
    if not request.user.is_staff:
        return Response({
            'success': False,
            'message': 'Admin access required'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Get all level progress data
    all_progress = LevelProgress.objects.select_related('session__user').all()
    serializer = LevelProgressSerializer(all_progress, many=True)
    
    return Response({
        'success': True,
        'progress': serializer.data
    })


# ═══════════════════════════════════════════════════════════════════════════════
# LEADERBOARD ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['GET'])
@permission_classes([AllowAny])
def get_leaderboard(request):
    """
    Get top players leaderboard
    GET /api/auth/leaderboard/?limit=10
    """
    limit = int(request.GET.get('limit', 10))
    leaderboard = Leaderboard.objects.all()[:limit]
    serializer = LeaderboardSerializer(leaderboard, many=True)
    
    return Response({
        'success': True,
        'leaderboard': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_to_leaderboard(request):
    """
    Submit completed game to leaderboard
    POST /api/auth/leaderboard/
    """
    try:
        session_id = request.data.get('session_id')
        session = GameSession.objects.get(id=session_id, user=request.user, finished=True)
        
        # Create leaderboard entry
        leaderboard_entry = Leaderboard.objects.create(
            user=request.user,
            session=session,
            final_score=session.score,
            total_time=(session.completed_at - session.started_at).total_seconds(),
            rank_achieved=request.data.get('rank_achieved', ''),
            accuracy=request.data.get('accuracy', 0),
            speed_score=request.data.get('speed_score', 0)
        )
        
        return Response({
            'success': True,
            'message': 'Score submitted to leaderboard',
            'entry': LeaderboardSerializer(leaderboard_entry).data
        }, status=status.HTTP_201_CREATED)
        
    except GameSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found or not finished'
        }, status=status.HTTP_404_NOT_FOUND)


# ═══════════════════════════════════════════════════════════════════════════════
# ACHIEVEMENTS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_achievements(request):
    """
    Get all achievements unlocked by user
    GET /api/auth/achievements/
    """
    achievements = UserAchievement.objects.filter(user=request.user)
    serializer = UserAchievementSerializer(achievements, many=True)
    
    return Response({
        'success': True,
        'achievements': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def list_all_achievements(request):
    """
    List all available achievements
    GET /api/auth/achievements/all/
    """
    achievements = Achievement.objects.all()
    serializer = AchievementSerializer(achievements, many=True)
    
    return Response({
        'success': True,
        'achievements': serializer.data
    })


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTIONS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_questions(request):
    """
    Get all active questions
    GET /api/auth/questions/
    """
    questions = Question.objects.filter(is_active=True).order_by('level_number')
    serializer = QuestionSerializer(questions, many=True)
    
    return Response({
        'success': True,
        'count': questions.count(),
        'questions': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_question_by_level(request, level_number):
    """
    Get a specific question by level number
    GET /api/auth/questions/<level_number>/
    """
    try:
        question = Question.objects.get(level_number=level_number, is_active=True)
        serializer = QuestionSerializer(question)
        
        return Response({
            'success': True,
            'question': serializer.data
        })
    except Question.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Question for level {level_number} not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    """
    Create a new question (admin only)
    POST /api/auth/questions/create/
    """
    # Check if user is admin
    if not request.user.is_staff:
        return Response({
            'success': False,
            'message': 'Admin access required'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Question created successfully',
            'question': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_question(request, level_number):
    """
    Update a question by level number (admin only)
    PUT /api/auth/questions/<level_number>/update/
    """
    # Check if user is admin
    if not request.user.is_staff:
        return Response({
            'success': False,
            'message': 'Admin access required'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        question = Question.objects.get(level_number=level_number)
        # Pass is_update=True to the serializer
        serializer = QuestionSerializer(question, data=request.data, partial=False, context={'request': request, 'is_update': True})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Question updated successfully',
                'question': serializer.data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Question.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Question for level {level_number} not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_question(request, level_number):
    """
    Delete a question by level number (admin only)
    DELETE /api/auth/questions/<level_number>/delete/
    """
    # Check if user is admin
    if not request.user.is_staff:
        return Response({
            'success': False,
            'message': 'Admin access required'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        question = Question.objects.get(level_number=level_number)
        question.delete()
        return Response({
            'success': True,
            'message': f'Question for level {level_number} deleted successfully'
        })
    except Question.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Question for level {level_number} not found'
        }, status=status.HTTP_404_NOT_FOUND)

# ═══════════════════════════════════════════════════════════════════════════════
# GAME COMPLETION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_game_completed_permanently(request):
    """
    Mark game as completed permanently to prevent replay
    POST /api/auth/game/mark_completed/
    """
    try:
        session = GameSession.objects.get(user=request.user, is_active=True)
        session.game_completed_permanently = True
        session.finished = True
        session.completed_at = timezone.now()
        session.save()
        
        # Update user stats
        user = request.user
        user.total_score += session.score
        user.games_played += 1
        user.best_streak = max(user.best_streak, session.max_streak)
        user.save()
        
        return Response({
            'success': True,
            'message': 'Game marked as completed permanently'
        })
        
    except GameSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'No active session found'
        }, status=status.HTTP_404_NOT_FOUND)

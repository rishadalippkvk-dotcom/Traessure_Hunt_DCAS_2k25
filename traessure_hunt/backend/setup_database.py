"""
Database Setup Script for FOSS Treasure Hunt Backend
Run this script to initialize the database with default data
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'treasure_hunt_backend.settings')
django.setup()

from authentication.models import Achievement


def create_default_achievements():
    """Create default achievements"""
    achievements_data = [
        {
            'name': 'First Steps',
            'description': 'Complete your first level',
            'icon': '🎓',
            'points': 5
        },
        {
            'name': 'FOSS Graduate',
            'description': 'Complete all 6 levels',
            'icon': '🎓',
            'points': 20
        },
        {
            'name': 'Security Expert',
            'description': 'Crack all security keys',
            'icon': '🔐',
            'points': 15
        },
        {
            'name': 'Speed Runner',
            'description': 'Complete the game in under 10 minutes',
            'icon': '⚡',
            'points': 25
        },
        {
            'name': 'Perfect Solver',
            'description': 'Complete a level without hints or wrong answers',
            'icon': '💎',
            'points': 10
        },
        {
            'name': 'Streak Master',
            'description': 'Achieve a 5-level streak',
            'icon': '🔥',
            'points': 15
        },
        {
            'name': 'Unstoppable',
            'description': 'Achieve a 6-level perfect streak',
            'icon': '⭐',
            'points': 30
        },
        {
            'name': 'FOSS Grandmaster',
            'description': 'Complete the game with perfect score and no hints',
            'icon': '🏆',
            'points': 50
        },
    ]
    
    created_count = 0
    for achievement_data in achievements_data:
        achievement, created = Achievement.objects.get_or_create(
            name=achievement_data['name'],
            defaults=achievement_data
        )
        if created:
            created_count += 1
            print(f"✓ Created achievement: {achievement.icon} {achievement.name}")
        else:
            print(f"- Achievement already exists: {achievement.icon} {achievement.name}")
    
    print(f"\n{created_count} new achievements created!")
    print(f"Total achievements: {Achievement.objects.count()}")


def main():
    print("=" * 70)
    print("FOSS Treasure Hunt - Database Setup")
    print("=" * 70)
    print()
    
    print("Setting up default achievements...")
    create_default_achievements()
    
    print()
    print("=" * 70)
    print("Database setup complete! 🎉")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Run: python manage.py createsuperuser")
    print("2. Run: python manage.py runserver")
    print("3. Access admin at: http://localhost:8000/admin/")
    print()


if __name__ == '__main__':
    main()

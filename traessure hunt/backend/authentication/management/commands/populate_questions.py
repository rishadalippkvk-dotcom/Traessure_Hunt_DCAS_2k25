"""
Django Management Command to Populate Initial Questions
Run with: python manage.py populate_questions
"""
from django.core.management.base import BaseCommand
from authentication.models import Question


class Command(BaseCommand):
    help = 'Populate the database with initial game questions'

    def handle(self, *args, **kwargs):
        # Define initial questions (from final2.py QUESTIONS list)
        questions_data = [
            {
                "level_number": 0,
                "question": "🔍 The Hidden Core\n\nI am invisible but control it all,\nCPU, memory, devices—I stand tall.\nWithout me, Linux would never run,\nFind my name, and Level 2 is begun.",
                "answer": "kernel",
                "security_riddle": "What 3-letter command shows you where you are in the Linux filesystem?",
                "security_key": "pwd",
                "hint": "💡 Think of the 'heart' of the operating system that manages hardware.",
                "security_hint": "💡 Stands for 'Print Working Directory'.",
                "category": "OS Architecture",
                "difficulty": "easy",
                "points": 10
            },
            {
                "level_number": 1,
                "question": "🔍 The Command Interpreter\n\nI'm not food, but I'm called a shell,\nWithout me, using the kernel is hell.\nI take your commands, one by one,\nBash, Zsh, Fish—I'm the one!",
                "answer": "shell",
                "security_riddle": "What license ensures software remains free and open source? (3 letters, created by FSF)",
                "security_key": "gpl",
                "hint": "💡 The interface between users and the kernel. Famous types include Bash and Zsh.",
                "security_hint": "💡 GNU _____ License. Richard Stallman's creation.",
                "category": "System Components",
                "difficulty": "medium",
                "points": 15
            },
            {
                "level_number": 2,
                "question": "🔍 The Ancient Ancestor\n\nBorn at Bell Labs in the 1970s,\nI shaped today's systems and realities.\nLinux is my child, that's true,\nFour letters, can you name me too?",
                "answer": "unix",
                "security_riddle": "Decode: 01101100 01101001 01101110 01110101 01111000",
                "security_key": "linux",
                "hint": "💡 The operating system that inspired Linux. Starts with 'U'.",
                "security_hint": "💡 Convert binary to ASCII. Each group is 8 bits = 1 character.",
                "category": "OS History",
                "difficulty": "hard",
                "points": 20
            },
            {
                "level_number": 3,
                "question": "🔍 The Software Manager\n\nI fetch, install, and update with ease,\napt, yum, pacman—examples of me.\nWithout me, your software is stranded,\nWhat's my name, two words demanded?",
                "answer": "package manager",
                "security_riddle": "What command changes your current directory in Linux? (2 letters)",
                "security_key": "cd",
                "hint": "💡 Two words. First word is 'Package'. Manages software installation.",
                "security_hint": "💡 'Change Directory' - one of the most basic Linux commands.",
                "category": "System Tools",
                "difficulty": "medium",
                "points": 15
            },
            {
                "level_number": 4,
                "question": "🔍 The Permission Master\n\nI control who can read, write, execute,\nThree groups of three—that's my tribute.\nOwner, group, others—I set the law,\nWhat am I called? Answer with awe.",
                "answer": "chmod",
                "security_riddle": "What famous OS did Linus Torvalds create? (5 letters)",
                "security_key": "linux",
                "hint": "💡 A Linux command to change file permissions. Starts with 'ch'.",
                "security_hint": "💡 The creator's first name is Linus. OS released in 1991.",
                "category": "File System",
                "difficulty": "medium",
                "points": 15
            },
            {
                "level_number": 5,
                "question": "🔍 The Final Treasure\n\nI wrote the kernel back in '91,\nFor fun at first, but now it runs everyone.\nA Finnish programmer, still maintaining today,\nWho am I—can you say?",
                "answer": "linus torvalds",
                "security_riddle": "What 3-letter open source version control system did Linus also create?",
                "security_key": "git",
                "hint": "💡 His first name is Linus. Created Linux as a student project.",
                "security_hint": "💡 Rhymes with 'sit'. Used for tracking code changes.",
                "category": "Linux History",
                "difficulty": "hard",
                "points": 20
            }
        ]

        self.stdout.write(self.style.WARNING('Clearing existing questions...'))
        Question.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Populating questions...'))
        created_count = 0
        
        for q_data in questions_data:
            question, created = Question.objects.get_or_create(
                level_number=q_data['level_number'],
                defaults=q_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created Level {q_data["level_number"] + 1}: {q_data["category"]}'
                    )
                )
            else:
                # Update existing question
                for key, value in q_data.items():
                    setattr(question, key, value)
                question.save()
                self.stdout.write(
                    self.style.WARNING(
                        f'⟳ Updated Level {q_data["level_number"] + 1}: {q_data["category"]}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully populated {len(questions_data)} questions!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'   Created: {created_count} | Updated: {len(questions_data) - created_count}'
            )
        )

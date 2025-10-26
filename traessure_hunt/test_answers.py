import toml
import os

# Test that we can load the answers from the TOML file
try:
    # Use absolute path to ensure file is found in all environments
    answers_file_path = os.path.join(os.path.dirname(__file__), "answers.toml")
    answers_data = toml.load(answers_file_path)
    answers = answers_data["questions"]
    
    print("Answers loaded successfully from TOML file:")
    for key, value in answers.items():
        print(f"{key}: {value}")
        
    # Test specific answers
    print("\nTesting specific answers:")
    print(f"Level 1 answer: {answers['level_1_answer']}")
    print(f"Level 1 security key: {answers['level_1_security_key']}")
    
except Exception as e:
    print(f"Error loading answers: {e}")
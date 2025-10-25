import toml

# Test that we can load the answers from the TOML file
try:
    answers_data = toml.load("answers.toml")
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
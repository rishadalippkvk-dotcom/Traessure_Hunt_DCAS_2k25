# FOSS Treasure Hunt - Answer Security Implementation

## Overview
This document describes the implementation of answer security for the FOSS Treasure Hunt game by moving the answers to a separate TOML file.

## Changes Made

### 1. Created answers.toml file
- Created a new file `answers.toml` to store all game answers separately
- Contains both main answers and security keys for all 6 levels
- Structure:
  ```
  [questions]
  level_1_answer = "kernel"
  level_1_security_key = "pwd"
  # ... and so on for all levels
  ```

### 2. Updated requirements.txt
- Added `toml==0.10.2` dependency to support TOML file parsing

### 3. Modified final2.py
- Added `import toml` to enable TOML file parsing
- Modified the QUESTIONS data structure to load answers from the TOML file instead of hardcoding them
- Implemented dynamic loading of answers at runtime

## Security Benefits
- Answers are no longer visible in the main source code
- Easier to update answers without modifying the main application code
- Separation of data and logic improves maintainability
- Reduces risk of accidental exposure of answers in version control

## Implementation Details
The implementation loads the TOML file at application startup and dynamically populates the QUESTIONS data structure with the answers from the file. This ensures that the game functionality remains exactly the same while improving security.

## Testing
The implementation has been tested and verified to work correctly:
- TOML file loads successfully
- Answers are correctly mapped to their respective levels
- Game functions as expected with the new implementation
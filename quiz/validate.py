#!/usr/bin/env python3
"""
Simple validation script for Quiz Master Application.
Tests core components without GUI.
"""

print("Quiz Master Application Validator")
print("=" * 40)

# Test 1: Check Python version
import sys
print(f"Python Version: {sys.version}")
if sys.version_info < (3, 7):
    print("❌ Python 3.7+ required")
    sys.exit(1)
else:
    print("✅ Python version OK")

# Test 2: Check standard library imports
try:
    import tkinter
    import sqlite3
    import threading
    import json
    import csv
    import time
    print("✅ All standard library modules available")
except ImportError as e:
    print(f"❌ Missing standard library module: {e}")
    sys.exit(1)

# Test 3: Check application modules
try:
    from database import DatabaseManager
    from quiz_logic import QuizManager, QuizSession
    from ui_manager import QuizMasterUI
    print("✅ All application modules imported successfully")
except ImportError as e:
    print(f"❌ Application module import error: {e}")
    sys.exit(1)

# Test 4: Test database functionality
print("\nTesting database functionality...")
try:
    db = DatabaseManager("validation_test.db")
    questions = db.get_questions(3)
    print(f"✅ Database created with {len(questions)} sample questions")
    
    # Test score addition
    score_id = db.add_score("Validator", 3, 3, 60)
    print(f"✅ Score added successfully (ID: {score_id})")
    
    # Test leaderboard
    leaderboard = db.get_leaderboard(1)
    print(f"✅ Leaderboard retrieved with {len(leaderboard)} entries")
    
    db.close()
    
    # Clean up test database
    import os
    if os.path.exists("validation_test.db"):
        os.remove("validation_test.db")
        
except Exception as e:
    print(f"❌ Database test failed: {e}")

# Test 5: Test quiz logic
print("\nTesting quiz logic...")
try:
    sample_questions = [
        {
            'id': 1,
            'question': 'What is 2+2?',
            'options': ['3', '4', '5', '6'],
            'correct_answer': 'B',
            'difficulty': 'easy',
            'category': 'math'
        }
    ]
    
    session = QuizSession(sample_questions, 30)
    session.start_quiz()
    
    current_q = session.get_current_question()
    if current_q and current_q['question']:
        print("✅ Quiz session created and question retrieved")
    
    # Test answer submission
    result = session.submit_answer('B')
    if result['is_correct']:
        print("✅ Answer submission working correctly")
    
except Exception as e:
    print(f"❌ Quiz logic test failed: {e}")

print("\n" + "=" * 40)
print("Validation Complete!")
print("\nIf all tests passed, you can run the full application with:")
print("python main.py")
print("\nFeatures included:")
print("• Interactive GUI with Tkinter")
print("• SQLite database for questions and scores")  
print("• Real-time timer with auto-submit")
print("• Multiple difficulty levels")
print("• Leaderboard system")
print("• Results export functionality")
print("• Comprehensive error handling")
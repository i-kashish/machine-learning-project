#!/usr/bin/env python3
"""
Test script for Quiz Master Application
Tests core functionality without GUI.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database():
    """Test database functionality."""
    print("Testing Database Manager...")
    
    try:
        from database import DatabaseManager
        
        # Create test database
        db = DatabaseManager("test_quiz_master.db")
        
        # Test getting questions
        questions = db.get_questions(5)
        print(f"✓ Retrieved {len(questions)} questions")
        
        # Test adding a score
        score_id = db.add_score("Test Player", 8, 10, 120)
        print(f"✓ Added test score with ID: {score_id}")
        
        # Test leaderboard
        leaderboard = db.get_leaderboard(5)
        print(f"✓ Retrieved leaderboard with {len(leaderboard)} entries")
        
        # Cleanup
        db.close()
        if os.path.exists("test_quiz_master.db"):
            os.remove("test_quiz_master.db")
            
        print("✓ Database tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_quiz_logic():
    """Test quiz logic functionality."""
    print("\nTesting Quiz Logic...")
    
    try:
        from quiz_logic import QuizSession, QuizManager
        
        # Create sample questions
        sample_questions = [
            {
                'id': 1,
                'question': 'Test question 1?',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'B',
                'difficulty': 'easy',
                'category': 'test'
            },
            {
                'id': 2,
                'question': 'Test question 2?',
                'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
                'correct_answer': 'C',
                'difficulty': 'medium',
                'category': 'test'
            }
        ]
        
        # Test quiz session
        session = QuizSession(sample_questions, 30)
        session.start_quiz()
        
        print(f"✓ Quiz session started")
        print(f"✓ Current question: {session.get_current_question()['question']}")
        print(f"✓ Progress: {session.get_progress()}")
        
        # Test answering
        result = session.submit_answer('B')
        print(f"✓ Answer submitted: {result['is_correct']}")
        
        # Test final results
        if session.current_question_index >= len(session.questions):
            results = session.get_final_results()
            print(f"✓ Final results: {results['score']}/{results['total_questions']}")
        
        print("✓ Quiz logic tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Quiz logic test failed: {e}")
        return False

def test_imports():
    """Test all imports work correctly."""
    print("\nTesting Imports...")
    
    try:
        import tkinter as tk
        print("✓ Tkinter imported successfully")
        
        from database import DatabaseManager
        print("✓ DatabaseManager imported successfully")
        
        from quiz_logic import QuizManager, QuizSession
        print("✓ Quiz logic modules imported successfully")
        
        from ui_manager import QuizMasterUI
        print("✓ UI Manager imported successfully")
        
        print("✓ All imports successful!")
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=== Quiz Master Application Tests ===\n")
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_imports():
        tests_passed += 1
        
    if test_database():
        tests_passed += 1
        
    if test_quiz_logic():
        tests_passed += 1
    
    # Summary
    print(f"\n=== Test Summary ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! The Quiz Master application should work correctly.")
        print("\nTo run the full application, execute: python main.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
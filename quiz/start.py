#!/usr/bin/env python3
"""
Quiz Master - Startup Script with Enhanced Error Handling
Provides user-friendly error messages and troubleshooting guidance.
"""

import sys
import os

def check_requirements():
    """Check system requirements and dependencies."""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ ERROR: Python 3.7 or higher is required.")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Check required modules
    required_modules = ['tkinter', 'sqlite3', 'threading', 'json', 'csv', 'time']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ ERROR: Missing required modules: {', '.join(missing_modules)}")
        print("   These are usually included with Python. Please reinstall Python.")
        return False
    
    print("✅ All required standard library modules available")
    
    # Check application files
    required_files = ['main.py', 'database.py', 'quiz_logic.py', 'ui_manager.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ ERROR: Missing application files: {', '.join(missing_files)}")
        print("   Please ensure all files are in the same directory.")
        return False
    
    print("✅ All application files present")
    
    # Test imports
    try:
        from database import DatabaseManager
        from quiz_logic import QuizManager
        from ui_manager import QuizMasterUI
        print("✅ Application modules loaded successfully")
    except ImportError as e:
        print(f"❌ ERROR: Failed to import application modules: {e}")
        print("   Please check that all Python files are in the same directory.")
        return False
    
    return True

def create_shortcut_info():
    """Create information about keyboard shortcuts."""
    shortcuts_info = """
🎯 QUIZ MASTER - KEYBOARD SHORTCUTS 🎯

During Quiz:
• 1, 2, 3, 4    - Select answer options A, B, C, D
• Enter         - Submit selected answer
• Escape        - Skip current question

Navigation:
• Tab           - Move between interface elements
• Space         - Activate buttons
• Alt+F4        - Close application

Tips:
• Watch the timer! It changes color as time runs low
• Green = Safe, Orange = Warning, Red = Danger
• Questions and options are shuffled each game
• Your best scores are saved to the leaderboard

Difficulty Levels:
• Easy: 8 questions, 45 seconds each
• Medium: 10 questions, 30 seconds each  
• Hard: 12 questions, 20 seconds each

Good luck! 🍀
"""
    
    try:
        with open("SHORTCUTS.txt", "w", encoding="utf-8") as f:
            f.write(shortcuts_info)
        print("📝 Created SHORTCUTS.txt with keyboard shortcuts")
    except:
        pass  # Not critical if this fails

def main():
    """Main startup function."""
    print("🎯 QUIZ MASTER - INTERACTIVE QUIZ APPLICATION")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Startup failed due to requirements not being met.")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Ensure Python 3.7+ is installed")
        print("2. Verify all application files are present")
        print("3. Check that Tkinter is available (usually included with Python)")
        print("4. Try running: python -m tkinter (should open a small window)")
        input("\nPress Enter to exit...")
        return False
    
    # Create additional resources
    create_shortcut_info()
    
    print("\n🚀 Starting Quiz Master Application...")
    print("   If a window doesn't appear, check for error messages below.")
    
    try:
        # Import and run the application
        from main import QuizMaster
        
        # Create and run application
        app = QuizMaster()
        print("✅ Application window should now be visible!")
        print("   Close this console window if everything looks good.")
        
        # Start the application
        app.run()
        
    except KeyboardInterrupt:
        print("\n⚠️  Application interrupted by user (Ctrl+C)")
        return True
        
    except Exception as e:
        print(f"\n❌ RUNTIME ERROR: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Close any other instances of the application")
        print("2. Restart your computer if problems persist")
        print("3. Check that no antivirus is blocking the application")
        print("4. Try running as administrator (right-click -> Run as administrator)")
        
        # Detailed error for debugging
        import traceback
        print(f"\nDetailed error information:")
        print("-" * 30)
        traceback.print_exc()
        print("-" * 30)
        
        input("\nPress Enter to exit...")
        return False
    
    print("\n✅ Quiz Master application closed successfully.")
    return True

if __name__ == "__main__":
    try:
        success = main()
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        print("Please report this error if the application should work on your system.")
        input("Press Enter to exit...")
    
    # Cleanup any temporary files
    cleanup_files = ["validation_test.db", "test_quiz.db"]
    for file in cleanup_files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except:
            pass
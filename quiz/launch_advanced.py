#!/usr/bin/env python3
"""
Advanced Quiz Master Launcher
Enhanced launcher for the advanced Quiz Master application with comprehensive features.

Author: Qoder AI Assistant
Date: 2025-08-26
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def show_features_overview():
    """Show an overview of the advanced features."""
    features_text = """
🎯 QUIZ MASTER PRO - ADVANCED FEATURES 🎯

🌟 NEW ADVANCED FEATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 MULTI-LANGUAGE SUPPORT:
  • Questions in English, Spanish, French, German, Japanese & Chinese
  • Automatic language detection and localization
  • Mixed-language quizzes available

📚 COMPREHENSIVE SUBJECT COVERAGE:
  • Mathematics: Algebra, Calculus, Statistics, Geometry
  • Science: Physics, Chemistry, Biology, Earth Science, Astronomy
  • Technology: Programming, AI, Databases, Algorithms
  • Humanities: History, Literature, Philosophy, Languages
  • Arts: Music, Visual Arts, Architecture, Performing Arts
  • Social Sciences: Psychology, Economics, Law, Sociology
  • Health Sciences: Medicine, Anatomy, Public Health

🎮 ADVANCED GAMEPLAY:
  • Weighted scoring system (different points per question)
  • Speed bonuses for quick correct answers
  • Achievement system with unlockable badges
  • Performance ratings based on accuracy and speed
  • Custom difficulty levels (Easy, Medium, Hard, Expert)

🏆 ENHANCED SCORING & ACHIEVEMENTS:
  • Perfect Score Master
  • Speed Demon (fast answers)
  • Hot Streak (consecutive correct answers)
  • Quiz Master (90%+ accuracy)
  • Scholar (80%+ accuracy)
  • Lightning Fast (sub-5-second answers)

📝 QUESTION MANAGEMENT SYSTEM:
  • Add custom questions with multi-language support
  • Import/Export questions (JSON, CSV, Text)
  • Edit existing questions through GUI
  • Batch operations for database management
  • Real-time question statistics and analytics

📊 ADVANCED ANALYTICS:
  • Detailed performance tracking
  • Category-wise score analysis
  • Time efficiency metrics
  • Progress history and trends
  • Leaderboard with filtering options

⚙️ CUSTOMIZATION OPTIONS:
  • Custom number of questions (5-50)
  • Adjustable time limits (10-120 seconds)
  • Category and subject filtering
  • Language preference selection
  • Difficulty mixing and matching

🎨 ENHANCED USER INTERFACE:
  • Modern, responsive design
  • Color-coded difficulty indicators
  • Real-time progress tracking
  • Achievement notifications
  • Keyboard shortcuts support

Ready to experience the ultimate quiz challenge? 🚀
"""
    
    # Create features window
    features_window = tk.Tk()
    features_window.title("Quiz Master Pro - Features Overview")
    features_window.geometry("700x600")
    features_window.resizable(True, True)
    
    # Create scrollable text widget
    from tkinter import scrolledtext
    text_widget = scrolledtext.ScrolledText(
        features_window, 
        wrap=tk.WORD, 
        font=("Courier", 10),
        padx=10,
        pady=10
    )
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Insert features text
    text_widget.insert(tk.END, features_text)
    text_widget.config(state=tk.DISABLED)  # Make read-only
    
    # Add launch button
    button_frame = tk.Frame(features_window)
    button_frame.pack(pady=10)
    
    def launch_app():
        features_window.destroy()
        launch_quiz_master()
    
    tk.Button(
        button_frame,
        text="🚀 Launch Quiz Master Pro",
        command=launch_app,
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10
    ).pack(side=tk.LEFT, padx=10)
    
    tk.Button(
        button_frame,
        text="❌ Exit",
        command=features_window.destroy,
        font=("Arial", 12),
        padx=20,
        pady=10
    ).pack(side=tk.LEFT, padx=10)
    
    # Center the window
    features_window.update_idletasks()
    x = (features_window.winfo_screenwidth() // 2) - (features_window.winfo_width() // 2)
    y = (features_window.winfo_screenheight() // 2) - (features_window.winfo_height() // 2)
    features_window.geometry(f"+{x}+{y}")
    
    features_window.mainloop()

def check_advanced_requirements():
    """Check if all advanced components are available."""
    print("🔍 Checking Advanced Quiz Master Requirements...")
    
    missing_files = []
    required_files = [
        'main.py',
        'database.py', 
        'quiz_logic.py',
        'ui_manager.py',
        'question_manager.py',
        'advanced_questions.json'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    # Test imports
    try:
        from database import DatabaseManager
        from quiz_logic import QuizManager
        from ui_manager import QuizMasterUI
        from question_manager import QuestionManagerUI
        print("✅ All advanced components loaded successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def setup_advanced_database():
    """Set up the advanced database with sample questions."""
    try:
        from database import DatabaseManager
        
        print("🗄️ Setting up advanced database...")
        db = DatabaseManager()
        
        # Check if advanced questions are loaded
        questions = db.get_questions(limit=5, shuffle=False)
        if len(questions) >= 5:
            print(f"✅ Database ready with {len(questions)} questions")
            
            # Show question statistics
            stats = db.get_question_stats()
            print(f"📊 Questions by difficulty: {stats.get('by_difficulty', {})}")
            print(f"🏷️ Questions by category: {stats.get('by_category', {})}")
            print(f"🌐 Questions by language: {stats.get('by_language', {})}")
            
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def launch_quiz_master():
    """Launch the advanced Quiz Master application."""
    try:
        print("🚀 Launching Quiz Master Pro...")
        
        from main import QuizMaster
        app = QuizMaster()
        
        print("✅ Application started successfully!")
        print("📱 GUI window should now be visible")
        print("💡 Tip: Close this console if the GUI is working properly")
        
        app.run()
        
    except Exception as e:
        print(f"❌ Launch failed: {e}")
        messagebox.showerror("Launch Error", f"Failed to start application: {str(e)}")

def main():
    """Main launcher function."""
    print("=" * 60)
    print("🎯 QUIZ MASTER PRO - ADVANCED LAUNCHER")
    print("=" * 60)
    
    # Check requirements
    if not check_advanced_requirements():
        print("\n❌ Requirements check failed!")
        print("Please ensure all files are in the same directory.")
        input("Press Enter to exit...")
        return
    
    # Setup database
    if not setup_advanced_database():
        print("\n❌ Database setup failed!")
        input("Press Enter to exit...")
        return
    
    print("\n✅ All systems ready!")
    print("\nChoose how to start:")
    print("1. Show features overview first")
    print("2. Launch directly")
    print("3. Exit")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            show_features_overview()
        elif choice == "2":
            launch_quiz_master()
        elif choice == "3":
            print("👋 Goodbye!")
            return
        else:
            print("Invalid choice. Launching directly...")
            launch_quiz_master()
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
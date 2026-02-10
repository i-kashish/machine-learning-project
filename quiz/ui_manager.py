#!/usr/bin/env python3
"""
UI Manager for Quiz Master Application
Handles all Tkinter UI components and user interactions.

Author: Qoder AI Assistant
Date: 2025-08-26
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from typing import Optional, Dict, List
from quiz_logic import QuizManager, format_time


class QuizMasterUI:
    """
    Main UI manager class for Quiz Master application.
    Manages all screens and user interactions.
    """
    
    def __init__(self, root: tk.Tk, database_manager):
        """
        Initialize the UI manager.
        
        Args:
            root (tk.Tk): Main tkinter window
            database_manager: Database manager instance
        """
        self.root = root
        self.db_manager = database_manager
        self.quiz_manager = QuizManager(database_manager)
        
        # UI State variables
        self.current_frame = None
        self.timer_running = False
        self.timer_thread = None
        self.selected_answer = tk.StringVar()
        self.player_name = tk.StringVar()
        self.difficulty = tk.StringVar(value="medium")
        
        # Style configuration
        self.setup_styles()
        
        # Initialize main container
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Show welcome screen
        self.show_welcome_screen()
        
    def setup_styles(self):
        """Set up custom styles for ttk widgets."""
        style = ttk.Style()
        
        # Configure custom button styles
        style.configure("Large.TButton", font=("Arial", 12, "bold"), padding=10)
        style.configure("Option.TButton", font=("Arial", 11), padding=5)
        style.configure("Timer.TLabel", font=("Arial", 16, "bold"), foreground="red")
        style.configure("Question.TLabel", font=("Arial", 12), wraplength=600)
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        style.configure("Score.TLabel", font=("Arial", 14, "bold"))
        
    def clear_frame(self):
        """Clear the current frame."""
        if self.current_frame:
            self.current_frame.destroy()
            
    def show_welcome_screen(self):
        """Display the welcome screen with player name input and advanced quiz options."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.main_container)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            self.current_frame, 
            text="🎯 Welcome to Quiz Master Pro! 🎯", 
            style="Title.TLabel"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ttk.Label(
            self.current_frame,
            text="Advanced Multi-Language Quiz System with Comprehensive Subject Coverage!",
            font=("Arial", 11)
        )
        subtitle_label.pack(pady=5)
        
        # Main form frame
        form_frame = ttk.LabelFrame(self.current_frame, text="Advanced Quiz Setup", padding=20)
        form_frame.pack(pady=20, padx=30, fill=tk.X)
        
        # Player name input
        name_frame = tk.Frame(form_frame)
        name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(name_frame, text="Enter your name:", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        name_entry = ttk.Entry(name_frame, textvariable=self.player_name, font=("Arial", 11), width=25)
        name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        name_entry.focus()
        
        # Advanced options frame
        advanced_frame = ttk.LabelFrame(form_frame, text="Quiz Configuration", padding=15)
        advanced_frame.pack(fill=tk.X, pady=20)
        
        # Row 1: Difficulty and Language
        row1 = tk.Frame(advanced_frame)
        row1.pack(fill=tk.X, pady=5)
        
        # Difficulty selection
        ttk.Label(row1, text="Difficulty:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="medium")
        difficulty_combo = ttk.Combobox(
            row1, 
            textvariable=self.difficulty_var,
            values=["easy", "medium", "hard", "expert"],
            state="readonly",
            width=12
        )
        difficulty_combo.pack(side=tk.LEFT, padx=(5, 20))
        
        # Language selection
        ttk.Label(row1, text="Language:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.language_var = tk.StringVar(value="en")
        language_combo = ttk.Combobox(
            row1,
            textvariable=self.language_var,
            values=["en", "es", "fr", "de", "ja", "zh", "multi"],
            state="readonly",
            width=12
        )
        language_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Row 2: Category and Subject
        row2 = tk.Frame(advanced_frame)
        row2.pack(fill=tk.X, pady=5)
        
        # Category selection
        ttk.Label(row2, text="Category:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="all")
        try:
            available_categories = self.quiz_manager.get_available_categories()
            category_values = ["all"] + [cat['name'] for cat in available_categories]
        except:
            category_values = ["all", "science", "mathematics", "technology", "humanities", "arts"]
            
        category_combo = ttk.Combobox(
            row2,
            textvariable=self.category_var,
            values=category_values,
            state="readonly",
            width=12
        )
        category_combo.pack(side=tk.LEFT, padx=(5, 20))
        
        # Subject selection  
        ttk.Label(row2, text="Subject:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.subject_var = tk.StringVar(value="all")
        try:
            available_subjects = self.quiz_manager.get_available_subjects()
            subject_values = ["all"] + available_subjects
        except:
            subject_values = ["all", "physics", "chemistry", "biology", "calculus", "programming"]
            
        subject_combo = ttk.Combobox(
            row2,
            textvariable=self.subject_var,
            values=subject_values,
            state="readonly",
            width=12
        )
        subject_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Row 3: Custom settings
        row3 = tk.Frame(advanced_frame)
        row3.pack(fill=tk.X, pady=5)
        
        # Number of questions
        ttk.Label(row3, text="Questions:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.num_questions_var = tk.IntVar(value=10)
        questions_spin = tk.Spinbox(
            row3,
            from_=5,
            to=50,
            textvariable=self.num_questions_var,
            width=8
        )
        questions_spin.pack(side=tk.LEFT, padx=(5, 20))
        
        # Time per question
        ttk.Label(row3, text="Time/Question:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.time_per_question_var = tk.IntVar(value=30)
        time_spin = tk.Spinbox(
            row3,
            from_=10,
            to=120,
            textvariable=self.time_per_question_var,
            width=8
        )
        time_spin.pack(side=tk.LEFT, padx=(5, 0))
        ttk.Label(row3, text="seconds", font=("Arial", 9)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Statistics display
        stats_frame = ttk.LabelFrame(form_frame, text="Database Statistics", padding=10)
        stats_frame.pack(fill=tk.X, pady=15)
        
        try:
            question_stats = self.quiz_manager.get_question_statistics()
            total_questions = question_stats.get('total_questions', 0)
            by_difficulty = question_stats.get('by_difficulty', {})
            by_category = question_stats.get('by_category', {})
            
            stats_text = f"Available Questions: {total_questions} | "
            stats_text += f"Easy: {by_difficulty.get('easy', 0)} | "
            stats_text += f"Medium: {by_difficulty.get('medium', 0)} | "
            stats_text += f"Hard: {by_difficulty.get('hard', 0)}"
            
        except:
            stats_text = "Question statistics loading..."
            
        stats_label = ttk.Label(stats_frame, text=stats_text, font=("Arial", 9))
        stats_label.pack()
        
        # Buttons frame
        button_frame = tk.Frame(self.current_frame)
        button_frame.pack(pady=30)
        
        # Start Quiz button
        start_btn = ttk.Button(
            button_frame,
            text="🚀 Start Advanced Quiz",
            command=self.start_advanced_quiz,
            style="Large.TButton"
        )
        start_btn.pack(side=tk.LEFT, padx=10)
        
        # Question Manager button
        question_mgr_btn = ttk.Button(
            button_frame,
            text="📝 Question Manager",
            command=self.show_question_manager,
            style="Large.TButton"
        )
        question_mgr_btn.pack(side=tk.LEFT, padx=10)
        
        # Leaderboard button
        leaderboard_btn = ttk.Button(
            button_frame,
            text="🏆 View Leaderboard",
            command=self.show_leaderboard,
            style="Large.TButton"
        )
        leaderboard_btn.pack(side=tk.LEFT, padx=10)
        
        # Statistics button
        stats_btn = ttk.Button(
            button_frame,
            text="📊 Statistics",
            command=self.show_statistics,
            style="Large.TButton"
        )
        stats_btn.pack(side=tk.LEFT, padx=10)
        
        # Bind Enter key to start quiz
        self.root.bind('<Return>', lambda e: self.start_advanced_quiz())
        
    def start_advanced_quiz(self):
        """Start a new advanced quiz session with custom settings."""
        player_name = self.player_name.get().strip()
        
        if not player_name:
            messagebox.showerror("Error", "Please enter your name to start the quiz.")
            return
            
        if len(player_name) < 2:
            messagebox.showerror("Error", "Name must be at least 2 characters long.")
            return
            
        try:
            # Get advanced settings
            difficulty = self.difficulty_var.get()
            language = self.language_var.get()
            category = self.category_var.get() if self.category_var.get() != "all" else None
            subject = self.subject_var.get() if self.subject_var.get() != "all" else None
            num_questions = self.num_questions_var.get()
            time_per_question = self.time_per_question_var.get()
            
            # Create advanced quiz session
            self.quiz_session = self.quiz_manager.create_quiz(
                difficulty=difficulty,
                category=category,
                num_questions=num_questions,
                time_per_question=time_per_question,
                language=language,
                subject=subject
            )
            self.quiz_session.start_quiz()
            
            # Show quiz screen
            self.show_quiz_screen()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start quiz: {str(e)}")
            
    def show_question_manager(self):
        """Show the question management interface."""
        try:
            from question_manager import QuestionManagerUI
            
            qm = QuestionManagerUI(self.root, self.db_manager)
            qm.show_question_manager()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open question manager: {str(e)}")
        
    def start_quiz(self):
        """Start a new quiz session."""
        player_name = self.player_name.get().strip()
        
        if not player_name:
            messagebox.showerror("Error", "Please enter your name to start the quiz.")
            return
            
        if len(player_name) < 2:
            messagebox.showerror("Error", "Name must be at least 2 characters long.")
            return
            
        try:
            # Create quiz session
            self.quiz_session = self.quiz_manager.create_quiz(
                difficulty=self.difficulty.get()
            )
            self.quiz_session.start_quiz()
            
            # Show quiz screen
            self.show_quiz_screen()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start quiz: {str(e)}")
            
    def show_quiz_screen(self):
        """Display the main quiz interface."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.main_container)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top info frame
        info_frame = tk.Frame(self.current_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        # Player info
        player_info = ttk.Label(
            info_frame, 
            text=f"Player: {self.player_name.get()}", 
            font=("Arial", 11, "bold")
        )
        player_info.pack(side=tk.LEFT)
        
        # Timer (top right)
        self.timer_label = ttk.Label(
            info_frame, 
            text="30", 
            style="Timer.TLabel"
        )
        self.timer_label.pack(side=tk.RIGHT)
        
        # Progress frame
        progress_frame = tk.Frame(self.current_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        # Progress info
        progress = self.quiz_session.get_progress()
        progress_text = f"Question {progress['current']} of {progress['total']} | "
        progress_text += f"Score: {progress['score']} | "
        progress_text += f"Points: {progress['total_points']}/{progress['max_possible_points']}"
        
        if progress['achievements']:
            progress_text += f" | Achievements: {len(progress['achievements'])}"
            
        self.progress_label = ttk.Label(
            progress_frame,
            text=progress_text,
            font=("Arial", 11)
        )
        self.progress_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=200
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=10)
        self.progress_bar['value'] = progress['percentage']
        
        # Question frame
        question_frame = ttk.LabelFrame(self.current_frame, text="Question", padding=20)
        question_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Question text
        current_question = self.quiz_session.get_current_question()
        self.question_label = ttk.Label(
            question_frame,
            text=current_question['question'],
            style="Question.TLabel",
            justify=tk.LEFT
        )
        self.question_label.pack(pady=20)
        
        # Answer options frame
        self.options_frame = tk.Frame(question_frame)
        self.options_frame.pack(fill=tk.X, pady=20)
        
        self.selected_answer.set("")  # Clear previous selection
        
        # Create option buttons
        self.option_buttons = []
        for i, option in enumerate(current_question['options']):
            btn = ttk.Radiobutton(
                self.options_frame,
                text=f"{chr(65+i)}. {option}",
                variable=self.selected_answer,
                value=chr(65+i),
                style="TRadiobutton"
            )
            btn.pack(anchor=tk.W, pady=5, padx=20, fill=tk.X)
            self.option_buttons.append(btn)
            
        # Control buttons
        control_frame = tk.Frame(self.current_frame)
        control_frame.pack(fill=tk.X, pady=20)
        
        # Submit button
        self.submit_btn = ttk.Button(
            control_frame,
            text="Submit Answer",
            command=self.submit_answer,
            style="Large.TButton"
        )
        self.submit_btn.pack(side=tk.RIGHT, padx=10)
        
        # Skip button
        skip_btn = ttk.Button(
            control_frame,
            text="Skip Question",
            command=self.skip_question,
            style="TButton"
        )
        skip_btn.pack(side=tk.RIGHT)
        
        # Start timer
        self.start_timer()
        
        # Bind keyboard shortcuts
        self.root.bind('<Key-1>', lambda e: self.select_option('A'))
        self.root.bind('<Key-2>', lambda e: self.select_option('B'))
        self.root.bind('<Key-3>', lambda e: self.select_option('C'))
        self.root.bind('<Key-4>', lambda e: self.select_option('D'))
        self.root.bind('<Return>', lambda e: self.submit_answer())
        
    def select_option(self, option: str):
        """Select an option programmatically."""
        self.selected_answer.set(option)
        
    def start_timer(self):
        """Start the countdown timer for the current question."""
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self._timer_worker, daemon=True)
        self.timer_thread.start()
        
    def _timer_worker(self):
        """Timer worker thread."""
        while self.timer_running:
            remaining = self.quiz_session.get_time_remaining()
            
            # Update timer display
            self.root.after(0, self._update_timer_display, remaining)
            
            if remaining <= 0:
                # Time's up - auto submit
                self.root.after(0, self.time_up)
                break
                
            time.sleep(1)
            
    def _update_timer_display(self, remaining: int):
        """Update timer display on main thread."""
        if hasattr(self, 'timer_label'):
            self.timer_label.config(text=str(remaining))
            
            # Change color when time is running low
            if remaining <= 10:
                self.timer_label.config(foreground="red")
            elif remaining <= 20:
                self.timer_label.config(foreground="orange")
            else:
                self.timer_label.config(foreground="green")
                
    def time_up(self):
        """Handle when time runs out."""
        self.timer_running = False
        messagebox.showwarning("Time's Up!", "Time has run out for this question!")
        self.skip_question()
        
    def submit_answer(self):
        """Submit the selected answer."""
        selected = self.selected_answer.get()
        
        if not selected:
            messagebox.showwarning("No Answer", "Please select an answer before submitting.")
            return
            
        self.timer_running = False  # Stop timer
        
        # Process answer
        result = self.quiz_session.submit_answer(selected)
        
        # Show result popup
        self.show_answer_result(result)
        
        if result.get('quiz_complete', False):
            self.show_results_screen()
        else:
            self.show_quiz_screen()  # Next question
            
    def skip_question(self):
        """Skip the current question."""
        self.timer_running = False
        result = self.quiz_session.auto_submit()
        
        if result.get('quiz_complete', False):
            self.show_results_screen()
        else:
            self.show_quiz_screen()  # Next question
            
    def show_answer_result(self, result: Dict):
        """Show popup with enhanced answer result including points and achievements."""
        if result['is_correct']:
            title = "Correct! ✅"
            points_text = f" (+{result.get('points_earned', 0)} points)" if result.get('points_earned') else ""
            message = f"Well done! The answer is {result['correct_answer']}: {result['correct_option']}{points_text}"
            
            # Check for new achievements
            if result.get('achievements'):
                new_achievements = [ach for ach in result['achievements'] if ach not in getattr(self, 'previous_achievements', [])]
                if new_achievements:
                    message += f"\n\n🏆 New Achievement: {', '.join(new_achievements)}!"
                    
            icon = messagebox.showinfo
        else:
            title = "Incorrect ❌"
            message = f"Sorry, the correct answer is {result['correct_answer']}: {result['correct_option']}\n"
            if result.get('user_option') and result['user_option'] != 'No answer':
                message += f"You selected: {result['user_option']}"
            icon = messagebox.showwarning
            
        # Add explanation if available
        if result.get('explanation'):
            message += f"\n\nExplanation: {result['explanation']}"
            
        icon(title, message)
        
        # Update previous achievements for comparison
        self.previous_achievements = result.get('achievements', [])
        
    def show_results_screen(self):
        """Display the final results screen."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.main_container)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        results = self.quiz_session.get_final_results()
        
        # Save results to database
        try:
            score_id = self.quiz_manager.save_results(self.player_name.get(), self.quiz_session)
        except Exception as e:
            print(f"Error saving results: {e}")
            
        # Title
        title_label = ttk.Label(
            self.current_frame,
            text="🎉 Quiz Complete! 🎉",
            style="Title.TLabel"
        )
        title_label.pack(pady=20)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.current_frame, text="Your Results", padding=20)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=50)
        
        # Score display
        score_text = f"""
        Player: {self.player_name.get()}
        Language: {results.get('language', 'en').upper()}
        Category: {results.get('category', 'all').title()}
        
        Final Score: {results['score']} / {results['total_questions']}
        Percentage: {results['percentage']}%
        Grade: {results['grade']}
        
        Points Earned: {results.get('points_earned', 0)} / {results.get('max_possible_points', 0)}
        Points Percentage: {results.get('points_percentage', 0):.1f}%
        
        Time Taken: {format_time(results['total_time'])}
        Average Time per Question: {results['average_time_per_question']} seconds
        
        Performance Rating: {results.get('performance_rating', 'Good')}
        """
        
        # Add achievements if any
        if results.get('achievements'):
            score_text += f"\n        Achievements Earned: {len(results['achievements'])}\n"
            for achievement in results['achievements']:
                score_text += f"        🏆 {achievement}\n"
        
        score_label = ttk.Label(
            results_frame,
            text=score_text,
            style="Score.TLabel",
            justify=tk.CENTER
        )
        score_label.pack(pady=20)
        
        # Performance message
        performance_msg = self.get_performance_message(results['percentage'])
        performance_label = ttk.Label(
            results_frame,
            text=performance_msg,
            font=("Arial", 11, "italic"),
            justify=tk.CENTER
        )
        performance_label.pack(pady=10)
        
        # Detailed answers frame
        details_frame = ttk.LabelFrame(results_frame, text="Detailed Review", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Scrolled text for answers review
        self.answers_text = scrolledtext.ScrolledText(
            details_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=("Arial", 10)
        )
        self.answers_text.pack(fill=tk.BOTH, expand=True)
        
        # Populate answers review
        self.populate_answers_review(results['answers'])
        
        # Buttons frame
        buttons_frame = tk.Frame(self.current_frame)
        buttons_frame.pack(pady=20)
        
        # New Quiz button
        new_quiz_btn = ttk.Button(
            buttons_frame,
            text="🔄 Take New Quiz",
            command=self.show_welcome_screen,
            style="Large.TButton"
        )
        new_quiz_btn.pack(side=tk.LEFT, padx=10)
        
        # View Leaderboard button
        leaderboard_btn = ttk.Button(
            buttons_frame,
            text="🏆 View Leaderboard",
            command=self.show_leaderboard,
            style="Large.TButton"
        )
        leaderboard_btn.pack(side=tk.LEFT, padx=10)
        
        # Export Results button
        export_btn = ttk.Button(
            buttons_frame,
            text="💾 Export Results",
            command=self.export_results,
            style="TButton"
        )
        export_btn.pack(side=tk.LEFT, padx=10)
        
    def get_performance_message(self, percentage: float) -> str:
        """Get performance message based on score percentage."""
        if percentage >= 90:
            return "🌟 Outstanding! You're a quiz master! 🌟"
        elif percentage >= 80:
            return "🎯 Excellent work! You really know your stuff!"
        elif percentage >= 70:
            return "👍 Good job! You did well on this quiz."
        elif percentage >= 60:
            return "📚 Not bad! Keep studying and you'll improve."
        else:
            return "💪 Don't give up! Practice makes perfect."
            
    def populate_answers_review(self, answers: List[Dict]):
        """Populate the detailed answers review."""
        self.answers_text.delete('1.0', tk.END)
        
        for i, answer in enumerate(answers, 1):
            status = "✅ CORRECT" if answer['is_correct'] else "❌ INCORRECT"
            
            review_text = f"""
Question {i}: {answer['question']}
{status}

Your Answer: {answer.get('user_answer', 'No answer')}
Correct Answer: {answer['correct_answer']}
Time Taken: {answer['time_taken']:.1f} seconds

{'-' * 80}
"""
            self.answers_text.insert(tk.END, review_text)
            
    def show_leaderboard(self):
        """Display the leaderboard window."""
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("🏆 Leaderboard")
        leaderboard_window.geometry("700x500")
        leaderboard_window.resizable(True, True)
        
        # Center the window
        leaderboard_window.transient(self.root)
        leaderboard_window.grab_set()
        
        # Title
        title_label = ttk.Label(
            leaderboard_window,
            text="🏆 Top Players Leaderboard",
            style="Title.TLabel"
        )
        title_label.pack(pady=20)
        
        # Difficulty filter
        filter_frame = tk.Frame(leaderboard_window)
        filter_frame.pack(pady=10)
        
        ttk.Label(filter_frame, text="Filter by difficulty:").pack(side=tk.LEFT, padx=5)
        
        difficulty_var = tk.StringVar(value="all")
        difficulty_combo = ttk.Combobox(
            filter_frame,
            textvariable=difficulty_var,
            values=["all", "easy", "medium", "hard"],
            state="readonly",
            width=10
        )
        difficulty_combo.pack(side=tk.LEFT, padx=5)
        
        # Leaderboard frame
        lb_frame = ttk.LabelFrame(leaderboard_window, text="Rankings", padding=10)
        lb_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # Treeview for leaderboard
        columns = ('Rank', 'Player', 'Score', 'Percentage', 'Time', 'Difficulty', 'Date')
        lb_tree = ttk.Treeview(lb_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        lb_tree.heading('Rank', text='Rank')
        lb_tree.heading('Player', text='Player Name')
        lb_tree.heading('Score', text='Score')
        lb_tree.heading('Percentage', text='Percentage')
        lb_tree.heading('Time', text='Time')
        lb_tree.heading('Difficulty', text='Difficulty')
        lb_tree.heading('Date', text='Date')
        
        # Column widths
        lb_tree.column('Rank', width=60)
        lb_tree.column('Player', width=150)
        lb_tree.column('Score', width=80)
        lb_tree.column('Percentage', width=100)
        lb_tree.column('Time', width=80)
        lb_tree.column('Difficulty', width=80)
        lb_tree.column('Date', width=120)
        
        # Scrollbar
        lb_scrollbar = ttk.Scrollbar(lb_frame, orient=tk.VERTICAL, command=lb_tree.yview)
        lb_tree.configure(yscrollcommand=lb_scrollbar.set)
        
        lb_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        lb_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def update_leaderboard():
            """Update leaderboard display."""
            # Clear existing items
            for item in lb_tree.get_children():
                lb_tree.delete(item)
                
            # Get leaderboard data
            difficulty_filter = difficulty_var.get() if difficulty_var.get() != "all" else None
            leaderboard = self.db_manager.get_leaderboard(limit=50, difficulty=difficulty_filter)
            
            # Populate treeview
            for entry in leaderboard:
                date_str = entry['date_played'][:10] if entry['date_played'] else "N/A"
                time_str = format_time(entry['time_taken'])
                
                lb_tree.insert('', tk.END, values=(
                    entry['rank'],
                    entry['player_name'],
                    f"{entry['score']}/{entry['total_questions']}",
                    f"{entry['percentage']:.1f}%",
                    time_str,
                    entry['difficulty'].title(),
                    date_str
                ))
                
        # Initial load
        update_leaderboard()
        
        # Bind filter change
        difficulty_combo.bind('<<ComboboxSelected>>', lambda e: update_leaderboard())
        
        # Buttons frame
        btn_frame = tk.Frame(leaderboard_window)
        btn_frame.pack(pady=20)
        
        # Refresh button
        refresh_btn = ttk.Button(
            btn_frame,
            text="🔄 Refresh",
            command=update_leaderboard
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        # Clear leaderboard button
        clear_btn = ttk.Button(
            btn_frame,
            text="🗑️ Clear All",
            command=lambda: self.clear_leaderboard_confirm(update_leaderboard)
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Export button
        export_btn = ttk.Button(
            btn_frame,
            text="💾 Export CSV",
            command=self.export_leaderboard
        )
        export_btn.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_btn = ttk.Button(
            btn_frame,
            text="Close",
            command=leaderboard_window.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=10)
        
    def clear_leaderboard_confirm(self, callback):
        """Confirm and clear leaderboard."""
        if messagebox.askyesno(
            "Clear Leaderboard", 
            "Are you sure you want to clear all leaderboard entries?\n\nThis action cannot be undone."
        ):
            try:
                self.db_manager.clear_leaderboard()
                callback()  # Refresh display
                messagebox.showinfo("Success", "Leaderboard cleared successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear leaderboard: {str(e)}")
                
    def export_leaderboard(self):
        """Export leaderboard to CSV file."""
        try:
            filename = f"leaderboard_{int(time.time())}.csv"
            success = self.db_manager.export_leaderboard_csv(filename)
            
            if success:
                messagebox.showinfo(
                    "Export Successful", 
                    f"Leaderboard exported to: {filename}"
                )
            else:
                messagebox.showerror("Export Failed", "Failed to export leaderboard.")
        except Exception as e:
            messagebox.showerror("Error", f"Export error: {str(e)}")
            
    def show_statistics(self):
        """Display statistics window."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Statistics")
        stats_window.geometry("500x400")
        stats_window.resizable(False, False)
        
        # Center the window
        stats_window.transient(self.root)
        stats_window.grab_set()
        
        # Title
        title_label = ttk.Label(
            stats_window,
            text="📊 Quiz Statistics",
            style="Title.TLabel"
        )
        title_label.pack(pady=20)
        
        # Get statistics
        stats = self.quiz_manager.get_statistics()
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(stats_window, text="Overall Statistics", padding=20)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # Statistics text
        stats_text = f"""
        📈 Total Games Played: {stats['total_games']}
        
        👥 Unique Players: {stats['total_players']}
        
        ⭐ Average Score: {stats['average_score']}
        
        🏆 Highest Score: {stats['highest_score']}
        
        📊 Average Percentage: {stats['average_percentage']}%
        
        🥇 Top Player: {stats.get('top_player', 'None')}
        """
        
        stats_label = ttk.Label(
            stats_frame,
            text=stats_text,
            font=('Arial', 11),
            justify=tk.LEFT
        )
        stats_label.pack(pady=20)
        
        # Close button
        close_btn = ttk.Button(
            stats_window,
            text="Close",
            command=stats_window.destroy,
            style="Large.TButton"
        )
        close_btn.pack(pady=20)
        
    def export_results(self):
        """Export current quiz results."""
        if not hasattr(self, 'quiz_session'):
            messagebox.showerror("Error", "No quiz results to export.")
            return
            
        try:
            results = self.quiz_session.get_final_results()
            timestamp = int(time.time())
            filename = f"quiz_results_{self.player_name.get()}_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Quiz Master - Results Export\n")
                f.write(f"{'=' * 40}\n\n")
                f.write(f"Player: {self.player_name.get()}\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Difficulty: {self.difficulty.get().title()}\n\n")
                
                f.write(f"Final Score: {results['score']} / {results['total_questions']}\n")
                f.write(f"Percentage: {results['percentage']}%\n")
                f.write(f"Grade: {results['grade']}\n")
                f.write(f"Time Taken: {format_time(results['total_time'])}\n\n")
                
                f.write(f"Detailed Answers:\n")
                f.write(f"{'=' * 40}\n")
                
                for i, answer in enumerate(results['answers'], 1):
                    status = "CORRECT" if answer['is_correct'] else "INCORRECT"
                    f.write(f"\nQuestion {i}: {answer['question']}\n")
                    f.write(f"Status: {status}\n")
                    f.write(f"Your Answer: {answer.get('user_answer', 'No answer')}\n")
                    f.write(f"Correct Answer: {answer['correct_answer']}\n")
                    f.write(f"Time Taken: {answer['time_taken']:.1f} seconds\n")
                    
            messagebox.showinfo(
                "Export Successful",
                f"Results exported to: {filename}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results: {str(e)}")
            
    def __del__(self):
        """Cleanup when UI manager is destroyed."""
        self.timer_running = False
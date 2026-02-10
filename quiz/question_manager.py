#!/usr/bin/env python3
"""
Question Management System for Quiz Master Application
Provides tools for adding, editing, and managing quiz questions.

Author: Qoder AI Assistant
Date: 2025-08-26
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
from typing import Dict, List, Optional
from database import DatabaseManager


class QuestionManagerUI:
    """
    Advanced question management interface for Quiz Master.
    Allows adding, editing, importing, and exporting questions.
    """
    
    def __init__(self, parent_window, database_manager: DatabaseManager):
        """
        Initialize the question manager UI.
        
        Args:
            parent_window: Parent tkinter window
            database_manager: Database manager instance
        """
        self.parent = parent_window
        self.db_manager = database_manager
        self.window = None
        
    def show_question_manager(self):
        """Display the question management window."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📝 Question Management System")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        
        # Center the window
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Create main interface
        self.create_interface()
        
    def create_interface(self):
        """Create the main question management interface."""
        # Title
        title_label = ttk.Label(
            self.window,
            text="📝 Question Management System",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Create notebook for different tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add Question Tab
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="➕ Add Question")
        self.create_add_question_tab()\n        
        # Edit Questions Tab
        self.edit_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.edit_tab, text="✏️ Edit Questions")
        self.create_edit_questions_tab()
        
        # Import/Export Tab
        self.import_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.import_tab, text="📂 Import/Export")
        self.create_import_export_tab()
        
        # Statistics Tab
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="📊 Statistics")
        self.create_statistics_tab()
        
    def create_add_question_tab(self):
        """Create the add question tab interface."""
        # Scrollable frame for the form
        canvas = tk.Canvas(self.add_tab)
        scrollbar = ttk.Scrollbar(self.add_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        form_frame = ttk.LabelFrame(scrollable_frame, text="Question Details", padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Question text (English)
        ttk.Label(form_frame, text="Question (English)*:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.question_en = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, height=3)
        self.question_en.pack(fill=tk.X, pady=5)
        
        # Multi-language questions
        languages = [
            ("French", "question_fr"),
            ("Spanish", "question_es"), 
            ("German", "question_de"),
            ("Japanese", "question_ja"),
            ("Chinese", "question_zh")
        ]
        
        self.lang_questions = {}\n        for lang, field in languages:
            ttk.Label(form_frame, text=f"Question ({lang}):", font=("Arial", 10)).pack(anchor=tk.W, pady=2)
            widget = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, height=2)
            widget.pack(fill=tk.X, pady=2)
            self.lang_questions[field] = widget
            
        # Options section
        options_frame = ttk.LabelFrame(form_frame, text="Answer Options", padding=10)
        options_frame.pack(fill=tk.X, pady=15)
        
        # English options
        ttk.Label(options_frame, text="Options (English)*:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.options_en = []
        for i, letter in enumerate(['A', 'B', 'C', 'D']):
            ttk.Label(options_frame, text=f"Option {letter}:", font=("Arial", 9)).pack(anchor=tk.W)
            option_entry = tk.Entry(options_frame, font=("Arial", 10))
            option_entry.pack(fill=tk.X, pady=2)
            self.options_en.append(option_entry)
            
        # Multi-language options
        self.lang_options = {}
        for lang, field in languages:
            ttk.Label(options_frame, text=f"Options ({lang}):", font=("Arial", 10)).pack(anchor=tk.W, pady=(10, 2))
            lang_opts = []
            for i, letter in enumerate(['A', 'B', 'C', 'D']):
                ttk.Label(options_frame, text=f"Option {letter}:", font=("Arial", 9)).pack(anchor=tk.W)
                option_entry = tk.Entry(options_frame, font=("Arial", 9))
                option_entry.pack(fill=tk.X, pady=1)
                lang_opts.append(option_entry)
            self.lang_options[field] = lang_opts
            
        # Metadata section
        meta_frame = ttk.LabelFrame(form_frame, text="Question Metadata", padding=10)
        meta_frame.pack(fill=tk.X, pady=15)
        
        # Correct answer
        ttk.Label(meta_frame, text="Correct Answer*:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.correct_answer = ttk.Combobox(meta_frame, values=['A', 'B', 'C', 'D'], state="readonly")
        self.correct_answer.pack(fill=tk.X, pady=5)
        
        # Difficulty
        ttk.Label(meta_frame, text="Difficulty*:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.difficulty = ttk.Combobox(meta_frame, values=['easy', 'medium', 'hard', 'expert'], state="readonly")
        self.difficulty.pack(fill=tk.X, pady=5)
        
        # Category and Subject
        row1 = tk.Frame(meta_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="Category*:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.category = ttk.Combobox(row1, values=self.get_categories(), state="readonly")
        self.category.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        ttk.Label(row1, text="Subject:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.subject = tk.Entry(row1, font=("Arial", 10))
        self.subject.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Field and Points
        row2 = tk.Frame(meta_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="Field:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.field = ttk.Combobox(row2, values=['science', 'technology', 'humanities', 'arts', 'social_sciences', 'health_sciences'], state="readonly")
        self.field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        ttk.Label(row2, text="Points:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.points = tk.Spinbox(row2, from_=5, to=50, value=10, font=("Arial", 10))
        self.points.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Language and Tags
        row3 = tk.Frame(meta_frame)
        row3.pack(fill=tk.X, pady=5)
        
        ttk.Label(row3, text="Language:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.language = ttk.Combobox(row3, values=['en', 'es', 'fr', 'de', 'ja', 'zh', 'multi'], state="readonly")
        self.language.set('en')
        self.language.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        ttk.Label(row3, text="Tags (comma-separated):", font=("Arial", 10)).pack(side=tk.LEFT)
        self.tags = tk.Entry(row3, font=("Arial", 10))
        self.tags.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Explanation
        ttk.Label(meta_frame, text="Explanation:", font=("Arial", 10)).pack(anchor=tk.W, pady=(10, 2))
        self.explanation = scrolledtext.ScrolledText(meta_frame, wrap=tk.WORD, height=3)
        self.explanation.pack(fill=tk.X, pady=5)
        
        # Buttons
        button_frame = tk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(button_frame, text="💾 Save Question", command=self.save_question).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="👁️ Preview", command=self.preview_question).pack(side=tk.LEFT, padx=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_edit_questions_tab(self):
        """Create the edit questions tab interface."""
        # Search and filter frame
        search_frame = ttk.LabelFrame(self.edit_tab, text="Search & Filter", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Search row
        search_row = tk.Frame(search_frame)
        search_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_row, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_row, font=("Arial", 10))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_row, text="🔍 Search", command=self.search_questions).pack(side=tk.LEFT, padx=5)
        
        # Filter row
        filter_row = tk.Frame(search_frame)
        filter_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_row, text="Category:").pack(side=tk.LEFT, padx=5)
        self.filter_category = ttk.Combobox(filter_row, values=['All'] + self.get_categories(), state="readonly")
        self.filter_category.set('All')
        self.filter_category.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_row, text="Difficulty:").pack(side=tk.LEFT, padx=5)
        self.filter_difficulty = ttk.Combobox(filter_row, values=['All', 'easy', 'medium', 'hard', 'expert'], state="readonly")
        self.filter_difficulty.set('All')
        self.filter_difficulty.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_row, text="🔄 Refresh", command=self.refresh_questions).pack(side=tk.LEFT, padx=5)
        
        # Questions list
        list_frame = ttk.LabelFrame(self.edit_tab, text="Questions", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for questions
        columns = ('ID', 'Question', 'Category', 'Difficulty', 'Points', 'Language')
        self.questions_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.questions_tree.heading('ID', text='ID')
        self.questions_tree.heading('Question', text='Question')
        self.questions_tree.heading('Category', text='Category')
        self.questions_tree.heading('Difficulty', text='Difficulty')
        self.questions_tree.heading('Points', text='Points')
        self.questions_tree.heading('Language', text='Language')
        
        # Column widths
        self.questions_tree.column('ID', width=50)
        self.questions_tree.column('Question', width=400)
        self.questions_tree.column('Category', width=100)
        self.questions_tree.column('Difficulty', width=80)
        self.questions_tree.column('Points', width=60)
        self.questions_tree.column('Language', width=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.questions_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.questions_tree.xview)
        self.questions_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.questions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame for question actions
        action_frame = tk.Frame(self.edit_tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="✏️ Edit Selected", command=self.edit_selected_question).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🗑️ Delete Selected", command=self.delete_selected_question).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="📋 Duplicate", command=self.duplicate_selected_question).pack(side=tk.LEFT, padx=5)
        
        # Load questions initially
        self.refresh_questions()
        
    def create_import_export_tab(self):
        """Create the import/export tab interface."""
        # Import section
        import_frame = ttk.LabelFrame(self.import_tab, text="📥 Import Questions", padding=15)
        import_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(import_frame, text="Import questions from JSON file:", font=("Arial", 11)).pack(anchor=tk.W, pady=5)
        
        import_buttons = tk.Frame(import_frame)
        import_buttons.pack(fill=tk.X, pady=5)
        
        ttk.Button(import_buttons, text="📁 Select JSON File", command=self.import_questions_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(import_buttons, text="🌐 Load Sample Questions", command=self.load_sample_questions).pack(side=tk.LEFT, padx=5)
        
        # Export section
        export_frame = ttk.LabelFrame(self.import_tab, text="📤 Export Questions", padding=15)
        export_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(export_frame, text="Export questions to various formats:", font=("Arial", 11)).pack(anchor=tk.W, pady=5)
        
        export_buttons = tk.Frame(export_frame)
        export_buttons.pack(fill=tk.X, pady=5)
        
        ttk.Button(export_buttons, text="💾 Export as JSON", command=self.export_questions_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_buttons, text="📊 Export as CSV", command=self.export_questions_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_buttons, text="📄 Export as Text", command=self.export_questions_txt).pack(side=tk.LEFT, padx=5)
        
        # Batch operations
        batch_frame = ttk.LabelFrame(self.import_tab, text="⚡ Batch Operations", padding=15)
        batch_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(batch_frame, text="Perform operations on multiple questions:", font=("Arial", 11)).pack(anchor=tk.W, pady=5)
        
        batch_buttons = tk.Frame(batch_frame)
        batch_buttons.pack(fill=tk.X, pady=5)
        
        ttk.Button(batch_buttons, text="🏷️ Update Categories", command=self.batch_update_categories).pack(side=tk.LEFT, padx=5)
        ttk.Button(batch_buttons, text="🔄 Recalculate Points", command=self.batch_update_points).pack(side=tk.LEFT, padx=5)
        ttk.Button(batch_buttons, text="🧹 Clean Database", command=self.clean_database).pack(side=tk.LEFT, padx=5)
        
    def create_statistics_tab(self):
        """Create the statistics tab interface."""
        stats_frame = ttk.LabelFrame(self.stats_tab, text="📊 Question Database Statistics", padding=15)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Statistics display
        self.stats_text = scrolledtext.ScrolledText(stats_frame, wrap=tk.WORD, font=("Courier", 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Refresh button
        ttk.Button(stats_frame, text="🔄 Refresh Statistics", command=self.refresh_statistics).pack(pady=10)
        
        # Load initial statistics
        self.refresh_statistics()
        
    def get_categories(self) -> List[str]:
        \"\"\"Get available categories from database.\"\"\"\n        try:\n            categories = self.db_manager.get_categories()\n            return categories if categories else ['general', 'science', 'mathematics', 'history', 'literature']\n        except:\n            return ['general', 'science', 'mathematics', 'history', 'literature']
            
    def save_question(self):
        """Save a new question to the database."""
        try:
            # Validate required fields
            if not self.question_en.get("1.0", tk.END).strip():
                messagebox.showerror("Error", "Question text is required!")
                return
                
            if not all(opt.get().strip() for opt in self.options_en):
                messagebox.showerror("Error", "All answer options are required!")
                return
                
            if not self.correct_answer.get():
                messagebox.showerror("Error", "Correct answer is required!")
                return
                
            # Prepare question data
            question_data = {
                'question': self.question_en.get("1.0", tk.END).strip(),
                'options': [opt.get().strip() for opt in self.options_en],
                'correct_answer': self.correct_answer.get(),
                'difficulty': self.difficulty.get() or 'medium',
                'category': self.category.get() or 'general',
                'subject': self.subject.get() or 'general',
                'field': self.field.get() or 'general',
                'points': int(self.points.get()) if self.points.get() else 10,
                'language': self.language.get() or 'en',
                'explanation': self.explanation.get("1.0", tk.END).strip(),
                'tags': [tag.strip() for tag in self.tags.get().split(',') if tag.strip()]
            }
            
            # Add multi-language versions if provided
            for field, widget in self.lang_questions.items():
                text = widget.get("1.0", tk.END).strip()
                if text:
                    question_data[field] = text
                    
            for field, widgets in self.lang_options.items():
                options = [w.get().strip() for w in widgets]
                if any(options):  # If any option is filled
                    question_data[f"options_{field.split('_')[1]}"] = options
                    
            # Save to database
            question_id = self.db_manager.add_advanced_question(question_data)
            
            messagebox.showinfo("Success", f"Question saved successfully! (ID: {question_id})")
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save question: {str(e)}")
            
    def clear_form(self):
        """Clear all form fields."""
        self.question_en.delete("1.0", tk.END)
        
        for widget in self.lang_questions.values():
            widget.delete("1.0", tk.END)
            
        for opt in self.options_en:
            opt.delete(0, tk.END)
            
        for widgets in self.lang_options.values():
            for widget in widgets:
                widget.delete(0, tk.END)
                
        self.correct_answer.set('')
        self.difficulty.set('')
        self.category.set('')
        self.subject.delete(0, tk.END)
        self.field.set('')
        self.points.delete(0, tk.END)
        self.points.insert(0, '10')
        self.language.set('en')
        self.tags.delete(0, tk.END)
        self.explanation.delete("1.0", tk.END)
        
    def preview_question(self):
        """Preview the question in a popup window."""
        if not self.question_en.get("1.0", tk.END).strip():
            messagebox.showwarning("Warning", "Please enter a question first.")
            return
            
        preview_window = tk.Toplevel(self.window)
        preview_window.title("Question Preview")
        preview_window.geometry("500x400")
        
        # Question text
        ttk.Label(preview_window, text="Question Preview", font=("Arial", 14, "bold")).pack(pady=10)
        
        question_frame = ttk.LabelFrame(preview_window, text="Question", padding=10)
        question_frame.pack(fill=tk.X, padx=20, pady=10)
        
        question_label = ttk.Label(question_frame, text=self.question_en.get("1.0", tk.END).strip(), 
                                  wraplength=450, font=("Arial", 11))
        question_label.pack(pady=5)
        
        # Options
        options_frame = ttk.LabelFrame(preview_window, text="Options", padding=10)
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        for i, opt in enumerate(self.options_en):
            if opt.get().strip():
                letter = chr(65 + i)  # A, B, C, D
                is_correct = letter == self.correct_answer.get()
                color = "green" if is_correct else "black"
                ttk.Label(options_frame, text=f"{letter}. {opt.get().strip()}", 
                         foreground=color, font=("Arial", 10, "bold" if is_correct else "normal")).pack(anchor=tk.W, pady=2)
                         
        # Metadata
        meta_frame = ttk.LabelFrame(preview_window, text="Metadata", padding=10)
        meta_frame.pack(fill=tk.X, padx=20, pady=10)
        
        meta_text = f"""Difficulty: {self.difficulty.get() or 'medium'}
Category: {self.category.get() or 'general'}
Points: {self.points.get() or '10'}
Language: {self.language.get() or 'en'}"""
        
        ttk.Label(meta_frame, text=meta_text, font=("Arial", 9)).pack(anchor=tk.W)
        
        ttk.Button(preview_window, text="Close", command=preview_window.destroy).pack(pady=20)
        
    def refresh_questions(self):
        """Refresh the questions list."""
        # Clear existing items
        for item in self.questions_tree.get_children():
            self.questions_tree.delete(item)
            
        try:
            # Get filter values
            category_filter = self.filter_category.get() if self.filter_category.get() != 'All' else None
            difficulty_filter = self.filter_difficulty.get() if self.filter_difficulty.get() != 'All' else None
            
            # Get questions from database
            questions = self.db_manager.get_questions(
                limit=1000,  # Get more for editing
                category=category_filter,
                difficulty=difficulty_filter,
                shuffle=False
            )
            
            # Populate treeview
            for q in questions:
                question_preview = q['question'][:100] + "..." if len(q['question']) > 100 else q['question']
                self.questions_tree.insert('', tk.END, values=(
                    q['id'],
                    question_preview,
                    q.get('category', 'general'),
                    q.get('difficulty', 'medium'),
                    q.get('points', 10),
                    q.get('language', 'en')
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {str(e)}")
            
    def search_questions(self):
        """Search questions by text."""
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            self.refresh_questions()
            return
            
        # Clear existing items
        for item in self.questions_tree.get_children():
            self.questions_tree.delete(item)
            
        try:
            questions = self.db_manager.get_questions(limit=1000, shuffle=False)
            
            # Filter by search term
            filtered_questions = [
                q for q in questions 
                if search_term in q['question'].lower() or 
                   any(search_term in opt.lower() for opt in q['options'])
            ]
            
            # Populate treeview
            for q in filtered_questions:
                question_preview = q['question'][:100] + "..." if len(q['question']) > 100 else q['question']
                self.questions_tree.insert('', tk.END, values=(
                    q['id'],
                    question_preview,
                    q.get('category', 'general'),
                    q.get('difficulty', 'medium'),
                    q.get('points', 10),
                    q.get('language', 'en')
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
            
    def edit_selected_question(self):
        """Edit the selected question."""
        selection = self.questions_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a question to edit.")
            return
            
        messagebox.showinfo("Info", "Edit functionality will be implemented in the next version.")
        
    def delete_selected_question(self):
        """Delete the selected question."""
        selection = self.questions_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a question to delete.")
            return
            
        item = selection[0]
        question_id = self.questions_tree.item(item)['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete question ID {question_id}?"):
            try:
                cursor = self.db_manager.connection.cursor()
                cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
                self.db_manager.connection.commit()
                
                messagebox.showinfo("Success", "Question deleted successfully!")
                self.refresh_questions()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete question: {str(e)}")
                
    def duplicate_selected_question(self):
        """Duplicate the selected question."""
        selection = self.questions_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a question to duplicate.")
            return
            
        messagebox.showinfo("Info", "Duplicate functionality will be implemented in the next version.")
        
    def import_questions_json(self):
        """Import questions from JSON file."""
        filename = filedialog.askopenfilename(
            title="Select JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                questions_added = 0
                
                # Handle different JSON formats
                if 'advanced_questions' in data:
                    questions = data['advanced_questions']
                elif 'questions' in data:
                    questions = data['questions']
                else:
                    questions = data if isinstance(data, list) else [data]
                    
                for q in questions:
                    try:
                        self.db_manager.add_advanced_question(q)
                        questions_added += 1
                    except Exception as e:
                        print(f"Error adding question: {e}")
                        
                messagebox.showinfo("Success", f"Imported {questions_added} questions successfully!")
                self.refresh_questions()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import questions: {str(e)}")
                
    def export_questions_json(self):
        """Export questions to JSON file."""
        filename = filedialog.asksaveasfilename(
            title="Save questions as JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                questions = self.db_manager.get_questions(limit=10000, shuffle=False)
                
                from datetime import datetime
                export_data = {
                    "questions": questions,
                    "metadata": {
                        "exported_date": str(datetime.now()),
                        "total_questions": len(questions),
                        "export_source": "Quiz Master Question Manager"
                    }
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                    
                messagebox.showinfo("Success", f"Exported {len(questions)} questions to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export questions: {str(e)}")
                
    def refresh_statistics(self):
        """Refresh and display question statistics."""
        try:
            stats = self.db_manager.get_question_stats()
            
            stats_text = f"""📊 QUESTION DATABASE STATISTICS
{'=' * 50}

📈 OVERVIEW:
  Total Questions: {stats.get('total_questions', 0)}
  
📚 BY DIFFICULTY:
"""
            
            for difficulty, count in stats.get('by_difficulty', {}).items():
                stats_text += f"  {difficulty.title()}: {count} questions\n"
                
            stats_text += "\n🏷️ BY CATEGORY:\n"
            for category, count in stats.get('by_category', {}).items():
                stats_text += f"  {category.title()}: {count} questions\n"
                
            stats_text += "\n🌐 BY LANGUAGE:\n"
            for language, count in stats.get('by_language', {}).items():
                stats_text += f"  {language.upper()}: {count} questions\n"
                
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', stats_text)
            
        except Exception as e:
            error_text = f"Error loading statistics: {str(e)}"
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', error_text)
            
    def load_sample_questions(self):
        """Load sample questions from advanced_questions.json."""
        try:
            with open('advanced_questions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            questions_added = 0
            for q in data['advanced_questions']:
                try:
                    self.db_manager.add_advanced_question(q)
                    questions_added += 1
                except Exception as e:
                    print(f"Error adding question: {e}")
                    
            messagebox.showinfo("Success", f"Loaded {questions_added} sample questions!")
            self.refresh_questions()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sample questions: {str(e)}")
            
    # Placeholder methods for features to be implemented
    def export_questions_csv(self):
        messagebox.showinfo("Info", "CSV export will be implemented in the next version.")
        
    def export_questions_txt(self):
        messagebox.showinfo("Info", "Text export will be implemented in the next version.")
        
    def batch_update_categories(self):
        messagebox.showinfo("Info", "Batch category update will be implemented in the next version.")
        
    def batch_update_points(self):
        messagebox.showinfo("Info", "Batch points update will be implemented in the next version.")
        
    def clean_database(self):
        if messagebox.askyesno("Confirm", "This will remove duplicate and invalid questions. Continue?"):
            messagebox.showinfo("Info", "Database cleaning will be implemented in the next version.")


# Test function
if __name__ == "__main__":
    from database import DatabaseManager
    
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    db = DatabaseManager("test_questions.db")
    qm = QuestionManagerUI(root, db)
    qm.show_question_manager()
    
    root.mainloop()
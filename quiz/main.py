#!/usr/bin/env python3
"""
Quiz Master - A Python GUI Quiz Application
Entry point for the Quiz Master application.

Author: Qoder AI Assistant
Date: 2025-08-26
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ui_manager import QuizMasterUI
    from database import DatabaseManager
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure all required modules are in the same directory.")
    sys.exit(1)


class QuizMaster:
    """
    Main application class for Quiz Master.
    Handles initialization and coordination between components.
    """
    
    def __init__(self):
        """Initialize the Quiz Master application."""
        self.root = tk.Tk()
        self.root.title("Quiz Master")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set application icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass  # Ignore if icon file not found
        
        # Initialize database
        self.db_manager = DatabaseManager()
        
        # Initialize UI
        self.ui = QuizMasterUI(self.root, self.db_manager)
        
        # Center the window on screen
        self.center_window()
        
    def center_window(self):
        """Center the application window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def run(self):
        """Start the Quiz Master application."""
        try:
            # Show welcome message
            messagebox.showinfo(
                "Welcome to Quiz Master!", 
                "Welcome to Quiz Master!\n\nTest your knowledge with our interactive quiz system.\n\nGood luck!"
            )
            
            # Start the main event loop
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Clean up database connection
            if hasattr(self, 'db_manager'):
                self.db_manager.close()


def main():
    """Main function to start the Quiz Master application."""
    try:
        app = QuizMaster()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        messagebox.showerror("Fatal Error", f"A fatal error occurred: {str(e)}")


if __name__ == "__main__":
    main()
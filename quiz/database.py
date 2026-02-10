#!/usr/bin/env python3
"""
Database Manager for Quiz Master Application
Handles SQLite database operations for questions and leaderboard.

Author: Qoder AI Assistant
Date: 2025-08-26
"""

import sqlite3
import json
import os
import random
from datetime import datetime
from typing import List, Dict, Tuple, Optional


class DatabaseManager:
    """
    Manages SQLite database operations for Quiz Master application.
    Handles questions storage and leaderboard functionality.
    """
    
    def __init__(self, db_path: str = "quiz_master.db"):
        """
        Initialize database manager.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self.init_database()
        
    def init_database(self):
        """Initialize database connection and create tables if they don't exist."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            self.create_tables()
            self.populate_sample_questions()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
            raise
            
    def create_tables(self):
        """Create necessary tables for questions and leaderboard."""
        cursor = self.connection.cursor()
        
        # Enhanced Questions table with advanced features
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                question_fr TEXT,
                question_es TEXT,
                question_de TEXT,
                question_ja TEXT,
                question_zh TEXT,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                options_fr TEXT,
                options_es TEXT,
                options_de TEXT,
                options_ja TEXT,
                options_zh TEXT,
                correct_answer TEXT NOT NULL,
                difficulty TEXT DEFAULT 'medium',
                category TEXT DEFAULT 'general',
                subject TEXT DEFAULT 'general',
                field TEXT DEFAULT 'general',
                points INTEGER DEFAULT 10,
                language TEXT DEFAULT 'en',
                explanation TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User achievements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                achievement_type TEXT NOT NULL,
                achievement_name TEXT NOT NULL,
                description TEXT,
                earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced Leaderboard table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                points_earned INTEGER DEFAULT 0,
                time_taken INTEGER NOT NULL,
                difficulty TEXT DEFAULT 'medium',
                category TEXT DEFAULT 'all',
                language TEXT DEFAULT 'en',
                achievements TEXT,
                date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.connection.commit()
        
    def populate_sample_questions(self):
        """Add sample questions to the database if it's empty."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM questions")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Load from advanced questions JSON if available
            try:
                import json
                with open('advanced_questions.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for q in data['advanced_questions']:
                    self.add_advanced_question(
                        question_data=q
                    )
                    
                # Add categories
                for cat in data['categories']:
                    self.add_category(cat['name'], cat['display_name'], cat.get('description', ''))
                    
            except (FileNotFoundError, json.JSONDecodeError):
                # Fallback to basic questions
                self._add_basic_sample_questions()
                
    def _add_basic_sample_questions(self):
        """Add basic sample questions as fallback."""
        sample_questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct": "C",
                "difficulty": "easy",
                "category": "geography"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": "B",
                "difficulty": "easy",
                "category": "science"
            },
            {
                "question": "What is 15 × 8?",
                "options": ["120", "125", "130", "115"],
                "correct": "A",
                "difficulty": "medium",
                "category": "mathematics"
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "correct": "B",
                "difficulty": "medium",
                "category": "literature"
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["Elephant", "Giraffe", "Blue Whale", "Hippopotamus"],
                "correct": "C",
                "difficulty": "easy",
                "category": "biology"
            }
        ]
        
        for q in sample_questions:
            self.add_question(
                question_text=q["question"],
                option_a=q["options"][0],
                option_b=q["options"][1],
                option_c=q["options"][2],
                option_d=q["options"][3],
                correct_answer=q["correct"],
                difficulty=q["difficulty"],
                category=q["category"]
            )
                
    def add_advanced_question(self, question_data: Dict) -> int:
        """Add an advanced question with multi-language support and additional metadata."""
        cursor = self.connection.cursor()
        
        # Convert options to JSON strings for multi-language support
        options_json = {}
        if 'options_fr' in question_data:
            options_json['fr'] = question_data['options_fr']
        if 'options_es' in question_data:
            options_json['es'] = question_data['options_es']
        if 'options_de' in question_data:
            options_json['de'] = question_data['options_de']
        if 'options_ja' in question_data:
            options_json['ja'] = question_data['options_ja']
        if 'options_zh' in question_data:
            options_json['zh'] = question_data['options_zh']
        
        import json
        
        cursor.execute('''
            INSERT INTO questions 
            (question_text, question_fr, question_es, question_de, question_ja, question_zh,
             option_a, option_b, option_c, option_d, 
             options_fr, options_es, options_de, options_ja, options_zh,
             correct_answer, difficulty, category, subject, field, points, language, 
             explanation, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            question_data['question'],
            question_data.get('question_fr'),
            question_data.get('question_es'), 
            question_data.get('question_de'),
            question_data.get('question_ja'),
            question_data.get('question_zh'),
            question_data['options'][0],
            question_data['options'][1],
            question_data['options'][2], 
            question_data['options'][3],
            json.dumps(question_data.get('options_fr', [])) if question_data.get('options_fr') else None,
            json.dumps(question_data.get('options_es', [])) if question_data.get('options_es') else None,
            json.dumps(question_data.get('options_de', [])) if question_data.get('options_de') else None,
            json.dumps(question_data.get('options_ja', [])) if question_data.get('options_ja') else None,
            json.dumps(question_data.get('options_zh', [])) if question_data.get('options_zh') else None,
            question_data['correct_answer'],
            question_data.get('difficulty', 'medium'),
            question_data.get('category', 'general'),
            question_data.get('subject', 'general'),
            question_data.get('field', 'general'),
            question_data.get('points', 10),
            question_data.get('language', 'en'),
            question_data.get('explanation', ''),
            json.dumps(question_data.get('tags', []))
        ))
        
        self.connection.commit()
        return cursor.lastrowid
        
    def add_category(self, name: str, display_name: str, description: str = "") -> int:
        """Add a new category to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO categories (name, display_name, description)
                VALUES (?, ?, ?)
            ''', (name, display_name, description))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Category already exists
            return None
                    
                # Add categories
                for cat in data['categories']:
                    self.add_category(cat['name'], cat['display_name'], cat.get('description', ''))
                    
            except (FileNotFoundError, json.JSONDecodeError):
                # Fallback to basic questions
                self._add_basic_sample_questions()
                
    def _add_basic_sample_questions(self):
        """Add basic sample questions as fallback."""
        sample_questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct": "C",
                "difficulty": "easy",
                "category": "geography"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": "B",
                "difficulty": "easy",
                "category": "science"
            },
            {
                "question": "What is 15 × 8?",
                "options": ["120", "125", "130", "115"],
                "correct": "A",
                "difficulty": "medium",
                "category": "mathematics"
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "correct": "B",
                "difficulty": "medium",
                "category": "literature"
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["Elephant", "Giraffe", "Blue Whale", "Hippopotamus"],
                "correct": "C",
                "difficulty": "easy",
                "category": "biology"
            }
        ]
        
        for q in sample_questions:
            self.add_question(
                question_text=q["question"],
                option_a=q["options"][0],
                option_b=q["options"][1],
                option_c=q["options"][2],
                option_d=q["options"][3],
                correct_answer=q["correct"],
                difficulty=q["difficulty"],
                category=q["category"]
            )
                
    def add_question(self, question_text: str, option_a: str, option_b: str, 
                    option_c: str, option_d: str, correct_answer: str, 
                    difficulty: str = "medium", category: str = "general") -> int:
        """
        Add a new question to the database.
        
        Args:
            question_text (str): The question text
            option_a, option_b, option_c, option_d (str): Answer options
            correct_answer (str): Correct answer (A, B, C, or D)
            difficulty (str): Question difficulty level
            category (str): Question category
            
        Returns:
            int: ID of the inserted question
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO questions 
            (question_text, option_a, option_b, option_c, option_d, 
             correct_answer, difficulty, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (question_text, option_a, option_b, option_c, option_d, 
              correct_answer, difficulty, category))
        
        self.connection.commit()
        return cursor.lastrowid
        
    def get_questions(self, limit: int = 10, difficulty: str = None, 
                     category: str = None, shuffle: bool = True, 
                     language: str = 'en', subject: str = None, 
                     field: str = None) -> List[Dict]:
        """
        Retrieve questions from the database with enhanced filtering.
        
        Args:
            limit (int): Maximum number of questions to retrieve
            difficulty (str): Filter by difficulty level
            category (str): Filter by category
            shuffle (bool): Whether to randomize question order
            language (str): Preferred language for questions
            subject (str): Filter by subject
            field (str): Filter by field
            
        Returns:
            List[Dict]: List of question dictionaries
        """
        cursor = self.connection.cursor()
        
        query = "SELECT * FROM questions"
        params = []
        
        # Add filters
        conditions = []
        if difficulty:
            conditions.append("difficulty = ?")
            params.append(difficulty)
        if category:
            conditions.append("category = ?")
            params.append(category)
        if subject:
            conditions.append("subject = ?")
            params.append(subject)
        if field:
            conditions.append("field = ?")
            params.append(field)
        if language and language != 'all':
            conditions.append("(language = ? OR language = 'multi')")
            params.append(language)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        # Add random ordering if shuffle is True
        if shuffle:
            query += " ORDER BY RANDOM()"
            
        query += f" LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        questions = []
        for row in rows:
            # Select appropriate language version
            question_text = self._get_localized_text(row, 'question', language)
            options = self._get_localized_options(row, language)
            
            question = {
                'id': row['id'],
                'question': question_text,
                'options': options,
                'correct_answer': row['correct_answer'],
                'difficulty': row['difficulty'],
                'category': row['category'],
                'subject': row['subject'] if 'subject' in row.keys() else row['category'],
                'field': row['field'] if 'field' in row.keys() else 'general',
                'points': row['points'] if 'points' in row.keys() else 10,
                'language': row['language'] if 'language' in row.keys() else 'en',
                'explanation': row['explanation'] if 'explanation' in row.keys() else '',
                'tags': self._parse_tags(row.get('tags', '[]'))
            }
            questions.append(question)
            
        return questions
        
    def _get_localized_text(self, row, field_prefix: str, language: str) -> str:
        """Get localized text for a given field and language."""
        if language == 'en' or not language:
            return row[f'{field_prefix}_text']
            
        localized_field = f'{field_prefix}_{language}'
        if localized_field in row.keys() and row[localized_field]:
            return row[localized_field]
            
        # Fallback to English
        return row[f'{field_prefix}_text']
        
    def _get_localized_options(self, row, language: str) -> List[str]:
        """Get localized options for a given language."""
        if language == 'en' or not language:
            return [row['option_a'], row['option_b'], row['option_c'], row['option_d']]
            
        options_field = f'options_{language}'
        if options_field in row.keys() and row[options_field]:
            try:
                import json
                localized_options = json.loads(row[options_field])
                if len(localized_options) == 4:
                    return localized_options
            except (json.JSONDecodeError, TypeError):
                pass
                
        # Fallback to English options
        return [row['option_a'], row['option_b'], row['option_c'], row['option_d']]
        
    def _parse_tags(self, tags_json: str) -> List[str]:
        """Parse tags from JSON string."""
        try:
            import json
            return json.loads(tags_json) if tags_json else []
        except (json.JSONDecodeError, TypeError):
            return []
        
    def add_score(self, player_name: str, score: int, total_questions: int,
                  time_taken: int, difficulty: str = "medium", 
                  points_earned: int = 0, category: str = "all", 
                  language: str = "en", achievements: List[str] = None) -> int:
        """
        Add a new score to the leaderboard with enhanced features.
        
        Args:
            player_name (str): Name of the player
            score (int): Number of correct answers
            total_questions (int): Total number of questions attempted
            time_taken (int): Time taken in seconds
            difficulty (str): Quiz difficulty level
            points_earned (int): Total points earned
            category (str): Quiz category
            language (str): Quiz language
            achievements (List[str]): List of achievements earned
            
        Returns:
            int: ID of the inserted score record
        """
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        achievements_json = json.dumps(achievements or [])
        
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO leaderboard 
            (player_name, score, total_questions, percentage, points_earned, 
             time_taken, difficulty, category, language, achievements)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (player_name, score, total_questions, percentage, points_earned,
              time_taken, difficulty, category, language, achievements_json))
        
        self.connection.commit()
        
        # Check and award achievements
        self._check_achievements(player_name, score, total_questions, percentage, points_earned)
        
        return cursor.lastrowid
        
    def _check_achievements(self, player_name: str, score: int, total_questions: int, 
                           percentage: float, points_earned: int):
        """Check and award achievements based on performance."""
        achievements_to_award = []
        
        # Perfect score achievement
        if percentage == 100.0:
            achievements_to_award.append(("perfect_score", "Perfect Score", "Answered all questions correctly!"))
            
        # High scorer achievement
        if percentage >= 90.0:
            achievements_to_award.append(("high_scorer", "High Scorer", "Scored 90% or higher!"))
            
        # Speed demon achievement (assuming average time per question < 15 seconds)
        if total_questions > 0 and (points_earned / total_questions) > 15:
            achievements_to_award.append(("speed_demon", "Speed Demon", "Answered quickly and accurately!"))
            
        # Award achievements
        cursor = self.connection.cursor()
        for achievement_type, name, description in achievements_to_award:
            # Check if already awarded
            cursor.execute(
                "SELECT COUNT(*) FROM achievements WHERE user_name = ? AND achievement_type = ?",
                (player_name, achievement_type)
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO achievements (user_name, achievement_type, achievement_name, description) VALUES (?, ?, ?, ?)",
                    (player_name, achievement_type, name, description)
                )
                
        self.connection.commit()
        
    def get_leaderboard(self, limit: int = 10, difficulty: str = None) -> List[Dict]:
        """
        Get leaderboard entries.
        
        Args:
            limit (int): Maximum number of entries to retrieve
            difficulty (str): Filter by difficulty level
            
        Returns:
            List[Dict]: List of leaderboard entries
        """
        cursor = self.connection.cursor()
        
        query = '''
            SELECT player_name, score, total_questions, percentage, 
                   time_taken, difficulty, date_played
            FROM leaderboard
        '''
        
        params = []
        if difficulty:
            query += " WHERE difficulty = ?"
            params.append(difficulty)
            
        query += " ORDER BY percentage DESC, score DESC, time_taken ASC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        leaderboard = []
        for i, row in enumerate(rows, 1):
            entry = {
                'rank': i,
                'player_name': row['player_name'],
                'score': row['score'],
                'total_questions': row['total_questions'],
                'percentage': row['percentage'],
                'time_taken': row['time_taken'],
                'difficulty': row['difficulty'],
                'date_played': row['date_played']
            }
            leaderboard.append(entry)
            
        return leaderboard
        
    def clear_leaderboard(self):
        """Clear all leaderboard entries."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM leaderboard")
        self.connection.commit()
        
    def get_categories(self) -> List[str]:
        """Get all available question categories."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT category FROM questions ORDER BY category")
        rows = cursor.fetchall()
        return [row['category'] for row in rows]
        
    def get_difficulties(self) -> List[str]:
        """Get all available difficulty levels."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT difficulty FROM questions ORDER BY difficulty")
        rows = cursor.fetchall()
        return [row['difficulty'] for row in rows]
        
    def get_subjects(self) -> List[str]:
        """Get all available question subjects."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT subject FROM questions WHERE subject IS NOT NULL ORDER BY subject")
        rows = cursor.fetchall()
        return [row['subject'] for row in rows]
        
    def get_fields(self) -> List[str]:
        """Get all available question fields."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT field FROM questions WHERE field IS NOT NULL ORDER BY field")
        rows = cursor.fetchall()
        return [row['field'] for row in rows]
        
    def get_available_categories(self) -> List[Dict]:
        """Get all available categories with details."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY display_name")
        rows = cursor.fetchall()
        
        categories = []
        for row in rows:
            category = {
                'name': row['name'],
                'display_name': row['display_name'],
                'description': row['description']
            }
            categories.append(category)
            
        return categories
        
    def get_languages(self) -> List[str]:
        """Get all available question languages."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT language FROM questions WHERE language IS NOT NULL ORDER BY language")
        rows = cursor.fetchall()
        return [row['language'] for row in rows]
        
    def get_question_stats(self) -> Dict:
        """Get statistics about questions in the database."""
        cursor = self.connection.cursor()
        
        stats = {}
        
        # Total questions
        cursor.execute("SELECT COUNT(*) FROM questions")
        stats['total_questions'] = cursor.fetchone()[0]
        
        # Questions by difficulty
        cursor.execute("SELECT difficulty, COUNT(*) FROM questions GROUP BY difficulty")
        stats['by_difficulty'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Questions by category
        cursor.execute("SELECT category, COUNT(*) FROM questions GROUP BY category")
        stats['by_category'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Questions by language
        cursor.execute("SELECT language, COUNT(*) FROM questions GROUP BY language")
        stats['by_language'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        return stats
        
    def export_leaderboard_csv(self, filename: str = "leaderboard.csv") -> bool:
        """
        Export leaderboard to CSV file.
        
        Args:
            filename (str): Output filename
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            import csv
            
            leaderboard = self.get_leaderboard(limit=100)  # Get all entries
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['rank', 'player_name', 'score', 'total_questions', 
                            'percentage', 'time_taken', 'difficulty', 'date_played']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for entry in leaderboard:
                    writer.writerow(entry)
                    
            return True
        except Exception as e:
            print(f"Error exporting leaderboard: {e}")
            return False
            
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            
    def __del__(self):
        """Destructor to ensure database connection is closed."""
        self.close()


# Test functions for development
if __name__ == "__main__":
    # Test the database manager
    db = DatabaseManager("test_quiz.db")
    
    print("Testing DatabaseManager...")
    
    # Test getting questions
    questions = db.get_questions(5)
    print(f"Retrieved {len(questions)} questions")
    
    # Test adding a score
    score_id = db.add_score("Test Player", 8, 10, 120)
    print(f"Added score with ID: {score_id}")
    
    # Test leaderboard
    leaderboard = db.get_leaderboard(5)
    print(f"Leaderboard entries: {len(leaderboard)}")
    
    # Cleanup
    db.close()
    if os.path.exists("test_quiz.db"):
        os.remove("test_quiz.db")
    
    print("Database tests completed successfully!")
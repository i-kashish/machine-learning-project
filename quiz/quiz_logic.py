#!/usr/bin/env python3
"""
Quiz Logic for Quiz Master Application
Handles quiz flow, scoring, and question management.

Author: Qoder AI Assistant
Date: 2025-08-26
"""

import random
import time
from typing import List, Dict, Optional, Callable
from datetime import datetime


class QuizSession:
    """
    Manages a single quiz session including questions, scoring, timing, and achievements.
    """
    
    def __init__(self, questions: List[Dict], time_per_question: int = 30, 
                 language: str = 'en', category: str = 'all'):
        """
        Initialize a quiz session.
        
        Args:
            questions (List[Dict]): List of question dictionaries
            time_per_question (int): Time limit per question in seconds
            language (str): Selected language for the quiz
            category (str): Selected category for the quiz
        """
        self.questions = questions.copy()
        self.time_per_question = time_per_question
        self.language = language
        self.category = category
        self.current_question_index = 0
        self.score = 0
        self.total_points = 0
        self.max_possible_points = sum(q.get('points', 10) for q in questions)
        self.answers = []  # Store user answers
        self.start_time = None
        self.end_time = None
        self.question_start_time = None
        self.is_active = False
        self.achievements = []
        
        # Shuffle questions and options for each question
        self.shuffle_quiz()
        
    def shuffle_quiz(self):
        """Shuffle questions and answer options within each question."""
        # Shuffle question order
        random.shuffle(self.questions)
        
        # Shuffle options within each question while maintaining correct answer
        for question in self.questions:
            options = question['options'].copy()
            correct_index = ord(question['correct_answer']) - ord('A')
            correct_option = options[correct_index]
            
            # Shuffle options
            random.shuffle(options)
            
            # Update correct answer to match new position
            new_correct_index = options.index(correct_option)
            question['correct_answer'] = chr(ord('A') + new_correct_index)
            question['options'] = options
            
    def start_quiz(self):
        """Start the quiz session."""
        self.start_time = time.time()
        self.question_start_time = time.time()
        self.is_active = True
        
    def get_current_question(self) -> Optional[Dict]:
        """
        Get the current question.
        
        Returns:
            Dict or None: Current question dictionary or None if quiz is complete
        """
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
        
    def get_progress(self) -> Dict:
        """
        Get quiz progress information.
        
        Returns:
            Dict: Progress information including current question number, total questions, points, etc.
        """
        return {
            'current': self.current_question_index + 1,
            'total': len(self.questions),
            'percentage': ((self.current_question_index) / len(self.questions)) * 100,
            'score': self.score,
            'total_points': self.total_points,
            'max_possible_points': self.max_possible_points,
            'questions_remaining': len(self.questions) - self.current_question_index,
            'achievements': self.achievements.copy()
        }
        
    def get_time_remaining(self) -> int:
        """
        Get remaining time for current question in seconds.
        
        Returns:
            int: Seconds remaining for current question
        """
        if not self.is_active or not self.question_start_time:
            return 0
            
        elapsed = time.time() - self.question_start_time
        remaining = max(0, self.time_per_question - elapsed)
        return int(remaining)
        
    def submit_answer(self, answer: str) -> Dict:
        """
        Submit an answer for the current question.
        
        Args:
            answer (str): User's answer (A, B, C, or D)
            
        Returns:
            Dict: Result information including correctness, correct answer, points earned, etc.
        """
        if not self.is_active or self.current_question_index >= len(self.questions):
            return {'error': 'No active question to answer'}
            
        current_question = self.questions[self.current_question_index]
        is_correct = answer == current_question['correct_answer']
        points_earned = 0
        
        if is_correct:
            self.score += 1
            points_earned = current_question.get('points', 10)
            self.total_points += points_earned
            
            # Check for speed bonus (if answered in less than 10 seconds)
            time_taken = time.time() - self.question_start_time if self.question_start_time else 0
            if time_taken < 10:
                speed_bonus = int(points_earned * 0.2)  # 20% bonus for quick answers
                points_earned += speed_bonus
                self.total_points += speed_bonus
                
        # Store answer information
        answer_info = {
            'question_index': self.current_question_index,
            'question': current_question['question'],
            'user_answer': answer,
            'correct_answer': current_question['correct_answer'],
            'is_correct': is_correct,
            'points_earned': points_earned,
            'time_taken': time.time() - self.question_start_time if self.question_start_time else 0,
            'options': current_question['options'].copy(),
            'explanation': current_question.get('explanation', '')
        }
        
        self.answers.append(answer_info)
        
        # Check for achievements
        self._check_question_achievements(is_correct, answer_info['time_taken'])
        
        # Move to next question
        self.current_question_index += 1
        
        # Reset question timer if not at end
        if self.current_question_index < len(self.questions):
            self.question_start_time = time.time()
        else:
            self.end_quiz()
            
        return {
            'is_correct': is_correct,
            'correct_answer': current_question['correct_answer'],
            'correct_option': current_question['options'][ord(current_question['correct_answer']) - ord('A')],
            'user_option': current_question['options'][ord(answer) - ord('A')] if answer in 'ABCD' else 'No answer',
            'points_earned': points_earned,
            'explanation': current_question.get('explanation', self._get_explanation(current_question, is_correct)),
            'quiz_complete': self.current_question_index >= len(self.questions),
            'achievements': self.achievements.copy()
        }
        
    def auto_submit(self) -> Dict:
        """
        Auto-submit when time runs out (no answer selected).
        
        Returns:
            Dict: Result information
        """
        return self.submit_answer('X')  # X represents no answer
        
    def end_quiz(self):
        """End the quiz session."""
        self.end_time = time.time()
        self.is_active = False
        
    def get_total_time(self) -> int:
        """
        Get total time taken for the quiz in seconds.
        
        Returns:
            int: Total time in seconds
        """
        if self.start_time and self.end_time:
            return int(self.end_time - self.start_time)
        elif self.start_time:
            return int(time.time() - self.start_time)
        return 0
        
    def get_final_results(self) -> Dict:
        """
        Get comprehensive quiz results.
        
        Returns:
            Dict: Complete results including score, time, detailed answers, achievements
        """
        total_questions = len(self.questions)
        percentage = (self.score / total_questions * 100) if total_questions > 0 else 0
        points_percentage = (self.total_points / self.max_possible_points * 100) if self.max_possible_points > 0 else 0
        
        # Check final achievements
        self._check_final_achievements(percentage)
        
        return {
            'score': self.score,
            'total_questions': total_questions,
            'percentage': round(percentage, 1),
            'points_earned': self.total_points,
            'max_possible_points': self.max_possible_points,
            'points_percentage': round(points_percentage, 1),
            'total_time': self.get_total_time(),
            'answers': self.answers.copy(),
            'average_time_per_question': round(self.get_total_time() / total_questions, 1) if total_questions > 0 else 0,
            'correct_answers': [ans for ans in self.answers if ans['is_correct']],
            'incorrect_answers': [ans for ans in self.answers if not ans['is_correct']],
            'grade': self._calculate_grade(percentage),
            'achievements': self.achievements.copy(),
            'language': self.language,
            'category': self.category,
            'performance_rating': self._calculate_performance_rating(percentage, points_percentage)
        }
        
    def _check_question_achievements(self, is_correct: bool, time_taken: float):
        """Check for achievements after each question."""
        if is_correct and time_taken < 5:
            if "Lightning Fast" not in self.achievements:
                self.achievements.append("Lightning Fast")
                
    def _check_final_achievements(self, percentage: float):
        """Check for final achievements based on overall performance."""
        if percentage == 100.0 and "Perfect Score" not in self.achievements:
            self.achievements.append("Perfect Score")
        elif percentage >= 90.0 and "Quiz Master" not in self.achievements:
            self.achievements.append("Quiz Master")
        elif percentage >= 80.0 and "Scholar" not in self.achievements:
            self.achievements.append("Scholar")
            
        # Streak achievements
        correct_streak = 0
        max_streak = 0
        for answer in self.answers:
            if answer['is_correct']:
                correct_streak += 1
                max_streak = max(max_streak, correct_streak)
            else:
                correct_streak = 0
                
        if max_streak >= 5 and "Hot Streak" not in self.achievements:
            self.achievements.append("Hot Streak")
            
    def _calculate_performance_rating(self, percentage: float, points_percentage: float) -> str:
        """Calculate overall performance rating."""
        combined_score = (percentage + points_percentage) / 2
        
        if combined_score >= 95:
            return "Outstanding"
        elif combined_score >= 85:
            return "Excellent"
        elif combined_score >= 75:
            return "Good"
        elif combined_score >= 65:
            return "Fair"
        else:
            return "Needs Improvement"
        
    def _get_explanation(self, question: Dict, is_correct: bool) -> str:
        """
        Get explanation for the answer (placeholder for future enhancement).
        
        Args:
            question (Dict): Question dictionary
            is_correct (bool): Whether the answer was correct
            
        Returns:
            str: Explanation text
        """
        if is_correct:
            return "Correct! Well done!"
        else:
            correct_option = question['options'][ord(question['correct_answer']) - ord('A')]
            return f"Incorrect. The correct answer is: {correct_option}"
            
    def _calculate_grade(self, percentage: float) -> str:
        """
        Calculate letter grade based on percentage.
        
        Args:
            percentage (float): Percentage score
            
        Returns:
            str: Letter grade
        """
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"


class QuizManager:
    """
    High-level quiz management class that coordinates quiz sessions.
    """
    
    def __init__(self, database_manager):
        """
        Initialize quiz manager.
        
        Args:
            database_manager: Database manager instance
        """
        self.db_manager = database_manager
        self.current_session = None
        self.difficulty_settings = {
            'easy': {'time_per_question': 45, 'num_questions': 8},
            'medium': {'time_per_question': 30, 'num_questions': 10},
            'hard': {'time_per_question': 20, 'num_questions': 12}
        }
        
    def create_quiz(self, difficulty: str = 'medium', category: str = None, 
                   num_questions: int = None, time_per_question: int = None,
                   language: str = 'en', subject: str = None, field: str = None) -> QuizSession:
        """
        Create a new quiz session with advanced options.
        
        Args:
            difficulty (str): Quiz difficulty level
            category (str): Question category filter
            num_questions (int): Number of questions (overrides difficulty default)
            time_per_question (int): Time per question (overrides difficulty default)
            language (str): Preferred language for questions
            subject (str): Specific subject filter
            field (str): Specific field filter
            
        Returns:
            QuizSession: New quiz session instance
        """
        # Get difficulty settings
        settings = self.difficulty_settings.get(difficulty, self.difficulty_settings['medium'])
        
        # Override with custom settings if provided
        final_num_questions = num_questions or settings['num_questions']
        final_time_per_question = time_per_question or settings['time_per_question']
        
        # Get questions from database with enhanced filtering
        questions = self.db_manager.get_questions(
            limit=final_num_questions,
            difficulty=difficulty,
            category=category,
            shuffle=True,
            language=language,
            subject=subject,
            field=field
        )
        
        if not questions:
            raise ValueError(f"No questions found for the specified criteria")
            
        # Create new session with advanced features
        self.current_session = QuizSession(
            questions, 
            final_time_per_question,
            language=language,
            category=category or 'all'
        )
        return self.current_session
        
    def get_current_session(self) -> Optional[QuizSession]:
        """
        Get the current active quiz session.
        
        Returns:
            QuizSession or None: Current session or None if no active session
        """
        return self.current_session
        
    def save_results(self, player_name: str, session: QuizSession) -> int:
        """
        Save quiz results to the database with enhanced features.
        
        Args:
            player_name (str): Player's name
            session (QuizSession): Completed quiz session
            
        Returns:
            int: Score ID in database
        """
        results = session.get_final_results()
        
        return self.db_manager.add_score(
            player_name=player_name,
            score=results['score'],
            total_questions=results['total_questions'],
            time_taken=results['total_time'],
            points_earned=results['points_earned'],
            category=results['category'],
            language=results['language'],
            achievements=results['achievements']
        )
        
    def get_statistics(self) -> Dict:
        """
        Get quiz statistics and metrics.
        
        Returns:
            Dict: Statistics information
        """
        try:
            # Get basic stats from database
            leaderboard = self.db_manager.get_leaderboard(limit=100)  # Get more entries for stats
            
            if not leaderboard:
                return {
                    'total_games': 0,
                    'average_score': 0,
                    'highest_score': 0,
                    'average_percentage': 0,
                    'total_players': 0
                }
                
            total_games = len(leaderboard)
            total_score = sum(entry['score'] for entry in leaderboard)
            total_percentage = sum(entry['percentage'] for entry in leaderboard)
            unique_players = len(set(entry['player_name'] for entry in leaderboard))
            highest_score = max(entry['score'] for entry in leaderboard)
            
            return {
                'total_games': total_games,
                'average_score': round(total_score / total_games, 1) if total_games > 0 else 0,
                'highest_score': highest_score,
                'average_percentage': round(total_percentage / total_games, 1) if total_games > 0 else 0,
                'total_players': unique_players,
                'top_player': leaderboard[0]['player_name'] if leaderboard else 'None'
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_games': 0,
                'average_score': 0,
                'highest_score': 0,
                'average_percentage': 0,
                'total_players': 0,
                'error': str(e)
            }
            
    def get_available_categories(self) -> List[Dict]:
        """Get available question categories."""
        try:
            return self.db_manager.get_available_categories()
        except Exception:
            return []
            
    def get_available_languages(self) -> List[str]:
        """Get available question languages."""
        try:
            return self.db_manager.get_languages()
        except Exception:
            return ['en']
            
    def get_available_subjects(self) -> List[str]:
        """Get available question subjects."""
        try:
            return self.db_manager.get_subjects()
        except Exception:
            return []
            
    def get_available_fields(self) -> List[str]:
        """Get available question fields."""
        try:
            return self.db_manager.get_fields()
        except Exception:
            return []
            
    def get_question_statistics(self) -> Dict:
        """Get detailed question statistics."""
        try:
            return self.db_manager.get_question_stats()
        except Exception as e:
            print(f"Error getting question statistics: {e}")
            return {}


# Utility functions for scoring and validation
def validate_answer(answer: str) -> bool:
    """
    Validate if an answer is in the correct format.
    
    Args:
        answer (str): Answer to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return answer in ['A', 'B', 'C', 'D']


def format_time(seconds: int) -> str:
    """
    Format time in seconds to MM:SS format.
    
    Args:
        seconds (int): Time in seconds
        
    Returns:
        str: Formatted time string
    """
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def calculate_performance_rating(percentage: float, time_ratio: float = 1.0) -> str:
    """
    Calculate performance rating based on score and time efficiency.
    
    Args:
        percentage (float): Score percentage
        time_ratio (float): Time efficiency ratio (1.0 = average time)
        
    Returns:
        str: Performance rating
    """
    # Adjust score based on time efficiency
    adjusted_score = percentage * (2.0 - time_ratio) if time_ratio <= 1.0 else percentage * (1.0 / time_ratio)
    
    if adjusted_score >= 95:
        return "Excellent"
    elif adjusted_score >= 85:
        return "Very Good"
    elif adjusted_score >= 75:
        return "Good"
    elif adjusted_score >= 65:
        return "Fair"
    else:
        return "Needs Improvement"


# Test function for development
if __name__ == "__main__":
    print("Testing Quiz Logic...")
    
    # Create sample questions for testing
    sample_questions = [
        {
            'id': 1,
            'question': 'What is 2 + 2?',
            'options': ['3', '4', '5', '6'],
            'correct_answer': 'B',
            'difficulty': 'easy',
            'category': 'math'
        },
        {
            'id': 2,
            'question': 'What is the capital of France?',
            'options': ['London', 'Berlin', 'Paris', 'Madrid'],
            'correct_answer': 'C',
            'difficulty': 'easy',
            'category': 'geography'
        }
    ]
    
    # Test quiz session
    session = QuizSession(sample_questions, 30)
    session.start_quiz()
    
    print(f"Current question: {session.get_current_question()['question']}")
    print(f"Progress: {session.get_progress()}")
    
    # Submit an answer
    result = session.submit_answer('B')
    print(f"Answer result: {result}")
    
    print("Quiz logic tests completed successfully!")
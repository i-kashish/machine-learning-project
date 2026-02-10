# 🎯 Quiz Master - Interactive Python Quiz Application

A comprehensive GUI quiz application built with Python and Tkinter, featuring dynamic question loading, real-time scoring, and leaderboard functionality.

## 🚀 Features

### Core Functionality
- **Interactive GUI**: Clean, responsive interface using Tkinter and ttk widgets
- **Dynamic Questions**: Load questions from SQLite database with shuffling
- **Multiple Difficulty Levels**: Easy, Medium, and Hard with different time limits
- **Real-time Timer**: Countdown timer for each question with auto-submit
- **Progress Tracking**: Visual progress bar and score display
- **Comprehensive Results**: Detailed results with answer review

### Scoring System
- **Real-time Scoring**: Track correct answers and percentages
- **Performance Grading**: Letter grades based on percentage scores
- **Time Tracking**: Monitor time per question and total quiz time
- **Detailed Analysis**: Review all answers with explanations

### Leaderboard Features
- **SQLite Database**: Persistent storage for scores and questions
- **Top Players**: Display top 5 (or more) players with filtering
- **Difficulty Filtering**: Filter leaderboard by difficulty level
- **Export Functionality**: Export leaderboard to CSV format
- **Statistics Dashboard**: Overall quiz statistics and metrics

### User Experience
- **Keyboard Shortcuts**: Use keys 1-4 to select options, Enter to submit
- **Visual Feedback**: Color-coded timer and immediate answer feedback
- **Customizable Settings**: Choose difficulty and number of questions
- **Result Export**: Export individual quiz results to text files

## 📁 Project Structure

```
quiz/
├── main.py              # Application entry point
├── ui_manager.py        # Tkinter UI components and screens
├── quiz_logic.py        # Quiz session management and scoring
├── database.py          # SQLite database operations
├── sample_questions.json # Sample questions for reference
├── quiz_master.db       # SQLite database (created automatically)
└── README.md           # This documentation file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Tkinter (usually included with Python)
- SQLite3 (included with Python)

### Quick Start
1. **Clone or download** all files to a directory
2. **Navigate** to the project directory
3. **Run** the application:
   ```bash
   python main.py
   ```

### Dependencies
All dependencies are part of Python's standard library:
- `tkinter` - GUI framework
- `sqlite3` - Database operations
- `threading` - Timer functionality
- `json` - Configuration and data handling
- `csv` - Export functionality
- `time` - Timing and formatting

## 🎮 How to Use

### Starting a Quiz
1. **Launch** the application by running `python main.py`
2. **Enter your name** in the welcome screen
3. **Select difficulty level**:
   - Easy: 8 questions, 45 seconds each
   - Medium: 10 questions, 30 seconds each
   - Hard: 12 questions, 20 seconds each
4. **Click "Start Quiz"** to begin

### During the Quiz
- **Read the question** and select one of four options (A, B, C, D)
- **Use keyboard shortcuts**: Press 1, 2, 3, or 4 to select options
- **Watch the timer**: Red indicates low time, orange is warning, green is safe
- **Submit answer**: Click "Submit Answer" or press Enter
- **Skip question**: Click "Skip Question" if needed

### After the Quiz
- **Review results**: See your score, percentage, and grade
- **Detailed analysis**: Review each question with correct answers
- **View leaderboard**: Check your ranking against other players
- **Export results**: Save your quiz results to a text file

### Leaderboard Management
- **View rankings**: Click "View Leaderboard" from any screen
- **Filter results**: Filter by difficulty level
- **Export data**: Export leaderboard to CSV format
- **Clear data**: Reset all leaderboard entries (with confirmation)

## 🔧 Customization

### Adding New Questions
Questions are stored in the SQLite database. To add new questions:

1. **Manually via database**: Use any SQLite browser to edit `quiz_master.db`
2. **Programmatically**: Use the `DatabaseManager.add_question()` method
3. **JSON import**: Create a JSON file and import using database methods

### Question Format
```python
{
    "question_text": "Your question here?",
    "option_a": "First option",
    "option_b": "Second option", 
    "option_c": "Third option",
    "option_d": "Fourth option",
    "correct_answer": "B",  # A, B, C, or D
    "difficulty": "medium",  # easy, medium, hard
    "category": "science"    # any category
}
```

### Modifying Difficulty Settings
Edit the `difficulty_settings` in `quiz_logic.py`:
```python
self.difficulty_settings = {
    'easy': {'time_per_question': 45, 'num_questions': 8},
    'medium': {'time_per_question': 30, 'num_questions': 10},
    'hard': {'time_per_question': 20, 'num_questions': 12}
}
```

## 🎨 Features Breakdown

### Timer System
- **Countdown display**: Shows remaining seconds
- **Color coding**: Green (safe) → Orange (warning) → Red (danger)
- **Auto-submit**: Automatically submits when time expires
- **Thread-safe**: Uses separate thread for smooth operation

### Database Schema
- **Questions table**: Stores all quiz questions with metadata
- **Leaderboard table**: Records player scores and statistics
- **Automatic initialization**: Creates tables and sample data on first run

### UI Components
- **Welcome screen**: Player registration and difficulty selection
- **Quiz interface**: Question display, options, timer, and progress
- **Results screen**: Comprehensive score display and answer review
- **Leaderboard window**: Rankings with filtering and export options
- **Statistics dashboard**: Overall quiz metrics and performance data

## 🐛 Troubleshooting

### Common Issues

**Application won't start**
- Ensure Python 3.7+ is installed
- Check that all files are in the same directory
- Verify Tkinter is available: `python -c "import tkinter"`

**Database errors**
- Delete `quiz_master.db` to reset the database
- Check file permissions in the project directory
- Ensure SQLite3 is available

**Timer issues**
- Close and restart the application
- Check for multiple instances running
- Verify threading support

**Import errors**
- Ensure all Python files are in the same directory
- Check file names match exactly (case-sensitive on some systems)
- Verify Python path includes current directory

## 📊 Performance Features

### Scoring Metrics
- **Percentage calculation**: (Correct answers / Total questions) × 100
- **Time efficiency**: Average time per question tracking
- **Performance rating**: Based on accuracy and speed
- **Grade assignment**: A (90%+), B (80-89%), C (70-79%), D (60-69%), F (<60%)

### Statistics Tracking
- Total games played across all users
- Average scores and percentages
- Unique player count
- Top performer identification
- Historical data retention

## 🔒 Data Storage

### Database Security
- Local SQLite database for privacy
- No external connections required
- Automatic backup capabilities
- Data export options for portability

### Export Formats
- **Leaderboard**: CSV format with all player data
- **Individual results**: Text format with detailed breakdown
- **Timestamps**: All records include date/time information

## 🎯 Future Enhancements

### Potential Additions
- **Sound effects**: Audio feedback for correct/incorrect answers
- **Categories**: Question filtering by subject area
- **Multiplayer**: Network-based competitive quizzes
- **Themes**: Customizable visual themes
- **Adaptive difficulty**: AI-based question selection
- **Achievement system**: Badges and rewards for milestones

### Technical Improvements
- **Question bank expansion**: Support for larger question databases
- **Image questions**: Support for visual questions
- **Explanation system**: Detailed answer explanations
- **Progress saving**: Resume interrupted quizzes
- **User profiles**: Personal statistics and preferences

## 📝 License

This project is created for educational and personal use. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create your feature branch
3. Test thoroughly
4. Submit a pull request

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review the code comments for implementation details
- Test with the provided sample data first

---

**Quiz Master** - Making learning interactive and fun! 🎓✨
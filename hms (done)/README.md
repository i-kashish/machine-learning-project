# Hospital Management System

A comprehensive GUI-based Hospital Management System built with Python Tkinter and SQLite database.

## Features

### 1. Patient Registration Module
- Add new patients with details: Name, Age, Gender, Contact, Address, Disease/Problem, Admission Date
- Edit/Update patient records
- Delete patient records
- Store patient data in SQLite database

### 2. Doctor Management Module
- Maintain doctor details (Name, Specialty, Availability)
- Add, update, and delete doctor records

### 3. Appointment Module
- Book appointments for patients
- Assign doctors to patients
- Display appointment schedule
- Search appointments by Doctor, Date, or Patient

### 4. Billing System
- Generate bills for patients (consultation fee, medicine charges, room charges, other expenses)
- Show bill summary in Tkinter window
- Option to print/save bill (placeholder functionality)
- Payment tracking with status (Paid/Unpaid/Pending) and methods (Cash/Online/Bank Transfer/Cheque)

### 5. Doctor Salary Management
- Generate and manage doctor salaries
- Track payment status and methods
- Monthly salary tracking

### 6. Search & Filter
- Search patients by Name, ID, Disease, or Admission Date
- Search appointments by Doctor, Date, or Patient
- Search bills and salaries by various criteria
- Display results in Tkinter Treeview tables

### 7. Reports Module
- Generate daily/monthly reports:
  - Total patients admitted
  - Total appointments
  - Revenue generated (in Indian Rupees ₹)
- Payment status and method breakdown
- Doctor salary reports
- Export reports (placeholder functionality)

### 8. Financial Overview
- Comprehensive financial dashboard
- Billing and salary summaries
- Net financial position calculation

## Technical Details

### Technologies Used
- **Frontend**: Python Tkinter
- **Backend**: SQLite Database
- **Currency**: Indian Rupees (₹)
- **Python Version**: 3.6 or higher

### Database Schema
The system uses SQLite with the following tables:
1. `patients` - Stores patient information
2. `doctors` - Stores doctor information
3. `appointments` - Stores appointment details
4. `billing` - Stores billing information with payment tracking
5. `doctor_salary` - Stores doctor salary information

## Installation

1. Ensure you have Python 3.6 or higher installed
2. No additional packages are required (uses only standard library modules)
3. Clone or download this repository
4. Run the application with: `python main.py`

## Usage

1. Run the application: `python main.py`
2. Use the navigation menu at the top to switch between modules:
   - **Patient**: Manage patient records
   - **Doctor**: Manage doctor records
   - **Appointment**: Book and manage appointments
   - **Billing**: Generate and manage patient bills
   - **Salary**: Manage doctor salaries
   - **Financial**: View financial overview and detailed reports
   - **Reports**: Generate daily and monthly reports
3. Each module has intuitive forms and search functionality
4. All financial amounts are displayed in Indian Rupees (₹)

## Project Structure

```
hospital-management-system/
├── main.py              # Main application entry point
├── patient_module.py    # Patient management functionality
├── doctor_module.py     # Doctor management functionality
├── appointment_module.py# Appointment booking functionality
├── billing_module.py    # Billing system functionality
├── salary_module.py     # Doctor salary management functionality
├── financial_module.py  # Financial overview functionality
├── report_module.py     # Reporting functionality
├── hospital.db          # SQLite database (created automatically)
├── requirements.txt     # Project requirements
└── README.md           # This file
```

## Implementation Notes

- All data is stored in a local SQLite database file (`hospital.db`)
- The database is automatically created on first run
- Input validation is implemented for all forms
- Error handling is included throughout the application
- The code is modular and well-commented for maintainability
- All financial amounts are displayed in Indian Rupees (₹)

## Future Enhancements

- Implement actual PDF/Excel export functionality
- Add user authentication and roles
- Implement data backup and restore features
- Add more advanced reporting capabilities
- Improve UI/UX with custom themes

## License

This project is open source and available under the MIT License.
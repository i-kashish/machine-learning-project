import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

# Import modules
from patient_module import PatientModule
from doctor_module import DoctorModule
from appointment_module import AppointmentModule
from billing_module import BillingModule
from report_module import ReportModule
from salary_module import SalaryModule
from financial_module import FinancialModule


class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Create database if not exists
        self.create_database()
        
        # Create main frames
        self.create_main_menu()
        self.create_content_frame()
        
        # Initialize modules
        self.patient_module = PatientModule(self.content_frame, self.db_conn)
        self.doctor_module = DoctorModule(self.content_frame, self.db_conn)
        self.appointment_module = AppointmentModule(self.content_frame, self.db_conn)
        self.billing_module = BillingModule(self.content_frame, self.db_conn)
        self.report_module = ReportModule(self.content_frame, self.db_conn)
        self.salary_module = SalaryModule(self.content_frame, self.db_conn)
        self.financial_module = FinancialModule(self.content_frame, self.db_conn)
        
        # Show default module
        self.show_module("patient")
        
    def create_database(self):
        """Create SQLite database and tables if they don't exist"""
        self.db_conn = sqlite3.connect('hospital.db')
        cursor = self.db_conn.cursor()
        
        # Create patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                contact TEXT NOT NULL,
                address TEXT NOT NULL,
                disease TEXT NOT NULL,
                admission_date TEXT NOT NULL
            )
        ''')
        
        # Create doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                availability TEXT NOT NULL
            )
        ''')
        
        # Create appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                status TEXT DEFAULT 'Scheduled',
                FOREIGN KEY (patient_id) REFERENCES patients (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')
        
        # Check if billing table exists and has the old schema
        cursor.execute("PRAGMA table_info(billing)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        if not columns:
            # Create new billing table with updated schema
            cursor.execute('''
                CREATE TABLE billing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    consultation_fee REAL DEFAULT 0,
                    medicine_charges REAL DEFAULT 0,
                    room_charges_per_day REAL DEFAULT 0,
                    number_of_days INTEGER DEFAULT 1,
                    other_charges REAL DEFAULT 0,
                    total_amount REAL DEFAULT 0,
                    billing_date TEXT NOT NULL,
                    payment_status TEXT DEFAULT 'Unpaid',
                    payment_method TEXT DEFAULT 'Cash',
                    payment_date TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (id)
                )
            ''')
        elif 'room_charges' in column_names and 'room_charges_per_day' not in column_names:
            # Migrate from old schema to new schema
            print("Migrating billing table schema...")
            
            # Check if there's existing data
            cursor.execute("SELECT COUNT(*) FROM billing")
            count = cursor.fetchone()[0]
            
            if count > 0:
                # Backup existing data
                cursor.execute("SELECT * FROM billing")
                billing_data = cursor.fetchall()
                
                # Drop the old table
                cursor.execute("DROP TABLE billing")
                
                # Create the new table with updated schema
                cursor.execute('''
                    CREATE TABLE billing (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        consultation_fee REAL DEFAULT 0,
                        medicine_charges REAL DEFAULT 0,
                        room_charges_per_day REAL DEFAULT 0,
                        number_of_days INTEGER DEFAULT 1,
                        other_charges REAL DEFAULT 0,
                        total_amount REAL DEFAULT 0,
                        billing_date TEXT NOT NULL,
                        payment_status TEXT DEFAULT 'Unpaid',
                        payment_method TEXT DEFAULT 'Cash',
                        payment_date TEXT,
                        FOREIGN KEY (patient_id) REFERENCES patients (id)
                    )
                ''')
                
                # Restore data (assuming room_charges was for 1 day)
                for record in billing_data:
                    # Extract values from old record
                    # Old schema: id, patient_id, consultation_fee, medicine_charges, room_charges, other_charges, total_amount, billing_date
                    old_id, patient_id, consultation_fee, medicine_charges, room_charges, other_charges, total_amount, billing_date = record
                    
                    # Insert into new table
                    cursor.execute('''
                        INSERT INTO billing (
                            id, patient_id, consultation_fee, medicine_charges, 
                            room_charges_per_day, number_of_days, other_charges, total_amount, billing_date
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (old_id, patient_id, consultation_fee, medicine_charges, room_charges, 1, other_charges, total_amount, billing_date))
            else:
                # No data, just drop and recreate
                cursor.execute("DROP TABLE billing")
                cursor.execute('''
                    CREATE TABLE billing (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        consultation_fee REAL DEFAULT 0,
                        medicine_charges REAL DEFAULT 0,
                        room_charges_per_day REAL DEFAULT 0,
                        number_of_days INTEGER DEFAULT 1,
                        other_charges REAL DEFAULT 0,
                        total_amount REAL DEFAULT 0,
                        billing_date TEXT NOT NULL,
                        payment_status TEXT DEFAULT 'Unpaid',
                        payment_method TEXT DEFAULT 'Cash',
                        payment_date TEXT,
                        FOREIGN KEY (patient_id) REFERENCES patients (id)
                    )
                ''')
        elif 'payment_status' not in column_names:
            # Add payment status columns to existing table
            print("Adding payment status columns to billing table...")
            try:
                cursor.execute("ALTER TABLE billing ADD COLUMN payment_status TEXT DEFAULT 'Unpaid'")
                cursor.execute("ALTER TABLE billing ADD COLUMN payment_method TEXT DEFAULT 'Cash'")
                cursor.execute("ALTER TABLE billing ADD COLUMN payment_date TEXT")
            except sqlite3.OperationalError:
                # Column might already exist, ignore error
                pass
        
        # Create doctor_salary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctor_salary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                salary_amount REAL DEFAULT 0,
                salary_month TEXT NOT NULL,
                salary_year TEXT NOT NULL,
                payment_date TEXT,
                payment_status TEXT DEFAULT 'Unpaid',
                payment_method TEXT DEFAULT 'Cash',
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')
        
        self.db_conn.commit()
        
    def create_main_menu(self):
        """Create the main navigation menu"""
        self.menu_frame = tk.Frame(self.root, bg="#2C3E50", height=60)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Menu buttons
        buttons = [
            ("Patient", "patient"),
            ("Doctor", "doctor"),
            ("Appointment", "appointment"),
            ("Billing", "billing"),
            ("Salary", "salary"),
            ("Financial", "financial"),
            ("Reports", "reports")
        ]
        
        for text, module in buttons:
            # Use default argument to capture the current value of module
            btn = tk.Button(
                self.menu_frame,
                text=text,
                font=("Arial", 12, "bold"),
                bg="#34495E",
                fg="white",
                relief=tk.FLAT,
                padx=20,
                pady=15,
                command=lambda m=module: self.show_module(m)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=10)
            
    def create_content_frame(self):
        """Create the main content frame"""
        self.content_frame = tk.Frame(self.root, bg="#ECF0F1")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def show_module(self, module_name):
        """Show the selected module"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Show selected module
        if module_name == "patient":
            self.patient_module.show()
        elif module_name == "doctor":
            self.doctor_module.show()
        elif module_name == "appointment":
            self.appointment_module.show()
        elif module_name == "billing":
            self.billing_module.show()
        elif module_name == "salary":
            self.salary_module.show()
        elif module_name == "financial":
            self.financial_module.show()
        elif module_name == "reports":
            self.report_module.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    root.mainloop()
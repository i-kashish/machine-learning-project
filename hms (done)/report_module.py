import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

class ReportModule:
    def __init__(self, parent, db_conn):
        self.parent = parent
        self.db_conn = db_conn
        
    def show(self):
        """Display the report module interface"""
        # Clear the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.daily_report_tab = ttk.Frame(self.notebook)
        self.monthly_report_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.daily_report_tab, text="Daily Report")
        self.notebook.add(self.monthly_report_tab, text="Monthly Report")
        
        # Setup tabs
        self.setup_daily_report_tab()
        self.setup_monthly_report_tab()
        
    def setup_daily_report_tab(self):
        """Setup the daily report tab"""
        # Main frame for daily report
        daily_frame = ttk.Frame(self.daily_report_tab, padding="20")
        daily_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(daily_frame, text="Daily Hospital Report", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Date selection
        date_frame = ttk.Frame(daily_frame)
        date_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(date_frame, text="Select Date (YYYY-MM-DD):", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.daily_date_entry = ttk.Entry(date_frame, width=20)
        self.daily_date_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        # Set today's date as default
        self.daily_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Generate report button
        generate_btn = ttk.Button(
            date_frame,
            text="Generate Report",
            command=self.generate_daily_report
        )
        generate_btn.pack(side=tk.LEFT)
        
        # Report display area
        report_frame = ttk.LabelFrame(daily_frame, text="Daily Report", padding="10")
        report_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Text widget with scrollbar for report
        text_frame = ttk.Frame(report_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.daily_report_text = tk.Text(text_frame, wrap=tk.WORD, height=20)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.daily_report_text.yview)
        self.daily_report_text.configure(yscrollcommand=scrollbar.set)
        
        self.daily_report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export button
        export_frame = ttk.Frame(daily_frame)
        export_frame.pack(fill=tk.X, pady=(10, 0))
        
        export_btn = ttk.Button(
            export_frame,
            text="Export Report (PDF/Excel)",
            command=self.export_daily_report
        )
        export_btn.pack(side=tk.RIGHT)
        
    def setup_monthly_report_tab(self):
        """Setup the monthly report tab"""
        # Main frame for monthly report
        monthly_frame = ttk.Frame(self.monthly_report_tab, padding="20")
        monthly_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(monthly_frame, text="Monthly Hospital Report", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Month/Year selection
        date_frame = ttk.Frame(monthly_frame)
        date_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(date_frame, text="Select Month/Year:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Month combobox
        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(
            date_frame,
            textvariable=self.month_var,
            values=[f"{i:02d}" for i in range(1, 13)],
            width=5,
            state="readonly"
        )
        month_combo.pack(side=tk.LEFT, padx=(10, 5))
        month_combo.set(datetime.now().strftime("%m"))
        
        # Year entry
        ttk.Label(date_frame, text="/").pack(side=tk.LEFT)
        
        self.year_entry = ttk.Entry(date_frame, width=8)
        self.year_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.year_entry.insert(0, datetime.now().strftime("%Y"))
        
        # Generate report button
        generate_btn = ttk.Button(
            date_frame,
            text="Generate Report",
            command=self.generate_monthly_report
        )
        generate_btn.pack(side=tk.LEFT)
        
        # Report display area
        report_frame = ttk.LabelFrame(monthly_frame, text="Monthly Report", padding="10")
        report_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Text widget with scrollbar for report
        text_frame = ttk.Frame(report_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.monthly_report_text = tk.Text(text_frame, wrap=tk.WORD, height=20)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.monthly_report_text.yview)
        self.monthly_report_text.configure(yscrollcommand=scrollbar.set)
        
        self.monthly_report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export button
        export_frame = ttk.Frame(monthly_frame)
        export_frame.pack(fill=tk.X, pady=(10, 0))
        
        export_btn = ttk.Button(
            export_frame,
            text="Export Report (PDF/Excel)",
            command=self.export_monthly_report
        )
        export_btn.pack(side=tk.RIGHT)
        
    def generate_daily_report(self):
        """Generate daily report for the selected date"""
        selected_date = self.daily_date_entry.get().strip()
        
        # Validate date format
        try:
            datetime.strptime(selected_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format")
            return
            
        try:
            cursor = self.db_conn.cursor()
            
            # Get total patients admitted on the selected date
            cursor.execute("SELECT COUNT(*) FROM patients WHERE admission_date = ?", (selected_date,))
            total_patients = cursor.fetchone()[0]
            
            # Get total appointments on the selected date
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", (selected_date,))
            total_appointments = cursor.fetchone()[0]
            
            # Get total revenue for the selected date
            cursor.execute('''
                SELECT SUM(total_amount) 
                FROM billing 
                WHERE billing_date = ?
            ''', (selected_date,))
            total_revenue = cursor.fetchone()[0] or 0
            
            # Generate report text
            report_text = f"""
DAILY HOSPITAL REPORT
=====================
Date: {selected_date}
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

SUMMARY:
--------
Total Patients Admitted: {total_patients}
Total Appointments: {total_appointments}
Total Revenue Generated: ₹{total_revenue:.2f}

DETAILED INFORMATION:
---------------------
1. PATIENTS ADMITTED:
"""
            
            # Get patient details
            cursor.execute("SELECT id, name, disease FROM patients WHERE admission_date = ?", (selected_date,))
            patients = cursor.fetchall()
            
            if patients:
                for patient in patients:
                    report_text += f"   - ID: {patient[0]}, Name: {patient[1]}, Disease: {patient[2]}\n"
            else:
                report_text += "   No patients admitted on this date.\n"
                
            report_text += "\n2. APPOINTMENTS:\n"
            
            # Get appointment details
            cursor.execute('''
                SELECT a.id, p.name, d.name, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                WHERE a.appointment_date = ?
                ORDER BY a.id
            ''', (selected_date,))
            appointments = cursor.fetchall()
            
            if appointments:
                for appointment in appointments:
                    report_text += f"   - Appointment ID: {appointment[0]}, Patient: {appointment[1]}, Doctor: {appointment[2]}, Status: {appointment[3]}\n"
            else:
                report_text += "   No appointments scheduled for this date.\n"
                
            report_text += f"\n3. REVENUE DETAILS:\n"
            report_text += f"   Total Revenue: ₹{total_revenue:.2f}\n"
            
            # Add payment status breakdown
            cursor.execute('''
                SELECT payment_status, COUNT(*), SUM(total_amount)
                FROM billing 
                WHERE billing_date = ?
                GROUP BY payment_status
            ''', (selected_date,))
            payment_stats = cursor.fetchall()
            
            if payment_stats:
                report_text += "\n4. PAYMENT STATUS BREAKDOWN:\n"
                for status, count, amount in payment_stats:
                    report_text += f"   {status}: {count} bills, ₹{amount or 0:.2f}\n"
            else:
                report_text += "\n4. PAYMENT STATUS BREAKDOWN:\n"
                report_text += "   No billing records found.\n"
                
            # Add payment method breakdown
            cursor.execute('''
                SELECT payment_method, COUNT(*), SUM(total_amount)
                FROM billing 
                WHERE billing_date = ?
                GROUP BY payment_method
            ''', (selected_date,))
            method_stats = cursor.fetchall()
            
            if method_stats:
                report_text += "\n5. PAYMENT METHOD BREAKDOWN:\n"
                for method, count, amount in method_stats:
                    report_text += f"   {method}: {count} bills, ₹{amount or 0:.2f}\n"
            else:
                report_text += "\n5. PAYMENT METHOD BREAKDOWN:\n"
                report_text += "   No billing records found.\n"
                
            # Add doctor salary information for the date
            cursor.execute('''
                SELECT d.name, s.salary_amount, s.payment_status, s.payment_method
                FROM doctor_salary s
                JOIN doctors d ON s.doctor_id = d.id
                WHERE s.payment_date = ?
                ORDER BY d.name
            ''', (selected_date,))
            salaries = cursor.fetchall()
            
            if salaries:
                report_text += f"\n6. DOCTOR SALARIES PAID ON {selected_date}:\n"
                total_salary = 0
                for name, amount, status, method in salaries:
                    report_text += f"   {name}: ₹{amount:.2f} (via {method})\n"
                    total_salary += amount
                report_text += f"   Total Salaries Paid: ₹{total_salary:.2f}\n"
            else:
                report_text += f"\n6. DOCTOR SALARIES PAID ON {selected_date}:\n"
                report_text += "   No salary payments recorded.\n"
                
            # Display report
            self.daily_report_text.delete(1.0, tk.END)
            self.daily_report_text.insert(1.0, report_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate daily report: {str(e)}")
            
    def generate_monthly_report(self):
        """Generate monthly report for the selected month/year"""
        selected_month = self.month_var.get().strip()
        selected_year = self.year_entry.get().strip()
        
        # Validate inputs
        if not selected_month or not selected_year:
            messagebox.showerror("Error", "Please select both month and year")
            return
            
        try:
            selected_year = int(selected_year)
            selected_month = int(selected_month)
            
            if selected_month < 1 or selected_month > 12:
                raise ValueError("Invalid month")
                
            if selected_year < 2000 or selected_year > 2100:
                raise ValueError("Invalid year")
                
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid month (01-12) and year (2000-2100)")
            return
            
        # Format the date range for the month
        month_str = f"{selected_year}-{selected_month:02d}"
        
        try:
            cursor = self.db_conn.cursor()
            
            # Get total patients admitted in the selected month
            cursor.execute("SELECT COUNT(*) FROM patients WHERE admission_date LIKE ?", (f"{month_str}%",))
            total_patients = cursor.fetchone()[0]
            
            # Get total appointments in the selected month
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date LIKE ?", (f"{month_str}%",))
            total_appointments = cursor.fetchone()[0]
            
            # Get total revenue for the selected month
            cursor.execute('''
                SELECT SUM(total_amount) 
                FROM billing 
                WHERE billing_date LIKE ?
            ''', (f"{month_str}%",))
            total_revenue = cursor.fetchone()[0] or 0
            
            # Generate report text
            report_text = f"""
MONTHLY HOSPITAL REPORT
=======================
Month: {selected_month:02d}/{selected_year}
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

SUMMARY:
--------
Total Patients Admitted: {total_patients}
Total Appointments: {total_appointments}
Total Revenue Generated: ₹{total_revenue:.2f}

DETAILED INFORMATION:
---------------------
1. PATIENTS ADMITTED:
"""
            
            # Get patient details
            cursor.execute("SELECT id, name, disease, admission_date FROM patients WHERE admission_date LIKE ? ORDER BY admission_date", (f"{month_str}%",))
            patients = cursor.fetchall()
            
            if patients:
                for patient in patients:
                    report_text += f"   - ID: {patient[0]}, Name: {patient[1]}, Disease: {patient[2]}, Admission Date: {patient[3]}\n"
            else:
                report_text += "   No patients admitted this month.\n"
                
            report_text += "\n2. APPOINTMENTS:\n"
            
            # Get appointment details
            cursor.execute('''
                SELECT a.id, p.name, d.name, a.appointment_date, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                WHERE a.appointment_date LIKE ?
                ORDER BY a.appointment_date
            ''', (f"{month_str}%",))
            appointments = cursor.fetchall()
            
            if appointments:
                for appointment in appointments:
                    report_text += f"   - Appointment ID: {appointment[0]}, Patient: {appointment[1]}, Doctor: {appointment[2]}, Date: {appointment[3]}, Status: {appointment[4]}\n"
            else:
                report_text += "   No appointments scheduled this month.\n"
                
            report_text += f"\n3. REVENUE DETAILS:\n"
            report_text += f"   Total Revenue: ₹{total_revenue:.2f}\n"
            
            # Add payment status breakdown
            cursor.execute('''
                SELECT payment_status, COUNT(*), SUM(total_amount)
                FROM billing 
                WHERE billing_date LIKE ?
                GROUP BY payment_status
            ''', (f"{month_str}%",))
            payment_stats = cursor.fetchall()
            
            if payment_stats:
                report_text += "\n4. PAYMENT STATUS BREAKDOWN:\n"
                for status, count, amount in payment_stats:
                    report_text += f"   {status}: {count} bills, ₹{amount or 0:.2f}\n"
            else:
                report_text += "\n4. PAYMENT STATUS BREAKDOWN:\n"
                report_text += "   No billing records found.\n"
                
            # Add payment method breakdown
            cursor.execute('''
                SELECT payment_method, COUNT(*), SUM(total_amount)
                FROM billing 
                WHERE billing_date LIKE ?
                GROUP BY payment_method
            ''', (f"{month_str}%",))
            method_stats = cursor.fetchall()
            
            if method_stats:
                report_text += "\n5. PAYMENT METHOD BREAKDOWN:\n"
                for method, count, amount in method_stats:
                    report_text += f"   {method}: {count} bills, ₹{amount or 0:.2f}\n"
            else:
                report_text += "\n5. PAYMENT METHOD BREAKDOWN:\n"
                report_text += "   No billing records found.\n"
                
            # Add doctor salary information
            cursor.execute('''
                SELECT d.name, s.salary_amount, s.payment_status, s.payment_method
                FROM doctor_salary s
                JOIN doctors d ON s.doctor_id = d.id
                WHERE s.salary_month = ? AND s.salary_year = ?
                ORDER BY d.name
            ''', (f"{selected_month:02d}", str(selected_year)))
            salaries = cursor.fetchall()
            
            if salaries:
                report_text += f"\n6. DOCTOR SALARIES FOR {selected_month:02d}/{selected_year}:\n"
                total_salary = 0
                for name, amount, status, method in salaries:
                    report_text += f"   {name}: ₹{amount:.2f} ({status} via {method})\n"
                    if status == "Paid":
                        total_salary += amount
                report_text += f"   Total Paid Salaries: ₹{total_salary:.2f}\n"
            else:
                report_text += f"\n6. DOCTOR SALARIES FOR {selected_month:02d}/{selected_year}:\n"
                report_text += "   No salary records found.\n"
                
            # Display report
            self.monthly_report_text.delete(1.0, tk.END)
            self.monthly_report_text.insert(1.0, report_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate monthly report: {str(e)}")
            
    def export_daily_report(self):
        """Export daily report (placeholder functionality)"""
        report_content = self.daily_report_text.get(1.0, tk.END).strip()
        if not report_content:
            messagebox.showinfo("Export Report", "Please generate a report first.")
            return
            
        messagebox.showinfo(
            "Export Report",
            "In a full implementation, this would export the daily report as PDF or Excel.\n"
            "For now, you can copy the report text and save it manually."
        )
        
    def export_monthly_report(self):
        """Export monthly report (placeholder functionality)"""
        report_content = self.monthly_report_text.get(1.0, tk.END).strip()
        if not report_content:
            messagebox.showinfo("Export Report", "Please generate a report first.")
            return
            
        messagebox.showinfo(
            "Export Report",
            "In a full implementation, this would export the monthly report as PDF or Excel.\n"
            "For now, you can copy the report text and save it manually."
        )
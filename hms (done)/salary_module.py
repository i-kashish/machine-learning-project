import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class SalaryModule:
    def __init__(self, parent, db_conn):
        self.parent = parent
        self.db_conn = db_conn
        self.current_salary_id = None
        
    def show(self):
        """Display the salary module interface"""
        # Clear the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.salary_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.salary_tab, text="Doctor Salary")
        self.notebook.add(self.search_tab, text="Search Salaries")
        
        # Setup tabs
        self.setup_salary_tab()
        self.setup_search_tab()
        
    def setup_salary_tab(self):
        """Setup the doctor salary tab"""
        # Main frame for salary
        salary_frame = ttk.Frame(self.salary_tab, padding="20")
        salary_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(salary_frame, text="Doctor Salary Management", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Doctor selection
        doctor_label = ttk.Label(salary_frame, text="Select Doctor:", font=("Arial", 10))
        doctor_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Doctor combobox
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(
            salary_frame,
            textvariable=self.doctor_var,
            width=28,
            state="readonly"
        )
        self.doctor_combo.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Refresh doctor list button
        refresh_doctors_btn = ttk.Button(
            salary_frame,
            text="Refresh Doctors",
            command=self.load_doctors,
            width=15
        )
        refresh_doctors_btn.grid(row=1, column=2, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Salary fields
        fields = [
            ("Salary Amount:", 2),
            ("Salary Month:", 3),
            ("Salary Year:", 4)
        ]
        
        self.entries = {}
        
        for label_text, row in fields:
            label = ttk.Label(salary_frame, text=label_text, font=("Arial", 10))
            label.grid(row=row, column=0, sticky=tk.W, pady=5)
            
            entry = ttk.Entry(salary_frame, width=30)
            entry.grid(row=row, column=1, padx=(10, 0), pady=5, sticky=tk.W)
            
            key = label_text.replace(":", "").replace(" ", "_").lower()
            self.entries[key] = entry
            
            # Set default values
            if "month" in key:
                entry.insert(0, datetime.now().strftime("%m"))
            elif "year" in key:
                entry.insert(0, datetime.now().strftime("%Y"))
            else:
                entry.insert(0, "0")
                
        # Payment status
        status_label = ttk.Label(salary_frame, text="Payment Status:", font=("Arial", 10))
        status_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        
        self.payment_status_var = tk.StringVar(value="Unpaid")
        status_combo = ttk.Combobox(
            salary_frame,
            textvariable=self.payment_status_var,
            values=["Unpaid", "Paid", "Pending"],
            width=28,
            state="readonly"
        )
        status_combo.grid(row=5, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Payment method
        method_label = ttk.Label(salary_frame, text="Payment Method:", font=("Arial", 10))
        method_label.grid(row=6, column=0, sticky=tk.W, pady=5)
        
        self.payment_method_var = tk.StringVar(value="Cash")
        method_combo = ttk.Combobox(
            salary_frame,
            textvariable=self.payment_method_var,
            values=["Cash", "Online", "Bank Transfer", "Cheque"],
            width=28,
            state="readonly"
        )
        method_combo.grid(row=6, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Payment date (only editable when status is Paid)
        date_label = ttk.Label(salary_frame, text="Payment Date (YYYY-MM-DD):", font=("Arial", 10))
        date_label.grid(row=7, column=0, sticky=tk.W, pady=5)
        
        self.payment_date_entry = ttk.Entry(salary_frame, width=30)
        self.payment_date_entry.grid(row=7, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        self.payment_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Buttons frame
        button_frame = ttk.Frame(salary_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=20)
        
        # Generate salary button
        generate_btn = ttk.Button(
            button_frame,
            text="Generate Salary",
            command=self.generate_salary
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Update button
        self.update_btn = ttk.Button(
            button_frame,
            text="Update Salary",
            command=self.update_salary,
            state=tk.DISABLED
        )
        self.update_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Delete button
        self.delete_btn = ttk.Button(
            button_frame,
            text="Delete Salary",
            command=self.delete_salary,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.load_doctors()
        
    def setup_search_tab(self):
        """Setup the salary search tab"""
        # Main frame for search
        search_frame = ttk.Frame(self.search_tab, padding="20")
        search_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search controls
        search_controls_frame = ttk.Frame(search_frame)
        search_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_controls_frame, text="Search by Doctor:").pack(side=tk.LEFT)
        
        self.search_entry = ttk.Entry(search_controls_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        search_btn = ttk.Button(
            search_controls_frame,
            text="Search",
            command=self.search_salaries
        )
        search_btn.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            search_controls_frame,
            text="Refresh",
            command=self.load_all_salaries
        )
        refresh_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview for displaying salaries
        tree_frame = ttk.Frame(search_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.salary_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Doctor", "Amount", "Month", "Year", "Status", "Method", "Payment Date"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.salary_tree.yview)
        h_scrollbar.config(command=self.salary_tree.xview)
        
        # Define headings
        headings = ["ID", "Doctor", "Amount", "Month", "Year", "Status", "Method", "Payment Date"]
        for i, heading in enumerate(headings):
            self.salary_tree.heading(heading, text=heading)
            # Set column widths
            widths = [50, 150, 100, 80, 80, 100, 100, 100]
            self.salary_tree.column(heading, width=widths[i])
            
        # Pack treeview and scrollbars
        self.salary_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.salary_tree.bind("<<TreeviewSelect>>", self.on_salary_select)
        
        # Buttons frame for actions
        buttons_frame = ttk.Frame(search_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # View Details button
        view_details_btn = ttk.Button(
            buttons_frame,
            text="View Salary Details",
            command=self.view_salary_details
        )
        view_details_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Load all salaries initially
        self.load_all_salaries()
        
    def load_doctors(self):
        """Load doctors into the doctor combobox"""
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, name FROM doctors ORDER BY name")
        doctors = cursor.fetchall()
        
        # Create a list of doctor names for the combobox
        doctor_names = [f"{doctor[1]} (ID: {doctor[0]})" for doctor in doctors]
        self.doctor_combo['values'] = doctor_names
        
        # If there are doctors, select the first one
        if doctor_names:
            self.doctor_combo.set(doctor_names[0])
            
    def get_selected_doctor_id(self):
        """Extract doctor ID from selected combobox value"""
        selected = self.doctor_var.get()
        if selected and " (ID: " in selected:
            try:
                # Extract ID from "Name (ID: X)"
                start = selected.rfind("(ID: ") + 5
                end = selected.rfind(")")
                return int(selected[start:end])
            except:
                return None
        return None
        
    def load_all_salaries(self):
        """Load all salaries into the treeview"""
        # Clear existing items
        for item in self.salary_tree.get_children():
            self.salary_tree.delete(item)
            
        # Fetch salaries from database with doctor names
        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT s.id, d.name, s.salary_amount, s.salary_month, s.salary_year, 
                   s.payment_status, s.payment_method, s.payment_date
            FROM doctor_salary s
            JOIN doctors d ON s.doctor_id = d.id
            ORDER BY s.salary_year DESC, s.salary_month DESC
        ''')
        salaries = cursor.fetchall()
        
        # Insert salaries into treeview
        for salary in salaries:
            self.salary_tree.insert("", tk.END, values=salary)
            
    def search_salaries(self):
        """Search salaries by doctor name"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a doctor name to search")
            return
            
        # Clear existing items
        for item in self.salary_tree.get_children():
            self.salary_tree.delete(item)
            
        # Search in database
        cursor = self.db_conn.cursor()
        query = '''
            SELECT s.id, d.name, s.salary_amount, s.salary_month, s.salary_year, 
                   s.payment_status, s.payment_method, s.payment_date
            FROM doctor_salary s
            JOIN doctors d ON s.doctor_id = d.id
            WHERE d.name LIKE ?
            ORDER BY s.salary_year DESC, s.salary_month DESC
        '''
        cursor.execute(query, (f"%{search_term}%",))
        salaries = cursor.fetchall()
        
        # Insert salaries into treeview
        for salary in salaries:
            self.salary_tree.insert("", tk.END, values=salary)
            
        if not salaries:
            messagebox.showinfo("Info", "No salaries found for the specified doctor")
            
    def on_salary_select(self, event):
        """Handle salary selection from treeview"""
        selection = self.salary_tree.selection()
        if selection:
            item = self.salary_tree.item(selection[0])
            salary_data = item['values']
            
            # Enable update and delete buttons
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            
            # Store current salary ID
            self.current_salary_id = salary_data[0]
            
            # Populate form with salary data
            self.populate_form(salary_data)
            
    def populate_form(self, salary_data):
        """Populate the salary form with salary data"""
        # salary_data: [id, doctor_name, amount, month, year, status, method, payment_date]
        
        # Find and select doctor
        doctor_name = salary_data[1]
        doctor_values = self.doctor_combo['values']
        for value in doctor_values:
            if doctor_name in value:
                self.doctor_combo.set(value)
                break
                
        # Set salary values
        self.entries['salary_amount'].delete(0, tk.END)
        self.entries['salary_amount'].insert(0, salary_data[2])
        
        self.entries['salary_month'].delete(0, tk.END)
        self.entries['salary_month'].insert(0, salary_data[3])
        
        self.entries['salary_year'].delete(0, tk.END)
        self.entries['salary_year'].insert(0, salary_data[4])
        
        # Set payment status and method
        self.payment_status_var.set(salary_data[5])
        self.payment_method_var.set(salary_data[6])
        
        # Set payment date
        self.payment_date_entry.delete(0, tk.END)
        self.payment_date_entry.insert(0, salary_data[7] or "")
        
    def generate_salary(self):
        """Generate a new salary record"""
        # Get form data
        doctor_id = self.get_selected_doctor_id()
        amount = self.entries['salary_amount'].get().strip() or "0"
        month = self.entries['salary_month'].get().strip()
        year = self.entries['salary_year'].get().strip()
        status = self.payment_status_var.get()
        method = self.payment_method_var.get()
        payment_date = self.payment_date_entry.get().strip() or None
        
        # Validate input
        if not doctor_id:
            messagebox.showerror("Error", "Please select a doctor")
            return
            
        # Validate numeric values
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value for salary amount")
            return
            
        # Validate month and year
        try:
            month = int(month)
            year = int(year)
            if month < 1 or month > 12:
                raise ValueError("Invalid month")
            if year < 2000 or year > 2100:
                raise ValueError("Invalid year")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid month (01-12) and year (2000-2100)")
            return
            
        # If status is Paid, payment date is required
        if status == "Paid" and not payment_date:
            messagebox.showerror("Error", "Please enter a payment date for paid salaries")
            return
            
        # Validate date format if provided
        if payment_date:
            try:
                datetime.strptime(payment_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Payment date must be in YYYY-MM-DD format")
                return
                
        # Insert into database
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO doctor_salary (
                    doctor_id, salary_amount, salary_month, salary_year, 
                    payment_status, payment_method, payment_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (doctor_id, amount, f"{month:02d}", str(year), status, method, payment_date))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Salary record generated successfully")
            
            # Clear form
            self.clear_form()
            
            # Refresh salary list
            self.load_all_salaries()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate salary record: {str(e)}")
            
    def update_salary(self):
        """Update an existing salary record"""
        if not self.current_salary_id:
            messagebox.showerror("Error", "No salary record selected for update")
            return
            
        # Get form data
        doctor_id = self.get_selected_doctor_id()
        amount = self.entries['salary_amount'].get().strip() or "0"
        month = self.entries['salary_month'].get().strip()
        year = self.entries['salary_year'].get().strip()
        status = self.payment_status_var.get()
        method = self.payment_method_var.get()
        payment_date = self.payment_date_entry.get().strip() or None
        
        # Validate input
        if not doctor_id:
            messagebox.showerror("Error", "Please select a doctor")
            return
            
        # Validate numeric values
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value for salary amount")
            return
            
        # Validate month and year
        try:
            month = int(month)
            year = int(year)
            if month < 1 or month > 12:
                raise ValueError("Invalid month")
            if year < 2000 or year > 2100:
                raise ValueError("Invalid year")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid month (01-12) and year (2000-2100)")
            return
            
        # If status is Paid, payment date is required
        if status == "Paid" and not payment_date:
            messagebox.showerror("Error", "Please enter a payment date for paid salaries")
            return
            
        # Validate date format if provided
        if payment_date:
            try:
                datetime.strptime(payment_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Payment date must be in YYYY-MM-DD format")
                return
                
        # Update database
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                UPDATE doctor_salary SET 
                    doctor_id=?, salary_amount=?, salary_month=?, salary_year=?, 
                    payment_status=?, payment_method=?, payment_date=?
                WHERE id=?
            ''', (doctor_id, amount, f"{month:02d}", str(year), status, method, payment_date, self.current_salary_id))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Salary record updated successfully")
            
            # Refresh salary list
            self.load_all_salaries()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update salary record: {str(e)}")
            
    def delete_salary(self):
        """Delete a salary record"""
        if not self.current_salary_id:
            messagebox.showerror("Error", "No salary record selected for deletion")
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this salary record?\nThis action cannot be undone."
        )
        
        if result:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM doctor_salary WHERE id=?", (self.current_salary_id,))
                
                self.db_conn.commit()
                messagebox.showinfo("Success", "Salary record deleted successfully")
                
                # Clear form and disable buttons
                self.clear_form()
                self.update_btn.config(state=tk.DISABLED)
                self.delete_btn.config(state=tk.DISABLED)
                self.current_salary_id = None
                
                # Refresh salary list
                self.load_all_salaries()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete salary record: {str(e)}")
                
    def clear_form(self):
        """Clear the salary form"""
        # Reset combobox to first value
        doctor_values = self.doctor_combo['values']
        if doctor_values:
            self.doctor_combo.set(doctor_values[0])
            
        # Clear salary entries and set defaults
        self.entries['salary_amount'].delete(0, tk.END)
        self.entries['salary_amount'].insert(0, "0")
        
        self.entries['salary_month'].delete(0, tk.END)
        self.entries['salary_month'].insert(0, datetime.now().strftime("%m"))
        
        self.entries['salary_year'].delete(0, tk.END)
        self.entries['salary_year'].insert(0, datetime.now().strftime("%Y"))
        
        # Reset payment status and method
        self.payment_status_var.set("Unpaid")
        self.payment_method_var.set("Cash")
        
        # Reset payment date
        self.payment_date_entry.delete(0, tk.END)
        self.payment_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.current_salary_id = None
        
    def view_salary_details(self):
        """View detailed salary information"""
        selection = self.salary_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a salary record to view details")
            return
            
        item = self.salary_tree.item(selection[0])
        salary_data = item['values']
        
        # salary_data: [id, doctor_name, amount, month, year, status, method, payment_date]
        salary_id = salary_data[0]
        doctor_name = salary_data[1]
        amount = float(salary_data[2])
        month = salary_data[3]
        year = salary_data[4]
        status = salary_data[5]
        method = salary_data[6]
        payment_date = salary_data[7]
        
        # Create a new window for salary details
        details_window = tk.Toplevel(self.parent)
        details_window.title(f"Salary Details - Salary ID: {salary_id}")
        details_window.geometry("400x400")
        details_window.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(details_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="SALARY DETAILS", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Salary information frame
        info_frame = ttk.LabelFrame(main_frame, text="Salary Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Salary details
        ttk.Label(info_frame, text=f"Salary ID: {salary_id}", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Doctor Name: {doctor_name}", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Salary Period: {month}/{year}", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Amount: ₹{amount:.2f}", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Status: {status}", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Payment Method: {method}", font=("Arial", 10)).grid(row=5, column=0, sticky=tk.W, pady=2)
        if payment_date:
            ttk.Label(info_frame, text=f"Payment Date: {payment_date}", font=("Arial", 10)).grid(row=6, column=0, sticky=tk.W, pady=2)
        
        # Close button
        close_btn = ttk.Button(main_frame, text="Close", command=details_window.destroy)
        close_btn.pack(pady=(20, 0))

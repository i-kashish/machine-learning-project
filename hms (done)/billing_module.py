import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class BillingModule:
    def __init__(self, parent, db_conn):
        self.parent = parent
        self.db_conn = db_conn
        self.current_bill_id = None
        
    def show(self):
        """Display the billing module interface"""
        # Clear the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.billing_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.billing_tab, text="Generate Bill")
        self.notebook.add(self.search_tab, text="Search Bills")
        
        # Setup tabs
        self.setup_billing_tab()
        self.setup_search_tab()
        
    def setup_billing_tab(self):
        """Setup the billing tab"""
        # Main frame for billing
        billing_frame = ttk.Frame(self.billing_tab, padding="20")
        billing_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(billing_frame, text="Generate Patient Bill", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Patient selection
        patient_label = ttk.Label(billing_frame, text="Select Patient:", font=("Arial", 10))
        patient_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Patient combobox
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(
            billing_frame,
            textvariable=self.patient_var,
            width=28,
            state="readonly"
        )
        self.patient_combo.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Refresh patient list button
        refresh_patients_btn = ttk.Button(
            billing_frame,
            text="Refresh Patients",
            command=self.load_patients,
            width=15
        )
        refresh_patients_btn.grid(row=1, column=2, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Billing fields
        fields = [
            ("Consultation Fee:", 2),
            ("Medicine Charges:", 3),
            ("Room Charges (per day):", 4),
            ("Number of Days:", 5),
            ("Other Charges:", 6)
        ]
        
        self.entries = {}
        
        for label_text, row in fields:
            label = ttk.Label(billing_frame, text=label_text, font=("Arial", 10))
            label.grid(row=row, column=0, sticky=tk.W, pady=5)
            
            entry = ttk.Entry(billing_frame, width=30)
            entry.grid(row=row, column=1, padx=(10, 0), pady=5, sticky=tk.W)
            
            key = label_text.replace(":", "").replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_").lower()
            self.entries[key] = entry
            
            # Set default value to 0 (except for number of days which defaults to 1)
            if "number_of_days" in key:
                entry.insert(0, "1")
            else:
                entry.insert(0, "0")
            
        # Payment status
        status_label = ttk.Label(billing_frame, text="Payment Status:", font=("Arial", 10))
        status_label.grid(row=7, column=0, sticky=tk.W, pady=5)
        
        self.payment_status_var = tk.StringVar(value="Unpaid")
        status_combo = ttk.Combobox(
            billing_frame,
            textvariable=self.payment_status_var,
            values=["Unpaid", "Paid", "Pending"],
            width=28,
            state="readonly"
        )
        status_combo.grid(row=7, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Payment method
        method_label = ttk.Label(billing_frame, text="Payment Method:", font=("Arial", 10))
        method_label.grid(row=8, column=0, sticky=tk.W, pady=5)
        
        self.payment_method_var = tk.StringVar(value="Cash")
        method_combo = ttk.Combobox(
            billing_frame,
            textvariable=self.payment_method_var,
            values=["Cash", "Online", "Bank Transfer", "Cheque"],
            width=28,
            state="readonly"
        )
        method_combo.grid(row=8, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Payment date (only editable when status is Paid)
        date_label = ttk.Label(billing_frame, text="Payment Date (YYYY-MM-DD):", font=("Arial", 10))
        date_label.grid(row=9, column=0, sticky=tk.W, pady=5)
        
        self.payment_date_entry = ttk.Entry(billing_frame, width=30)
        self.payment_date_entry.grid(row=9, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        self.payment_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Total amount label
        total_label = ttk.Label(billing_frame, text="Total Amount:", font=("Arial", 12, "bold"))
        total_label.grid(row=10, column=0, sticky=tk.W, pady=(10, 5))
        
        self.total_amount_var = tk.StringVar(value="0.00")
        total_entry = ttk.Entry(
            billing_frame, 
            textvariable=self.total_amount_var, 
            width=30, 
            font=("Arial", 12, "bold"),
            state="readonly"
        )
        total_entry.grid(row=10, column=1, padx=(10, 0), pady=(10, 5), sticky=tk.W)
        
        # Calculate button
        calc_btn = ttk.Button(
            billing_frame,
            text="Calculate Total",
            command=self.calculate_total
        )
        calc_btn.grid(row=10, column=2, padx=(10, 0), pady=(10, 5), sticky=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(billing_frame)
        button_frame.grid(row=11, column=0, columnspan=3, pady=20)
        
        # Generate bill button
        generate_btn = ttk.Button(
            button_frame,
            text="Generate Bill",
            command=self.generate_bill
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Update button
        self.update_btn = ttk.Button(
            button_frame,
            text="Update Bill",
            command=self.update_bill,
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
            text="Delete Bill",
            command=self.delete_bill,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Print bill button
        print_btn = ttk.Button(
            button_frame,
            text="Print/Export Bill",
            command=self.print_bill
        )
        print_btn.pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.load_patients()
        
    def setup_search_tab(self):
        """Setup the bill search tab"""
        # Main frame for search
        search_frame = ttk.Frame(self.search_tab, padding="20")
        search_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search controls
        search_controls_frame = ttk.Frame(search_frame)
        search_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_controls_frame, text="Search by Patient:").pack(side=tk.LEFT)
        
        self.search_entry = ttk.Entry(search_controls_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        search_btn = ttk.Button(
            search_controls_frame,
            text="Search",
            command=self.search_bills
        )
        search_btn.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            search_controls_frame,
            text="Refresh",
            command=self.load_all_bills
        )
        refresh_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview for displaying bills
        tree_frame = ttk.Frame(search_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.bill_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Patient", "Consultation", "Medicine", "Room/Day", "Days", "Other", "Total", "Status", "Method", "Payment Date", "Billing Date"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.bill_tree.yview)
        h_scrollbar.config(command=self.bill_tree.xview)
        
        # Define headings
        headings = ["ID", "Patient", "Consultation", "Medicine", "Room/Day", "Days", "Other", "Total", "Status", "Method", "Payment Date", "Billing Date"]
        for i, heading in enumerate(headings):
            self.bill_tree.heading(heading, text=heading)
            # Set column widths
            widths = [50, 150, 100, 100, 100, 50, 100, 100, 100, 100, 100, 100]
            self.bill_tree.column(heading, width=widths[i])
            
        # Pack treeview and scrollbars
        self.bill_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.bill_tree.bind("<<TreeviewSelect>>", self.on_bill_select)
        
        # Buttons frame for actions
        buttons_frame = ttk.Frame(search_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # View Details button
        view_details_btn = ttk.Button(
            buttons_frame,
            text="View Bill Details",
            command=self.view_bill_details
        )
        view_details_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Load all bills initially
        self.load_all_bills()
        
    def load_patients(self):
        """Load patients into the patient combobox"""
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, name FROM patients ORDER BY name")
        patients = cursor.fetchall()
        
        # Create a list of patient names for the combobox
        patient_names = [f"{patient[1]} (ID: {patient[0]})" for patient in patients]
        self.patient_combo['values'] = patient_names
        
        # If there are patients, select the first one
        if patient_names:
            self.patient_combo.set(patient_names[0])
            
    def get_selected_patient_id(self):
        """Extract patient ID from selected combobox value"""
        selected = self.patient_var.get()
        if selected and " (ID: " in selected:
            try:
                # Extract ID from "Name (ID: X)"
                start = selected.rfind("(ID: ") + 5
                end = selected.rfind(")")
                return int(selected[start:end])
            except:
                return None
        return None
        
    def calculate_total(self):
        """Calculate the total bill amount"""
        try:
            consultation = float(self.entries['consultation_fee'].get() or 0)
            medicine = float(self.entries['medicine_charges'].get() or 0)
            room_per_day = float(self.entries['room_charges_per_day'].get() or 0)
            days = int(self.entries['number_of_days'].get() or 1)
            other = float(self.entries['other_charges'].get() or 0)
            
            total = consultation + medicine + (room_per_day * days) + other
            self.total_amount_var.set(f"{total:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for all charges")
            
    def load_all_bills(self):
        """Load all bills into the treeview"""
        # Clear existing items
        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)
            
        # Fetch bills from database with patient names
        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT b.id, p.name, b.consultation_fee, b.medicine_charges, 
                   b.room_charges_per_day, b.number_of_days, b.other_charges, b.total_amount,
                   b.payment_status, b.payment_method, b.payment_date, b.billing_date
            FROM billing b
            JOIN patients p ON b.patient_id = p.id
            ORDER BY b.billing_date DESC
        ''')
        bills = cursor.fetchall()
        
        # Insert bills into treeview
        for bill in bills:
            self.bill_tree.insert("", tk.END, values=bill)
            
    def search_bills(self):
        """Search bills by patient name"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a patient name to search")
            return
            
        # Clear existing items
        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)
            
        # Search in database
        cursor = self.db_conn.cursor()
        query = '''
            SELECT b.id, p.name, b.consultation_fee, b.medicine_charges, 
                   b.room_charges_per_day, b.number_of_days, b.other_charges, b.total_amount,
                   b.payment_status, b.payment_method, b.payment_date, b.billing_date
            FROM billing b
            JOIN patients p ON b.patient_id = p.id
            WHERE p.name LIKE ?
            ORDER BY b.billing_date DESC
        '''
        cursor.execute(query, (f"%{search_term}%",))
        bills = cursor.fetchall()
        
        # Insert bills into treeview
        for bill in bills:
            self.bill_tree.insert("", tk.END, values=bill)
            
        if not bills:
            messagebox.showinfo("Info", "No bills found for the specified patient")
            
    def on_bill_select(self, event):
        """Handle bill selection from treeview"""
        selection = self.bill_tree.selection()
        if selection:
            item = self.bill_tree.item(selection[0])
            bill_data = item['values']
            
            # Enable update and delete buttons
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            
            # Store current bill ID
            self.current_bill_id = bill_data[0]
            
            # Populate form with bill data
            self.populate_form(bill_data)
            
    def populate_form(self, bill_data):
        """Populate the billing form with bill data"""
        # bill_data: [id, patient_name, consultation, medicine, room_per_day, days, other, total, status, method, payment_date, date]
        
        # Find and select patient
        patient_name = bill_data[1]
        patient_values = self.patient_combo['values']
        for value in patient_values:
            if patient_name in value:
                self.patient_combo.set(value)
                break
                
        # Set charge values
        self.entries['consultation_fee'].delete(0, tk.END)
        self.entries['consultation_fee'].insert(0, bill_data[2])
        
        self.entries['medicine_charges'].delete(0, tk.END)
        self.entries['medicine_charges'].insert(0, bill_data[3])
        
        self.entries['room_charges_per_day'].delete(0, tk.END)
        self.entries['room_charges_per_day'].insert(0, bill_data[4])
        
        self.entries['number_of_days'].delete(0, tk.END)
        self.entries['number_of_days'].insert(0, bill_data[5])
        
        self.entries['other_charges'].delete(0, tk.END)
        self.entries['other_charges'].insert(0, bill_data[6])
        
        # Set total amount
        self.total_amount_var.set(f"{bill_data[7]:.2f}")
        
        # Set payment status and method
        self.payment_status_var.set(bill_data[8])
        self.payment_method_var.set(bill_data[9])
        
        # Set payment date
        self.payment_date_entry.delete(0, tk.END)
        self.payment_date_entry.insert(0, bill_data[10] or "")
        
    def generate_bill(self):
        """Generate a new bill"""
        # Get form data
        patient_id = self.get_selected_patient_id()
        consultation = self.entries['consultation_fee'].get().strip() or "0"
        medicine = self.entries['medicine_charges'].get().strip() or "0"
        room_per_day = self.entries['room_charges_per_day'].get().strip() or "0"
        days = self.entries['number_of_days'].get().strip() or "1"
        other = self.entries['other_charges'].get().strip() or "0"
        total = self.total_amount_var.get()
        status = self.payment_status_var.get()
        method = self.payment_method_var.get()
        payment_date = self.payment_date_entry.get().strip() or None
        billing_date = datetime.now().strftime("%Y-%m-%d")
        
        # Validate input
        if not patient_id:
            messagebox.showerror("Error", "Please select a patient")
            return
            
        # Validate numeric values
        try:
            consultation = float(consultation)
            medicine = float(medicine)
            room_per_day = float(room_per_day)
            days = int(days)
            other = float(other)
            total = float(total)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for all charges")
            return
            
        # If status is Paid, payment date is required
        if status == "Paid" and not payment_date:
            messagebox.showerror("Error", "Please enter a payment date for paid bills")
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
                INSERT INTO billing (
                    patient_id, consultation_fee, medicine_charges, 
                    room_charges_per_day, number_of_days, other_charges, total_amount, 
                    billing_date, payment_status, payment_method, payment_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (patient_id, consultation, medicine, room_per_day, days, other, total, billing_date, status, method, payment_date))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Bill generated successfully")
            
            # Clear form
            self.clear_form()
            
            # Refresh bill list
            self.load_all_bills()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bill: {str(e)}")
            
    def update_bill(self):
        """Update an existing bill"""
        if not self.current_bill_id:
            messagebox.showerror("Error", "No bill selected for update")
            return
            
        # Get form data
        patient_id = self.get_selected_patient_id()
        consultation = self.entries['consultation_fee'].get().strip() or "0"
        medicine = self.entries['medicine_charges'].get().strip() or "0"
        room_per_day = self.entries['room_charges_per_day'].get().strip() or "0"
        days = self.entries['number_of_days'].get().strip() or "1"
        other = self.entries['other_charges'].get().strip() or "0"
        total = self.total_amount_var.get()
        status = self.payment_status_var.get()
        method = self.payment_method_var.get()
        payment_date = self.payment_date_entry.get().strip() or None
        billing_date = datetime.now().strftime("%Y-%m-%d")
        
        # Validate input
        if not patient_id:
            messagebox.showerror("Error", "Please select a patient")
            return
            
        # Validate numeric values
        try:
            consultation = float(consultation)
            medicine = float(medicine)
            room_per_day = float(room_per_day)
            days = int(days)
            other = float(other)
            total = float(total)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for all charges")
            return
            
        # If status is Paid, payment date is required
        if status == "Paid" and not payment_date:
            messagebox.showerror("Error", "Please enter a payment date for paid bills")
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
                UPDATE billing SET 
                    patient_id=?, consultation_fee=?, medicine_charges=?, 
                    room_charges_per_day=?, number_of_days=?, other_charges=?, total_amount=?, 
                    billing_date=?, payment_status=?, payment_method=?, payment_date=?
                WHERE id=?
            ''', (patient_id, consultation, medicine, room_per_day, days, other, total, billing_date, status, method, payment_date, self.current_bill_id))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Bill updated successfully")
            
            # Refresh bill list
            self.load_all_bills()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update bill: {str(e)}")
            
    def delete_bill(self):
        """Delete a bill"""
        if not self.current_bill_id:
            messagebox.showerror("Error", "No bill selected for deletion")
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this bill?\nThis action cannot be undone."
        )
        
        if result:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM billing WHERE id=?", (self.current_bill_id,))
                
                self.db_conn.commit()
                messagebox.showinfo("Success", "Bill deleted successfully")
                
                # Clear form and disable buttons
                self.clear_form()
                self.update_btn.config(state=tk.DISABLED)
                self.delete_btn.config(state=tk.DISABLED)
                self.current_bill_id = None
                
                # Refresh bill list
                self.load_all_bills()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete bill: {str(e)}")
                
    def print_bill(self):
        """Print or export the bill (placeholder functionality)"""
        if self.current_bill_id:
            messagebox.showinfo(
                "Print Bill",
                "In a full implementation, this would export the bill as PDF or Excel.\n"
                "For now, you can take a screenshot of the bill details."
            )
        else:
            messagebox.showinfo(
                "Print Bill",
                "Please select a bill to print/export.\n"
                "In a full implementation, this would export the bill as PDF or Excel."
            )
            
    def clear_form(self):
        """Clear the billing form"""
        # Reset combobox to first value
        patient_values = self.patient_combo['values']
        if patient_values:
            self.patient_combo.set(patient_values[0])
            
        # Clear charge entries and set to 0
        for key in ['consultation_fee', 'medicine_charges', 'room_charges_per_day', 'other_charges']:
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, "0")
            
        # Set number of days to 1
        self.entries['number_of_days'].delete(0, tk.END)
        self.entries['number_of_days'].insert(0, "1")
            
        # Reset total amount
        self.total_amount_var.set("0.00")
        
        # Reset payment status and method
        self.payment_status_var.set("Unpaid")
        self.payment_method_var.set("Cash")
        
        # Reset payment date
        self.payment_date_entry.delete(0, tk.END)
        self.payment_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.current_bill_id = None
        
    def view_bill_details(self):
        """View detailed bill information"""
        selection = self.bill_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a bill to view details")
            return
            
        item = self.bill_tree.item(selection[0])
        bill_data = item['values']
        
        # bill_data: [id, patient_name, consultation, medicine, room_per_day, days, other, total, status, method, payment_date, billing_date]
        bill_id = bill_data[0]
        patient_name = bill_data[1]
        consultation = float(bill_data[2])
        medicine = float(bill_data[3])
        room_per_day = float(bill_data[4])
        days = int(bill_data[5])
        other = float(bill_data[6])
        total = float(bill_data[7])
        status = bill_data[8]
        method = bill_data[9]
        payment_date = bill_data[10]
        billing_date = bill_data[11]
        
        # Calculate room charges
        room_total = room_per_day * days
        
        # Create a new window for bill details
        details_window = tk.Toplevel(self.parent)
        details_window.title(f"Bill Details - Bill ID: {bill_id}")
        details_window.geometry("500x600")
        details_window.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(details_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="BILL DETAILS", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Bill information frame
        info_frame = ttk.LabelFrame(main_frame, text="Bill Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Bill ID and dates
        ttk.Label(info_frame, text=f"Bill ID: {bill_id}", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Billing Date: {billing_date}", font=("Arial", 10)).grid(row=0, column=1, sticky=tk.W, pady=2)
        if payment_date:
            ttk.Label(info_frame, text=f"Payment Date: {payment_date}", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Payment Status: {status}", font=("Arial", 10)).grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Payment Method: {method}", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Patient information frame
        patient_frame = ttk.LabelFrame(main_frame, text="Patient Information", padding="10")
        patient_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(patient_frame, text=f"Patient Name: {patient_name}", font=("Arial", 10)).pack(anchor=tk.W)
        
        # Charges breakdown frame
        charges_frame = ttk.LabelFrame(main_frame, text="Charges Breakdown", padding="10")
        charges_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Charges details
        ttk.Label(charges_frame, text="Description", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(charges_frame, text="Amount", font=("Arial", 10, "bold")).grid(row=0, column=1, sticky=tk.E, pady=2)
        
        ttk.Separator(charges_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        ttk.Label(charges_frame, text="Consultation Fee:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(charges_frame, text=f"₹{consultation:.2f}", font=("Arial", 10)).grid(row=2, column=1, sticky=tk.E, pady=2)
        
        ttk.Label(charges_frame, text="Medicine Charges:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Label(charges_frame, text=f"₹{medicine:.2f}", font=("Arial", 10)).grid(row=3, column=1, sticky=tk.E, pady=2)
        
        ttk.Label(charges_frame, text=f"Room Charges:", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Label(charges_frame, text=f"₹{room_per_day:.2f}/day × {days} days", font=("Arial", 10)).grid(row=4, column=1, sticky=tk.E, pady=2)
        
        ttk.Label(charges_frame, text="Other Charges:", font=("Arial", 10)).grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Label(charges_frame, text=f"₹{other:.2f}", font=("Arial", 10)).grid(row=5, column=1, sticky=tk.E, pady=2)
        
        ttk.Separator(charges_frame, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        ttk.Label(charges_frame, text="TOTAL AMOUNT:", font=("Arial", 12, "bold")).grid(row=7, column=0, sticky=tk.W, pady=2)
        ttk.Label(charges_frame, text=f"₹{total:.2f}", font=("Arial", 12, "bold")).grid(row=7, column=1, sticky=tk.E, pady=2)
        
        # Close button
        close_btn = ttk.Button(main_frame, text="Close", command=details_window.destroy)
        close_btn.pack(pady=(20, 0))

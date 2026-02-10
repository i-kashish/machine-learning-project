import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class PatientModule:
    def __init__(self, parent, db_conn):
        self.parent = parent
        self.db_conn = db_conn
        self.current_patient_id = None
        
    def show(self):
        """Display the patient module interface"""
        # Clear the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.registration_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.registration_tab, text="Patient Registration")
        self.notebook.add(self.search_tab, text="Search Patients")
        
        # Setup tabs
        self.setup_registration_tab()
        self.setup_search_tab()
        
    def setup_registration_tab(self):
        """Setup the patient registration tab"""
        # Main frame for registration
        reg_frame = ttk.Frame(self.registration_tab, padding="20")
        reg_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(reg_frame, text="Patient Registration", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Form fields
        fields = [
            ("Name:", 1),
            ("Age:", 2),
            ("Gender:", 3),
            ("Contact:", 4),
            ("Address:", 5),
            ("Disease/Problem:", 6),
            ("Admission Date (YYYY-MM-DD):", 7)
        ]
        
        self.entries = {}
        
        for label_text, row in fields:
            label = ttk.Label(reg_frame, text=label_text, font=("Arial", 10))
            label.grid(row=row, column=0, sticky=tk.W, pady=5)
            
            entry = ttk.Entry(reg_frame, width=30)
            entry.grid(row=row, column=1, padx=(10, 0), pady=5, sticky=tk.W)
            
            # Generate key names for dictionary
            if "Name:" in label_text:
                key = "name"
            elif "Age:" in label_text:
                key = "age"
            elif "Gender:" in label_text:
                key = "gender"
            elif "Contact:" in label_text:
                key = "contact"
            elif "Address:" in label_text:
                key = "address"
            elif "Disease/Problem:" in label_text:
                key = "disease"
            elif "Admission Date" in label_text:
                key = "admission_date"
            else:
                key = label_text.replace(":", "").replace("/", "_").replace(" ", "_").lower()
                
            self.entries[key] = entry
            
        # Set today's date as default for admission date
        self.entries['admission_date'].insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Gender combobox
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(
            reg_frame, 
            textvariable=self.gender_var,
            values=["Male", "Female", "Other"],
            width=28,
            state="readonly"
        )
        gender_combo.grid(row=3, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        gender_combo.set("Male")
        self.entries['gender'] = gender_combo
        
        # Buttons frame
        button_frame = ttk.Frame(reg_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=20)
        
        # Save button
        save_btn = ttk.Button(
            button_frame,
            text="Save Patient",
            command=self.save_patient
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Update button
        self.update_btn = ttk.Button(
            button_frame,
            text="Update Patient",
            command=self.update_patient,
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
            text="Delete Patient",
            command=self.delete_patient,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
    def setup_search_tab(self):
        """Setup the patient search tab"""
        # Main frame for search
        search_frame = ttk.Frame(self.search_tab, padding="20")
        search_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search controls
        search_controls_frame = ttk.Frame(search_frame)
        search_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_controls_frame, text="Search by:").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar(value="name")
        search_combo = ttk.Combobox(
            search_controls_frame,
            textvariable=self.search_var,
            values=["name", "id", "disease", "admission_date"],
            width=15,
            state="readonly"
        )
        search_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        self.search_entry = ttk.Entry(search_controls_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        search_btn = ttk.Button(
            search_controls_frame,
            text="Search",
            command=self.search_patients
        )
        search_btn.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            search_controls_frame,
            text="Refresh",
            command=self.load_all_patients
        )
        refresh_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview for displaying patients
        tree_frame = ttk.Frame(search_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.patient_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Age", "Gender", "Contact", "Address", "Disease", "Admission Date"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.patient_tree.yview)
        h_scrollbar.config(command=self.patient_tree.xview)
        
        # Define headings
        headings = ["ID", "Name", "Age", "Gender", "Contact", "Address", "Disease", "Admission Date"]
        for heading in headings:
            self.patient_tree.heading(heading, text=heading)
            self.patient_tree.column(heading, width=100)
            
        # Pack treeview and scrollbars
        self.patient_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.patient_tree.bind("<<TreeviewSelect>>", self.on_patient_select)
        
        # Load all patients initially
        self.load_all_patients()
        
    def load_all_patients(self):
        """Load all patients into the treeview"""
        # Clear existing items
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
            
        # Fetch patients from database
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM patients ORDER BY id")
        patients = cursor.fetchall()
        
        # Insert patients into treeview
        for patient in patients:
            self.patient_tree.insert("", tk.END, values=patient)
            
    def search_patients(self):
        """Search patients based on criteria"""
        search_term = self.search_entry.get().strip()
        search_by = self.search_var.get()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
            
        # Clear existing items
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
            
        # Search in database
        cursor = self.db_conn.cursor()
        query = f"SELECT * FROM patients WHERE {search_by} LIKE ? ORDER BY id"
        cursor.execute(query, (f"%{search_term}%",))
        patients = cursor.fetchall()
        
        # Insert patients into treeview
        for patient in patients:
            self.patient_tree.insert("", tk.END, values=patient)
            
        if not patients:
            messagebox.showinfo("Info", "No patients found matching the search criteria")
            
    def on_patient_select(self, event):
        """Handle patient selection from treeview"""
        selection = self.patient_tree.selection()
        if selection:
            item = self.patient_tree.item(selection[0])
            patient_data = item['values']
            
            # Enable update and delete buttons
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            
            # Store current patient ID
            self.current_patient_id = patient_data[0]
            
            # Populate form with patient data
            self.populate_form(patient_data)
            
    def populate_form(self, patient_data):
        """Populate the registration form with patient data"""
        # patient_data: [id, name, age, gender, contact, address, disease, admission_date]
        self.entries['name'].delete(0, tk.END)
        self.entries['name'].insert(0, patient_data[1])
        
        self.entries['age'].delete(0, tk.END)
        self.entries['age'].insert(0, patient_data[2])
        
        self.gender_var.set(patient_data[3])
        
        self.entries['contact'].delete(0, tk.END)
        self.entries['contact'].insert(0, patient_data[4])
        
        self.entries['address'].delete(0, tk.END)
        self.entries['address'].insert(0, patient_data[5])
        
        self.entries['disease'].delete(0, tk.END)
        self.entries['disease'].insert(0, patient_data[6])
        
        self.entries['admission_date'].delete(0, tk.END)
        self.entries['admission_date'].insert(0, patient_data[7])
        
    def save_patient(self):
        """Save a new patient to the database"""
        # Get form data
        name = self.entries['name'].get().strip()
        age = self.entries['age'].get().strip()
        gender = self.gender_var.get()
        contact = self.entries['contact'].get().strip()
        address = self.entries['address'].get().strip()
        disease = self.entries['disease'].get().strip()
        admission_date = self.entries['admission_date'].get().strip()
        
        # Validate input
        if not all([name, age, contact, address, disease, admission_date]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        # Validate age is a number
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a valid number")
            return
            
        # Validate date format
        try:
            datetime.strptime(admission_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Admission date must be in YYYY-MM-DD format")
            return
            
        # Insert into database
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO patients (name, age, gender, contact, address, disease, admission_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, age, gender, contact, address, disease, admission_date))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Patient registered successfully")
            
            # Clear form
            self.clear_form()
            
            # Refresh patient list
            self.load_all_patients()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register patient: {str(e)}")
            
    def update_patient(self):
        """Update an existing patient record"""
        if not self.current_patient_id:
            messagebox.showerror("Error", "No patient selected for update")
            return
            
        # Get form data
        name = self.entries['name'].get().strip()
        age = self.entries['age'].get().strip()
        gender = self.gender_var.get()
        contact = self.entries['contact'].get().strip()
        address = self.entries['address'].get().strip()
        disease = self.entries['disease'].get().strip()
        admission_date = self.entries['admission_date'].get().strip()
        
        # Validate input
        if not all([name, age, contact, address, disease, admission_date]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        # Validate age is a number
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a valid number")
            return
            
        # Validate date format
        try:
            datetime.strptime(admission_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Admission date must be in YYYY-MM-DD format")
            return
            
        # Update database
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                UPDATE patients SET name=?, age=?, gender=?, contact=?, address=?, disease=?, admission_date=?
                WHERE id=?
            ''', (name, age, gender, contact, address, disease, admission_date, self.current_patient_id))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Patient record updated successfully")
            
            # Refresh patient list
            self.load_all_patients()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update patient: {str(e)}")
            
    def delete_patient(self):
        """Delete a patient record"""
        if not self.current_patient_id:
            messagebox.showerror("Error", "No patient selected for deletion")
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this patient record?\nThis action cannot be undone."
        )
        
        if result:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM patients WHERE id=?", (self.current_patient_id,))
                
                # Also delete related appointments and billing records
                cursor.execute("DELETE FROM appointments WHERE patient_id=?", (self.current_patient_id,))
                cursor.execute("DELETE FROM billing WHERE patient_id=?", (self.current_patient_id,))
                
                self.db_conn.commit()
                messagebox.showinfo("Success", "Patient record deleted successfully")
                
                # Clear form and disable buttons
                self.clear_form()
                self.update_btn.config(state=tk.DISABLED)
                self.delete_btn.config(state=tk.DISABLED)
                self.current_patient_id = None
                
                # Refresh patient list
                self.load_all_patients()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
                
    def clear_form(self):
        """Clear the registration form"""
        self.entries['name'].delete(0, tk.END)
        self.entries['age'].delete(0, tk.END)
        self.gender_var.set("Male")
        self.entries['contact'].delete(0, tk.END)
        self.entries['address'].delete(0, tk.END)
        self.entries['disease'].delete(0, tk.END)
        self.entries['admission_date'].delete(0, tk.END)
        self.entries['admission_date'].insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.current_patient_id = None
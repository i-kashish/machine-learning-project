import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class DoctorModule:
    def __init__(self, parent, db_conn):
        self.parent = parent
        self.db_conn = db_conn
        self.current_doctor_id = None
        
    def show(self):
        """Display the doctor module interface"""
        # Clear the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.registration_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.registration_tab, text="Doctor Registration")
        self.notebook.add(self.search_tab, text="Search Doctors")
        
        # Setup tabs
        self.setup_registration_tab()
        self.setup_search_tab()
        
    def setup_registration_tab(self):
        """Setup the doctor registration tab"""
        # Main frame for registration
        reg_frame = ttk.Frame(self.registration_tab, padding="20")
        reg_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(reg_frame, text="Doctor Registration", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Form fields
        fields = [
            ("Name:", 1),
            ("Specialty:", 2),
            ("Availability:", 3)
        ]
        
        self.entries = {}
        
        for label_text, row in fields:
            label = ttk.Label(reg_frame, text=label_text, font=("Arial", 10))
            label.grid(row=row, column=0, sticky=tk.W, pady=5)
            
            entry = ttk.Entry(reg_frame, width=30)
            entry.grid(row=row, column=1, padx=(10, 0), pady=5, sticky=tk.W)
            
            key = label_text.replace(":", "").replace("/", "_").replace(" ", "_").lower()
            self.entries[key] = entry
            
        # Availability combobox
        self.availability_var = tk.StringVar()
        availability_combo = ttk.Combobox(
            reg_frame, 
            textvariable=self.availability_var,
            values=["Monday-Friday 9AM-5PM", "Monday-Saturday 10AM-6PM", "24/7", "On Call"],
            width=28,
            state="readonly"
        )
        availability_combo.grid(row=3, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        availability_combo.set("Monday-Friday 9AM-5PM")
        self.entries['availability'] = availability_combo
        
        # Buttons frame
        button_frame = ttk.Frame(reg_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Save button
        save_btn = ttk.Button(
            button_frame,
            text="Save Doctor",
            command=self.save_doctor
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Update button
        self.update_btn = ttk.Button(
            button_frame,
            text="Update Doctor",
            command=self.update_doctor,
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
            text="Delete Doctor",
            command=self.delete_doctor,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
    def setup_search_tab(self):
        """Setup the doctor search tab"""
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
            values=["name", "specialty"],
            width=15,
            state="readonly"
        )
        search_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        self.search_entry = ttk.Entry(search_controls_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        search_btn = ttk.Button(
            search_controls_frame,
            text="Search",
            command=self.search_doctors
        )
        search_btn.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            search_controls_frame,
            text="Refresh",
            command=self.load_all_doctors
        )
        refresh_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview for displaying doctors
        tree_frame = ttk.Frame(search_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.doctor_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Specialty", "Availability"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.doctor_tree.yview)
        h_scrollbar.config(command=self.doctor_tree.xview)
        
        # Define headings
        headings = ["ID", "Name", "Specialty", "Availability"]
        for heading in headings:
            self.doctor_tree.heading(heading, text=heading)
            self.doctor_tree.column(heading, width=150)
            
        # Pack treeview and scrollbars
        self.doctor_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.doctor_tree.bind("<<TreeviewSelect>>", self.on_doctor_select)
        
        # Load all doctors initially
        self.load_all_doctors()
        
    def load_all_doctors(self):
        """Load all doctors into the treeview"""
        # Clear existing items
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
            
        # Fetch doctors from database
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM doctors ORDER BY id")
        doctors = cursor.fetchall()
        
        # Insert doctors into treeview
        for doctor in doctors:
            self.doctor_tree.insert("", tk.END, values=doctor)
            
    def search_doctors(self):
        """Search doctors based on criteria"""
        search_term = self.search_entry.get().strip()
        search_by = self.search_var.get()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
            
        # Clear existing items
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
            
        # Search in database
        cursor = self.db_conn.cursor()
        query = f"SELECT * FROM doctors WHERE {search_by} LIKE ? ORDER BY id"
        cursor.execute(query, (f"%{search_term}%",))
        doctors = cursor.fetchall()
        
        # Insert doctors into treeview
        for doctor in doctors:
            self.doctor_tree.insert("", tk.END, values=doctor)
            
        if not doctors:
            messagebox.showinfo("Info", "No doctors found matching the search criteria")
            
    def on_doctor_select(self, event):
        """Handle doctor selection from treeview"""
        selection = self.doctor_tree.selection()
        if selection:
            item = self.doctor_tree.item(selection[0])
            doctor_data = item['values']
            
            # Enable update and delete buttons
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            
            # Store current doctor ID
            self.current_doctor_id = doctor_data[0]
            
            # Populate form with doctor data
            self.populate_form(doctor_data)
            
    def populate_form(self, doctor_data):
        """Populate the registration form with doctor data"""
        # doctor_data: [id, name, specialty, availability]
        self.entries['name'].delete(0, tk.END)
        self.entries['name'].insert(0, doctor_data[1])
        
        self.entries['specialty'].delete(0, tk.END)
        self.entries['specialty'].insert(0, doctor_data[2])
        
        self.availability_var.set(doctor_data[3])
        
    def save_doctor(self):
        """Save a new doctor to the database"""
        # Get form data
        name = self.entries['name'].get().strip()
        specialty = self.entries['specialty'].get().strip()
        availability = self.availability_var.get()
        
        # Validate input
        if not all([name, specialty, availability]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        # Insert into database
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO doctors (name, specialty, availability)
                VALUES (?, ?, ?)
            ''', (name, specialty, availability))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Doctor registered successfully")
            
            # Clear form
            self.clear_form()
            
            # Refresh doctor list
            self.load_all_doctors()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register doctor: {str(e)}")
            
    def update_doctor(self):
        """Update an existing doctor record"""
        if not self.current_doctor_id:
            messagebox.showerror("Error", "No doctor selected for update")
            return
            
        # Get form data
        name = self.entries['name'].get().strip()
        specialty = self.entries['specialty'].get().strip()
        availability = self.availability_var.get()
        
        # Validate input
        if not all([name, specialty, availability]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        # Update database
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                UPDATE doctors SET name=?, specialty=?, availability=?
                WHERE id=?
            ''', (name, specialty, availability, self.current_doctor_id))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Doctor record updated successfully")
            
            # Refresh doctor list
            self.load_all_doctors()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update doctor: {str(e)}")
            
    def delete_doctor(self):
        """Delete a doctor record"""
        if not self.current_doctor_id:
            messagebox.showerror("Error", "No doctor selected for deletion")
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this doctor record?\nThis action cannot be undone."
        )
        
        if result:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM doctors WHERE id=?", (self.current_doctor_id,))
                
                # Also delete related appointments
                cursor.execute("DELETE FROM appointments WHERE doctor_id=?", (self.current_doctor_id,))
                
                self.db_conn.commit()
                messagebox.showinfo("Success", "Doctor record deleted successfully")
                
                # Clear form and disable buttons
                self.clear_form()
                self.update_btn.config(state=tk.DISABLED)
                self.delete_btn.config(state=tk.DISABLED)
                self.current_doctor_id = None
                
                # Refresh doctor list
                self.load_all_doctors()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete doctor: {str(e)}")
                
    def clear_form(self):
        """Clear the registration form"""
        self.entries['name'].delete(0, tk.END)
        self.entries['specialty'].delete(0, tk.END)
        self.availability_var.set("Monday-Friday 9AM-5PM")
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.current_doctor_id = None
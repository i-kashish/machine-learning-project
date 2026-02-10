import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

class AppointmentModule:
    def __init__(self, parent, db_conn):
        self.parent = parent
        self.db_conn = db_conn
        self.current_appointment_id = None
        
    def show(self):
        """Display the appointment module interface"""
        # Clear the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.booking_tab = ttk.Frame(self.notebook)
        self.schedule_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.booking_tab, text="Book Appointment")
        self.notebook.add(self.schedule_tab, text="Appointment Schedule")
        
        # Setup tabs
        self.setup_booking_tab()
        self.setup_schedule_tab()
        
    def setup_booking_tab(self):
        """Setup the appointment booking tab"""
        # Main frame for booking
        booking_frame = ttk.Frame(self.booking_tab, padding="20")
        booking_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(booking_frame, text="Book Appointment", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Patient selection
        patient_label = ttk.Label(booking_frame, text="Select Patient:", font=("Arial", 10))
        patient_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Patient combobox
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(
            booking_frame,
            textvariable=self.patient_var,
            width=28,
            state="readonly"
        )
        self.patient_combo.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Refresh patient list button
        refresh_patients_btn = ttk.Button(
            booking_frame,
            text="Refresh Patients",
            command=self.load_patients,
            width=15
        )
        refresh_patients_btn.grid(row=1, column=2, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Doctor selection
        doctor_label = ttk.Label(booking_frame, text="Select Doctor:", font=("Arial", 10))
        doctor_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Doctor combobox
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(
            booking_frame,
            textvariable=self.doctor_var,
            width=28,
            state="readonly"
        )
        self.doctor_combo.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Refresh doctor list button
        refresh_doctors_btn = ttk.Button(
            booking_frame,
            text="Refresh Doctors",
            command=self.load_doctors,
            width=15
        )
        refresh_doctors_btn.grid(row=2, column=2, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Appointment date
        date_label = ttk.Label(booking_frame, text="Appointment Date (YYYY-MM-DD):", font=("Arial", 10))
        date_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.date_entry = ttk.Entry(booking_frame, width=30)
        self.date_entry.grid(row=3, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Set tomorrow's date as default
        tomorrow = datetime.now() + timedelta(days=1)
        self.date_entry.insert(0, tomorrow.strftime("%Y-%m-%d"))
        
        # Buttons frame
        button_frame = ttk.Frame(booking_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Book button
        book_btn = ttk.Button(
            button_frame,
            text="Book Appointment",
            command=self.book_appointment
        )
        book_btn.pack(side=tk.LEFT, padx=5)
        
        # Update button
        self.update_btn = ttk.Button(
            button_frame,
            text="Update Appointment",
            command=self.update_appointment,
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
            text="Delete Appointment",
            command=self.delete_appointment,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.load_patients()
        self.load_doctors()
        
    def setup_schedule_tab(self):
        """Setup the appointment schedule tab"""
        # Main frame for schedule
        schedule_frame = ttk.Frame(self.schedule_tab, padding="20")
        schedule_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search controls
        search_controls_frame = ttk.Frame(schedule_frame)
        search_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_controls_frame, text="Search by:").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar(value="doctor")
        search_combo = ttk.Combobox(
            search_controls_frame,
            textvariable=self.search_var,
            values=["doctor", "patient", "date"],
            width=15,
            state="readonly"
        )
        search_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        self.search_entry = ttk.Entry(search_controls_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        search_btn = ttk.Button(
            search_controls_frame,
            text="Search",
            command=self.search_appointments
        )
        search_btn.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            search_controls_frame,
            text="Refresh",
            command=self.load_all_appointments
        )
        refresh_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview for displaying appointments
        tree_frame = ttk.Frame(schedule_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.appointment_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Patient", "Doctor", "Date", "Status"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.appointment_tree.yview)
        h_scrollbar.config(command=self.appointment_tree.xview)
        
        # Define headings
        headings = ["ID", "Patient", "Doctor", "Date", "Status"]
        for heading in headings:
            self.appointment_tree.heading(heading, text=heading)
            self.appointment_tree.column(heading, width=150)
            
        # Pack treeview and scrollbars
        self.appointment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.appointment_tree.bind("<<TreeviewSelect>>", self.on_appointment_select)
        
        # Load all appointments initially
        self.load_all_appointments()
        
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
        
    def load_all_appointments(self):
        """Load all appointments into the treeview"""
        # Clear existing items
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
            
        # Fetch appointments from database with patient and doctor names
        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT a.id, p.name, d.name, a.appointment_date, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appointment_date
        ''')
        appointments = cursor.fetchall()
        
        # Insert appointments into treeview
        for appointment in appointments:
            self.appointment_tree.insert("", tk.END, values=appointment)
            
    def search_appointments(self):
        """Search appointments based on criteria"""
        search_term = self.search_entry.get().strip()
        search_by = self.search_var.get()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
            
        # Clear existing items
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
            
        # Search in database
        cursor = self.db_conn.cursor()
        
        if search_by == "doctor":
            query = '''
                SELECT a.id, p.name, d.name, a.appointment_date, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                WHERE d.name LIKE ?
                ORDER BY a.appointment_date
            '''
        elif search_by == "patient":
            query = '''
                SELECT a.id, p.name, d.name, a.appointment_date, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                WHERE p.name LIKE ?
                ORDER BY a.appointment_date
            '''
        else:  # date
            query = '''
                SELECT a.id, p.name, d.name, a.appointment_date, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                WHERE a.appointment_date LIKE ?
                ORDER BY a.appointment_date
            '''
            
        cursor.execute(query, (f"%{search_term}%",))
        appointments = cursor.fetchall()
        
        # Insert appointments into treeview
        for appointment in appointments:
            self.appointment_tree.insert("", tk.END, values=appointment)
            
        if not appointments:
            messagebox.showinfo("Info", "No appointments found matching the search criteria")
            
    def on_appointment_select(self, event):
        """Handle appointment selection from treeview"""
        selection = self.appointment_tree.selection()
        if selection:
            item = self.appointment_tree.item(selection[0])
            appointment_data = item['values']
            
            # Enable update and delete buttons
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            
            # Store current appointment ID
            self.current_appointment_id = appointment_data[0]
            
            # Populate form with appointment data
            self.populate_form(appointment_data)
            
    def populate_form(self, appointment_data):
        """Populate the booking form with appointment data"""
        # appointment_data: [id, patient_name, doctor_name, date, status]
        
        # Find and select patient
        patient_name = appointment_data[1]
        patient_values = self.patient_combo['values']
        for value in patient_values:
            if patient_name in value:
                self.patient_combo.set(value)
                break
                
        # Find and select doctor
        doctor_name = appointment_data[2]
        doctor_values = self.doctor_combo['values']
        for value in doctor_values:
            if doctor_name in value:
                self.doctor_combo.set(value)
                break
                
        # Set date
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, appointment_data[3])
        
    def book_appointment(self):
        """Book a new appointment"""
        # Get form data
        patient_id = self.get_selected_patient_id()
        doctor_id = self.get_selected_doctor_id()
        appointment_date = self.date_entry.get().strip()
        
        # Validate input
        if not all([patient_id, doctor_id, appointment_date]):
            messagebox.showerror("Error", "Please select patient, doctor, and enter appointment date")
            return
            
        # Validate date format
        try:
            datetime.strptime(appointment_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Appointment date must be in YYYY-MM-DD format")
            return
            
        # Insert into database
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO appointments (patient_id, doctor_id, appointment_date)
                VALUES (?, ?, ?)
            ''', (patient_id, doctor_id, appointment_date))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Appointment booked successfully")
            
            # Clear form
            self.clear_form()
            
            # Refresh appointment list
            self.load_all_appointments()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book appointment: {str(e)}")
            
    def update_appointment(self):
        """Update an existing appointment"""
        if not self.current_appointment_id:
            messagebox.showerror("Error", "No appointment selected for update")
            return
            
        # Get form data
        patient_id = self.get_selected_patient_id()
        doctor_id = self.get_selected_doctor_id()
        appointment_date = self.date_entry.get().strip()
        
        # Validate input
        if not all([patient_id, doctor_id, appointment_date]):
            messagebox.showerror("Error", "Please select patient, doctor, and enter appointment date")
            return
            
        # Validate date format
        try:
            datetime.strptime(appointment_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Appointment date must be in YYYY-MM-DD format")
            return
            
        # Update database
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                UPDATE appointments 
                SET patient_id=?, doctor_id=?, appointment_date=?
                WHERE id=?
            ''', (patient_id, doctor_id, appointment_date, self.current_appointment_id))
            
            self.db_conn.commit()
            messagebox.showinfo("Success", "Appointment updated successfully")
            
            # Refresh appointment list
            self.load_all_appointments()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update appointment: {str(e)}")
            
    def delete_appointment(self):
        """Delete an appointment"""
        if not self.current_appointment_id:
            messagebox.showerror("Error", "No appointment selected for deletion")
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this appointment?\nThis action cannot be undone."
        )
        
        if result:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM appointments WHERE id=?", (self.current_appointment_id,))
                
                self.db_conn.commit()
                messagebox.showinfo("Success", "Appointment deleted successfully")
                
                # Clear form and disable buttons
                self.clear_form()
                self.update_btn.config(state=tk.DISABLED)
                self.delete_btn.config(state=tk.DISABLED)
                self.current_appointment_id = None
                
                # Refresh appointment list
                self.load_all_appointments()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete appointment: {str(e)}")
                
    def clear_form(self):
        """Clear the booking form"""
        # Reset comboboxes to first values
        patient_values = self.patient_combo['values']
        if patient_values:
            self.patient_combo.set(patient_values[0])
            
        doctor_values = self.doctor_combo['values']
        if doctor_values:
            self.doctor_combo.set(doctor_values[0])
            
        # Set tomorrow's date as default
        tomorrow = datetime.now() + timedelta(days=1)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, tomorrow.strftime("%Y-%m-%d"))
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.current_appointment_id = None
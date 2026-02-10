import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class FinancialModule:
    def __init__(self, parent, db_conn):
        self.parent = parent
        self.db_conn = db_conn
        
    def show(self):
        """Display the financial overview module interface"""
        # Clear the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.overview_tab = ttk.Frame(self.notebook)
        self.bills_tab = ttk.Frame(self.notebook)
        self.salaries_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.overview_tab, text="Financial Overview")
        self.notebook.add(self.bills_tab, text="All Bills")
        self.notebook.add(self.salaries_tab, text="All Salaries")
        
        # Setup tabs
        self.setup_overview_tab()
        self.setup_bills_tab()
        self.setup_salaries_tab()
        
    def setup_overview_tab(self):
        """Setup the financial overview tab"""
        # Main frame for overview
        overview_frame = ttk.Frame(self.overview_tab, padding="20")
        overview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(overview_frame, text="Financial Overview", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Create frames for bills and salaries summary
        bills_frame = ttk.LabelFrame(overview_frame, text="Billing Summary", padding="10")
        bills_frame.pack(fill=tk.X, pady=(0, 20))
        
        salaries_frame = ttk.LabelFrame(overview_frame, text="Salary Summary", padding="10")
        salaries_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Get billing summary
        cursor = self.db_conn.cursor()
        
        # Total bills and revenue
        cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM billing")
        bill_count, total_revenue = cursor.fetchone()
        total_revenue = total_revenue or 0
        
        # Paid bills and revenue
        cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM billing WHERE payment_status='Paid'")
        paid_count, paid_revenue = cursor.fetchone()
        paid_revenue = paid_revenue or 0
        
        # Unpaid bills and revenue
        cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM billing WHERE payment_status='Unpaid'")
        unpaid_count, unpaid_revenue = cursor.fetchone()
        unpaid_revenue = unpaid_revenue or 0
        
        # Display billing summary
        ttk.Label(bills_frame, text=f"Total Bills: {bill_count}", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(bills_frame, text=f"Total Revenue: ₹{total_revenue:.2f}", font=("Arial", 10)).grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Label(bills_frame, text=f"Paid Bills: {paid_count}", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(bills_frame, text=f"Paid Revenue: ₹{paid_revenue:.2f}", font=("Arial", 10)).grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Label(bills_frame, text=f"Unpaid Bills: {unpaid_count}", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(bills_frame, text=f"Unpaid Revenue: ₹{unpaid_revenue:.2f}", font=("Arial", 10)).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Get salary summary
        cursor.execute("SELECT COUNT(*), SUM(salary_amount) FROM doctor_salary")
        salary_count, total_salary = cursor.fetchone()
        total_salary = total_salary or 0
        
        # Paid salaries and amount
        cursor.execute("SELECT COUNT(*), SUM(salary_amount) FROM doctor_salary WHERE payment_status='Paid'")
        paid_salary_count, paid_salary_amount = cursor.fetchone()
        paid_salary_amount = paid_salary_amount or 0
        
        # Unpaid salaries and amount
        cursor.execute("SELECT COUNT(*), SUM(salary_amount) FROM doctor_salary WHERE payment_status='Unpaid'")
        unpaid_salary_count, unpaid_salary_amount = cursor.fetchone()
        unpaid_salary_amount = unpaid_salary_amount or 0
        
        # Display salary summary
        ttk.Label(salaries_frame, text=f"Total Salaries: {salary_count}", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(salaries_frame, text=f"Total Salary Amount: ₹{total_salary:.2f}", font=("Arial", 10)).grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Label(salaries_frame, text=f"Paid Salaries: {paid_salary_count}", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(salaries_frame, text=f"Paid Salary Amount: ₹{paid_salary_amount:.2f}", font=("Arial", 10)).grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Label(salaries_frame, text=f"Unpaid Salaries: {unpaid_salary_count}", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(salaries_frame, text=f"Unpaid Salary Amount: ₹{unpaid_salary_amount:.2f}", font=("Arial", 10)).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Net financial position
        net_position = paid_revenue - paid_salary_amount
        position_text = "Profit" if net_position >= 0 else "Loss"
        position_color = "green" if net_position >= 0 else "red"
        
        net_frame = ttk.LabelFrame(overview_frame, text="Net Financial Position", padding="10")
        net_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(net_frame, text=f"Net {position_text}: ₹{abs(net_position):.2f}", font=("Arial", 12, "bold"), foreground=position_color).pack()
        
        # Refresh button
        refresh_btn = ttk.Button(overview_frame, text="Refresh", command=self.refresh_overview)
        refresh_btn.pack(pady=(10, 0))
        
    def refresh_overview(self):
        """Refresh the financial overview"""
        # Clear the overview tab
        for widget in self.overview_tab.winfo_children():
            widget.destroy()
            
        # Setup the overview tab again
        self.setup_overview_tab()
        
    def setup_bills_tab(self):
        """Setup the all bills tab"""
        # Main frame for bills
        bills_frame = ttk.Frame(self.bills_tab, padding="20")
        bills_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(bills_frame, text="All Patient Bills", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Treeview for displaying bills
        tree_frame = ttk.Frame(bills_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.bills_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Patient", "Amount", "Status", "Method", "Billing Date", "Payment Date"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.bills_tree.yview)
        h_scrollbar.config(command=self.bills_tree.xview)
        
        # Define headings
        headings = ["ID", "Patient", "Amount", "Status", "Method", "Billing Date", "Payment Date"]
        for i, heading in enumerate(headings):
            self.bills_tree.heading(heading, text=heading)
            # Set column widths
            widths = [50, 150, 100, 100, 100, 100, 100]
            self.bills_tree.column(heading, width=widths[i])
            
        # Pack treeview and scrollbars
        self.bills_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Buttons frame
        buttons_frame = ttk.Frame(bills_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Refresh button
        refresh_btn = ttk.Button(buttons_frame, text="Refresh", command=self.load_all_bills)
        refresh_btn.pack(side=tk.LEFT)
        
        # Load all bills
        self.load_all_bills()
        
    def setup_salaries_tab(self):
        """Setup the all salaries tab"""
        # Main frame for salaries
        salaries_frame = ttk.Frame(self.salaries_tab, padding="20")
        salaries_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(salaries_frame, text="All Doctor Salaries", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Treeview for displaying salaries
        tree_frame = ttk.Frame(salaries_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.salaries_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Doctor", "Amount", "Status", "Method", "Month", "Year", "Payment Date"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.salaries_tree.yview)
        h_scrollbar.config(command=self.salaries_tree.xview)
        
        # Define headings
        headings = ["ID", "Doctor", "Amount", "Status", "Method", "Month", "Year", "Payment Date"]
        for i, heading in enumerate(headings):
            self.salaries_tree.heading(heading, text=heading)
            # Set column widths
            widths = [50, 150, 100, 100, 100, 80, 80, 100]
            self.salaries_tree.column(heading, width=widths[i])
            
        # Pack treeview and scrollbars
        self.salaries_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Buttons frame
        buttons_frame = ttk.Frame(salaries_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Refresh button
        refresh_btn = ttk.Button(buttons_frame, text="Refresh", command=self.load_all_salaries)
        refresh_btn.pack(side=tk.LEFT)
        
        # Load all salaries
        self.load_all_salaries()
        
    def load_all_bills(self):
        """Load all bills into the treeview"""
        # Clear existing items
        for item in self.bills_tree.get_children():
            self.bills_tree.delete(item)
            
        # Fetch bills from database with patient names
        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT b.id, p.name, b.total_amount, b.payment_status, b.payment_method, b.billing_date, b.payment_date
            FROM billing b
            JOIN patients p ON b.patient_id = p.id
            ORDER BY b.billing_date DESC
        ''')
        bills = cursor.fetchall()
        
        # Insert bills into treeview
        for bill in bills:
            self.bills_tree.insert("", tk.END, values=bill)
            
    def load_all_salaries(self):
        """Load all salaries into the treeview"""
        # Clear existing items
        for item in self.salaries_tree.get_children():
            self.salaries_tree.delete(item)
            
        # Fetch salaries from database with doctor names
        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT s.id, d.name, s.salary_amount, s.payment_status, s.payment_method, s.salary_month, s.salary_year, s.payment_date
            FROM doctor_salary s
            JOIN doctors d ON s.doctor_id = d.id
            ORDER BY s.salary_year DESC, s.salary_month DESC
        ''')
        salaries = cursor.fetchall()
        
        # Insert salaries into treeview
        for salary in salaries:
            self.salaries_tree.insert("", tk.END, values=salary)
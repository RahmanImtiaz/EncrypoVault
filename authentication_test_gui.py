import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from datetime import datetime

# Add src directory to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

# Import our modules
from src.Account import Account
from src.AccountType import Beginner, Advanced, Tester
from src.AuthenticationManager import AuthenticationManager
from src.AccountsFileManager import AccountsFileManager
from src.AuditLog import AuditLog
from src.User import User  # Import User class

class AuthenticationTestGUI:
    """Test GUI for EncryptoVault Authentication"""
    def __init__(self, root):
        self.root = root
        self.root.title("Authentication Test GUI")
        self.root.geometry("720x600")
        
        # Initialize backend components
        self.auth_manager = AuthenticationManager.get_instance()
        self.file_manager = AccountsFileManager.get_instance()
        self.audit_log = AuditLog.get_instance()
        self.user = User()  # Create User instance
        self.current_account = None
        
        # Monkey patch authentication components for testing
        self.patch_authentication()
        
        # Setup UI
        self.setup_ui()
    
    def patch_authentication(self):
        """
        Patch authentication components to allow testing without secure boot,
        biometrics, etc.
        """
        # Override prompt methods for testing
        AuthenticationManager.prompt_for_password = lambda self: self.test_password.encode()
        AuthenticationManager.prompt_for_biometrics = lambda self: b"test_biometric_data"
        AuthenticationManager.ensure_secure_boot = lambda self: True
        
        # Create a test attribute to store password for testing
        self.auth_manager.test_password = "test_password"
        
        # Patch the AuditLog.get_entries_in_range method to provide a count method
        original_get_entries = self.audit_log.get_entries_in_range
        
        def patched_get_entries_in_range(start_time, end_time):
            result = original_get_entries(start_time, end_time)
            # Add a count method that returns the number of failed logins
            result.count = lambda: sum(1 for entry in result.values() if entry['status'] == 'FAILED')
            return result
        
        # Replace the method with our patched version
        self.audit_log.get_entries_in_range = patched_get_entries_in_range
        
    
    def setup_ui(self):
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_tab = ttk.Frame(self.notebook)
        self.auth_tab = ttk.Frame(self.notebook)
        self.file_tab = ttk.Frame(self.notebook) 
        self.audit_tab = ttk.Frame(self.notebook)
        self.simulation_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.create_tab, text="Create Account")
        self.notebook.add(self.auth_tab, text="Authentication")
        self.notebook.add(self.file_tab, text="File Operations")
        self.notebook.add(self.audit_tab, text="Audit Log")
        self.notebook.add(self.simulation_tab, text="Full Simulation")
        
        
        # Setup each tab
        self.setup_create_tab()
        self.setup_auth_tab()
        self.setup_file_tab()
        self.setup_audit_tab()
        self.setup_simulation_tab()
        
        # Status bar at bottom
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_create_tab(self):
        # Account creation frame
        create_frame = ttk.LabelFrame(self.create_tab, text="Create Account")
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(create_frame, text="Account Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.create_name_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.create_name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(create_frame, text="Secret Key:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.create_key_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.create_key_var, show="*").grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(create_frame, text="Account Type:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.account_type_var = tk.StringVar(value="Beginner")
        ttk.Combobox(create_frame, textvariable=self.account_type_var, 
                    values=["Beginner", "Advanced", "Tester"]).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(create_frame, text="Create Account", command=self.create_account).grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Account modification frame
        manage_frame = ttk.LabelFrame(self.create_tab, text="Manage Account")
        manage_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(manage_frame, text="Add Contact:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(manage_frame, text="Contact Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.contact_name_var = tk.StringVar()
        ttk.Entry(manage_frame, textvariable=self.contact_name_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(manage_frame, text="Contact Address:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.contact_address_var = tk.StringVar()
        ttk.Entry(manage_frame, textvariable=self.contact_address_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(manage_frame, text="Add Contact", command=self.add_contact).grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Account info frame
        self.account_info_frame = ttk.LabelFrame(self.create_tab, text="Account Information")
        self.account_info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.account_info_text = tk.Text(self.account_info_frame, height=10, width=50)
        self.account_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.account_info_text.config(state=tk.DISABLED)
        
        ttk.Button(self.account_info_frame, text="Refresh Account Info", 
                  command=self.update_account_info).pack(pady=5)

    def setup_auth_tab(self):
        # Authentication frame
        auth_frame = ttk.LabelFrame(self.auth_tab, text="Authenticate")
        auth_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(auth_frame, text="Account Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.auth_name_var = tk.StringVar()
        ttk.Entry(auth_frame, textvariable=self.auth_name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(auth_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.auth_password_var = tk.StringVar()
        ttk.Entry(auth_frame, textvariable=self.auth_password_var, show="*").grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(auth_frame, text="Authenticate", command=self.authenticate_account).grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(auth_frame, text="Simulate Failed Auth", command=self.simulate_failed_auth).grid(row=2, column=1, padx=5, pady=10)
        
        # Authentication status frame
        status_frame = ttk.LabelFrame(self.auth_tab, text="Authentication Status")
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.auth_status_text = tk.Text(status_frame, height=10, width=50)
        self.auth_status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.auth_status_text.config(state=tk.DISABLED)

    def setup_file_tab(self):
        # File operations frame
        file_frame = ttk.LabelFrame(self.file_tab, text="File Operations")
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(file_frame, text="Save Current Account", command=self.save_account).pack(pady=5, padx=5, fill=tk.X)
        ttk.Button(file_frame, text="Load Account", command=self.load_account).pack(pady=5, padx=5, fill=tk.X)
        
        # File testing frame
        test_frame = ttk.LabelFrame(self.file_tab, text="Encryption/Decryption Testing")
        test_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(test_frame, text="Test Content:").pack(padx=5, pady=5, anchor=tk.W)
        
        self.test_content = tk.Text(test_frame, height=5, width=50)
        self.test_content.pack(fill=tk.X, padx=5, pady=5)
        self.test_content.insert(tk.END, "Type some test content here to encrypt/decrypt...")
        
        ttk.Label(test_frame, text="Password for encryption:").pack(padx=5, pady=5, anchor=tk.W)
        self.test_key_var = tk.StringVar(value="test_password")
        ttk.Entry(test_frame, textvariable=self.test_key_var).pack(fill=tk.X, padx=5, pady=5)
        
        button_frame = ttk.Frame(test_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        ttk.Button(button_frame, text="Test Encrypt", command=self.test_encrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Test Decrypt", command=self.test_decrypt).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(test_frame, text="Result:").pack(padx=5, pady=5, anchor=tk.W)
        self.test_result = tk.Text(test_frame, height=5, width=50)
        self.test_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.test_result.config(state=tk.DISABLED)

    def setup_audit_tab(self):
        # Audit log frame
        audit_frame = ttk.LabelFrame(self.audit_tab, text="Audit Log")
        audit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.audit_text = tk.Text(audit_frame, height=20, width=60)
        self.audit_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.audit_text.config(state=tk.DISABLED)
        
        ttk.Button(audit_frame, text="Refresh Audit Log", 
                  command=self.refresh_audit_log).pack(pady=5)
        
    # Add this method to your AuthenticationTestGUI class after setup_audit_tab():

    def setup_simulation_tab(self):
        """Set up the full authentication simulation tab"""
        sim_frame = ttk.LabelFrame(self.simulation_tab, text="Authentication Simulation")
        sim_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for auth/register tabs within simulation
        sim_notebook = ttk.Notebook(sim_frame)
        sim_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create auth and register tabs
        auth_tab = ttk.Frame(sim_notebook)
        register_tab = ttk.Frame(sim_notebook)
        
        sim_notebook.add(auth_tab, text="Authentication")
        sim_notebook.add(register_tab, text="Register New Account")
        
        # Setup authentication tab
        self.setup_auth_simulation(auth_tab)
        
        # Setup register tab
        self.setup_register_simulation(register_tab)

    def setup_auth_simulation(self, parent_frame):
        """Setup the authentication part of the simulation tab"""
        # Secure Boot Section
        secure_frame = ttk.LabelFrame(parent_frame, text="Secure Boot Verification")
        secure_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.secure_boot_var = tk.StringVar(value="Pending...")
        ttk.Label(secure_frame, text="Secure Boot Status:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(secure_frame, textvariable=self.secure_boot_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(secure_frame, text="Verify Secure Boot", 
                command=self.verify_secure_boot).grid(row=0, column=2, padx=5, pady=5)
        
        # Account Selection Section
        account_frame = ttk.LabelFrame(parent_frame, text="Account Selection")
        account_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(account_frame, text="Available Accounts:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.account_listbox = tk.Listbox(account_frame, height=5)
        self.account_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Button(account_frame, text="Select Directory", 
                command=self.select_accounts_directory).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(account_frame, text="Refresh List", 
                command=self.refresh_account_list).grid(row=2, column=1, padx=5, pady=5)
        
        # Credentials Section
        creds_frame = ttk.LabelFrame(parent_frame, text="Authentication Credentials")
        creds_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(creds_frame, text="Passphrase:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.sim_password_var = tk.StringVar()
        ttk.Entry(creds_frame, textvariable=self.sim_password_var, show="*").grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(creds_frame, text="Biometric Data:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Button(creds_frame, text="Simulate Biometric Scan", 
                command=self.simulate_biometric_scan).grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.biometric_status_var = tk.StringVar(value="Not scanned")
        ttk.Label(creds_frame, textvariable=self.biometric_status_var).grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Authentication Button
        ttk.Button(parent_frame, text="Authenticate Account", command=self.run_full_authentication,
                style="Accent.TButton").pack(padx=10, pady=15, fill=tk.X)
        
        # Results Section
        results_frame = ttk.LabelFrame(parent_frame, text="Authentication Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.sim_results = tk.Text(results_frame, height=8, width=50)
        self.sim_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.sim_results.config(state=tk.DISABLED)

    def setup_register_simulation(self, parent_frame):
        """Setup the registration part of the simulation tab"""
        # Account Details Section
        details_frame = ttk.LabelFrame(parent_frame, text="Account Details")
        details_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(details_frame, text="Account Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_name_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.reg_name_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(details_frame, text="Secret Key (for account):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_secret_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.reg_secret_var, show="*").grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(details_frame, text="Account Type:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_type_var = tk.StringVar(value="Beginner")
        ttk.Combobox(details_frame, textvariable=self.reg_type_var, 
                    values=["Beginner", "Advanced", "Tester"]).grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Authentication Section (new)
        auth_frame = ttk.LabelFrame(parent_frame, text="Authentication Settings")
        auth_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(auth_frame, text="Authentication Password:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_auth_pass_var = tk.StringVar()
        ttk.Entry(auth_frame, textvariable=self.reg_auth_pass_var, show="*").grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(auth_frame, text="Confirm Auth Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_confirm_auth_var = tk.StringVar()
        ttk.Entry(auth_frame, textvariable=self.reg_confirm_auth_var, show="*").grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(auth_frame, text="Note:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        note_text = "This password is used for encryption and authentication.\nIt's different from the secret key stored in the account."
        ttk.Label(auth_frame, text=note_text, foreground="blue").grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Security Section
        security_frame = ttk.LabelFrame(parent_frame, text="Security Settings")
        security_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(security_frame, text="Biometric Verification:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_biometric_var = tk.StringVar(value="Not enrolled")
        ttk.Label(security_frame, textvariable=self.reg_biometric_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(security_frame, text="Enroll Biometrics", 
                command=self.enroll_biometrics).grid(row=0, column=2, padx=5, pady=5)
        
        # Save Location Section
        save_frame = ttk.LabelFrame(parent_frame, text="Save Location")
        save_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.reg_location_var = tk.StringVar(value=self.file_manager.current_directory)
        ttk.Label(save_frame, text="Save Directory:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(save_frame, textvariable=self.reg_location_var, width=40).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(save_frame, text="Browse...", 
                command=self.select_reg_directory).grid(row=0, column=2, padx=5, pady=5)
        
        # Register Button
        ttk.Button(parent_frame, text="Register New Account", 
                command=self.register_new_account,
                style="Accent.TButton").pack(padx=10, pady=15, fill=tk.X)
        
        # Registration Results
        results_frame = ttk.LabelFrame(parent_frame, text="Registration Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.reg_results = tk.Text(results_frame, height=8, width=50)
        self.reg_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.reg_results.config(state=tk.DISABLED)
        
    def enroll_biometrics(self):
        """Simulate biometric enrollment process"""
        self.reg_biometric_var.set("Scanning...")
        self.root.update_idletasks()
        
        # Simulate enrollment process taking time
        self.root.after(2000)
        
        # Set to enrolled
        self.reg_biometric_var.set("✓ Enrolled")
        self.status_var.set("Biometric data enrolled successfully")

    def select_reg_directory(self):
        """Select directory for saving new account"""
        dir_path = filedialog.askdirectory(
            title="Select Directory to Save Account",
            initialdir=self.file_manager.current_directory
        )
        
        if dir_path:  # User selected a directory
            self.reg_location_var.set(dir_path)
            self.status_var.set(f"Selected save directory: {dir_path}")

    def register_new_account(self):
        """Process new account registration"""
        try:
            # Get form data
            account_name = self.reg_name_var.get()
            secret_key = self.reg_secret_var.get()
            auth_password = self.reg_auth_pass_var.get()
            confirm_auth = self.reg_confirm_auth_var.get()
            account_type_str = self.reg_type_var.get()
            save_dir = self.reg_location_var.get()
            
            # Validate inputs
            if not account_name or not auth_password:
                messagebox.showerror("Error", "Account name and authentication password are required")
                return
            
            if auth_password != confirm_auth:
                messagebox.showerror("Error", "Authentication passwords do not match")
                return
                
            if self.reg_biometric_var.get() != "✓ Enrolled":
                messagebox.showerror("Error", "Biometrics must be enrolled")
                return
            
            # Update UI
            self.reg_results.config(state=tk.NORMAL)
            self.reg_results.delete(1.0, tk.END)
            self.reg_results.insert(tk.END, "Creating account...\n")
            self.reg_results.config(state=tk.DISABLED)
            self.root.update_idletasks()
            
            # Create account type
            if account_type_str == "Beginner":
                account_type = Beginner()
            elif account_type_str == "Advanced":
                account_type = Advanced()
            else:
                account_type = Tester()
            
            # Create account directly
            account = Account(account_type=account_type)
            account.set_account_name(account_name)
            account.set_secret_key(secret_key or "")
            
            # Generate encryption key directly (don't rely on User.register)
            password = auth_password.encode()
            biometric = b"test_biometric_data"
            encryption_key = self.auth_manager._generate_key(password, biometric)
            
            # Set encryption key on account
            account.set_encryption_key(encryption_key)
            
            # Save account using temporary directory
            old_dir = self.file_manager.current_directory
            self.file_manager.current_directory = save_dir
            self.file_manager.save_account(account)
            
            # Reset directory
            self.file_manager.current_directory = old_dir
            
            # Add to audit log
            self.audit_log.add_entry(account_name, datetime.now(), "ACCOUNT_CREATED")
            
            # Set as current account
            self.current_account = account
            
            # Update UI with success
            self.reg_results.config(state=tk.NORMAL)
            self.reg_results.delete(1.0, tk.END)
            self.reg_results.insert(tk.END, f"✓ Account registered successfully\n\n")
            self.reg_results.insert(tk.END, f"Account Name: {account.get_account_name()}\n")
            self.reg_results.insert(tk.END, f"Account Type: {account.get_account_type().get_type_name()}\n")
            self.reg_results.insert(tk.END, f"Transaction Limit: {account.get_account_type().get_transaction_limit()}\n")
            self.reg_results.insert(tk.END, f"Uses Real Funds: {account.get_account_type().uses_real_funds()}\n")
            self.reg_results.insert(tk.END, f"Saved to: {save_dir}\n")
            self.reg_results.insert(tk.END, f"\nNote: Use your authentication password (not secret key)\n")
            self.reg_results.insert(tk.END, f"when authenticating this account in the future.\n")
            self.reg_results.config(state=tk.DISABLED)
            
            # Update account info and refresh list
            self.update_account_info()
            self.refresh_account_list()
            self.status_var.set(f"Account '{account_name}' registered successfully")
                
        except Exception as e:
            self.reg_results.config(state=tk.NORMAL)
            self.reg_results.delete(1.0, tk.END)
            self.reg_results.insert(tk.END, f"✗ Registration failed\n\n")
            self.reg_results.insert(tk.END, f"Error: {str(e)}\n")
            self.reg_results.config(state=tk.DISABLED)
            messagebox.showerror("Error", str(e))
                
    def verify_secure_boot(self):
        """Simulate secure boot verification"""
        self.secure_boot_var.set("Checking...")
        self.root.update_idletasks()
        
        # Simulate processing time
        self.root.after(1000)
        
        # Call the actual secure boot check but override for testing
        original_method = self.auth_manager.ensure_secure_boot
        try:
            # For testing, we'll make it succeed
            self.auth_manager.ensure_secure_boot = lambda: True
            result = self.auth_manager.ensure_secure_boot()
            
            if result:
                self.secure_boot_var.set("✓ Verified")
                self.status_var.set("Secure boot verification successful")
            else:
                self.secure_boot_var.set("✗ Failed")
                self.status_var.set("Secure boot verification failed")
        finally:
            # Restore original method
            self.auth_manager.ensure_secure_boot = original_method

    def select_accounts_directory(self):
        """Select directory containing account files"""
        dir_path = filedialog.askdirectory(
            title="Select Directory with Account Files",
            initialdir=self.file_manager.current_directory
        )
        
        if dir_path:  # User selected a directory
            self.file_manager.current_directory = dir_path
            self.refresh_account_list()
            self.status_var.set(f"Selected directory: {dir_path}")

    def refresh_account_list(self):
        """Refresh the list of available account files"""
        self.account_listbox.delete(0, tk.END)
        
        try:
            # Find all .enc files in the current directory
            for file in os.listdir(self.file_manager.current_directory):
                if file.endswith(".enc"):
                    account_name = os.path.splitext(file)[0]
                    self.account_listbox.insert(tk.END, account_name)
            
            self.status_var.set(f"Found {self.account_listbox.size()} account files")
        except Exception as e:
            self.status_var.set(f"Error listing accounts: {str(e)}")

    def simulate_biometric_scan(self):
        """Simulate biometric scanning"""
        self.biometric_status_var.set("Scanning...")
        self.root.update_idletasks()
        
        # Simulate scan taking time
        self.root.after(1500)
        
        # Set to scanned
        self.biometric_status_var.set("✓ Scanned")
        self.status_var.set("Biometric data scanned successfully")

    def run_full_authentication(self):
        """Run the full authentication process simulation"""
        # Check if secure boot is verified
        if self.secure_boot_var.get() != "✓ Verified":
            messagebox.showerror("Error", "Secure boot must be verified first")
            return
        
        # Check if an account is selected
        if not self.account_listbox.curselection():
            messagebox.showerror("Error", "Please select an account file")
            return
        
        # Get selected account
        selected_account = self.account_listbox.get(self.account_listbox.curselection()[0])
        
        # Get passphrase
        passphrase = self.sim_password_var.get()
        if not passphrase:
            messagebox.showerror("Error", "Please enter a passphrase")
            return
        
        # Check if biometric data is scanned
        if self.biometric_status_var.get() != "✓ Scanned":
            messagebox.showerror("Error", "Biometric data must be scanned first")
            return
        
        # Update UI to show authentication in progress
        self.sim_results.config(state=tk.NORMAL)
        self.sim_results.delete(1.0, tk.END)
        self.sim_results.insert(tk.END, "Authentication in progress...\n")
        self.sim_results.config(state=tk.DISABLED)
        self.root.update_idletasks()
        
        # Add debug logging
        print(f"Attempting to authenticate account: {selected_account}")
        print(f"Using passphrase: {passphrase}")
        
        # Override password method for testing
        self.auth_manager.test_password = passphrase
        
        try:
            # Simulate a delay for authentication
            self.root.after(1000)
            
            # Direct authentication instead of using User.login()
            auth_manager = AuthenticationManager.get_instance()
            file_manager = AccountsFileManager.get_instance()
            
            # Generate key with password and biometrics
            password = passphrase.encode()
            biometrics = b"test_biometric_data"
            decryption_key = auth_manager._generate_key(password, biometrics)
            
            # Try to decrypt and load account
            try:
                account = file_manager.load_account(decryption_key, selected_account)
                
                if account:
                    # Authentication successful
                    self.current_account = account
                    
                    # Update UI
                    self.sim_results.config(state=tk.NORMAL)
                    self.sim_results.delete(1.0, tk.END)
                    self.sim_results.insert(tk.END, f"✓ Authentication successful\n\n")
                    self.sim_results.insert(tk.END, f"Account Name: {account.get_account_name()}\n")
                    self.sim_results.insert(tk.END, f"Account Type: {account.get_account_type().get_type_name()}\n")
                    self.sim_results.insert(tk.END, f"Transaction Limit: {account.get_account_type().get_transaction_limit()}\n")
                    self.sim_results.insert(tk.END, f"Uses Real Funds: {account.get_account_type().uses_real_funds()}\n")
                    self.sim_results.config(state=tk.DISABLED)
                    
                    self.update_account_info()
                    self.status_var.set(f"Successfully authenticated as {selected_account}")
                    
                    # Log success
                    self.audit_log.add_entry(selected_account, datetime.now(), "SUCCESS")
                    
                    # Switch to the Account tab to show details
                    self.notebook.select(self.create_tab)
                else:
                    # Authentication failed
                    self.sim_results.config(state=tk.NORMAL)
                    self.sim_results.delete(1.0, tk.END)
                    self.sim_results.insert(tk.END, f"✗ Authentication failed\n\n")
                    self.sim_results.insert(tk.END, f"Error: Invalid credentials\n")
                    self.sim_results.config(state=tk.DISABLED)
                    
                    # Log failure
                    self.audit_log.add_entry(selected_account, datetime.now(), "FAILED")
                    self.status_var.set(f"Authentication failed for {selected_account}")
            except Exception as e:
                # Authentication error
                self.sim_results.config(state=tk.NORMAL)
                self.sim_results.delete(1.0, tk.END)
                self.sim_results.insert(tk.END, f"✗ Authentication failed\n\n")
                self.sim_results.insert(tk.END, f"Error: {str(e)}\n")
                self.sim_results.config(state=tk.DISABLED)
                
                # Log failure
                self.audit_log.add_entry(selected_account, datetime.now(), "FAILED")
                self.status_var.set(f"Authentication failed: {str(e)}")
            
            # Update audit log display
            self.refresh_audit_log()
            
        except Exception as e:
            messagebox.showerror("Error", f"Authentication process error: {str(e)}")

    # Action methods
    def create_account(self):
        """Create a new account based on form data"""
        try:
            account_name = self.create_name_var.get()
            secret_key = self.create_key_var.get()
            account_type_str = self.account_type_var.get()
            
            if not account_name or not secret_key:
                messagebox.showerror("Error", "Account name and secret key are required")
                return
            
            # Create account type
            if account_type_str == "Beginner":
                account_type = Beginner()
            elif account_type_str == "Advanced":
                account_type = Advanced()
            else:
                account_type = Tester()
            
            # Create account
            account = Account(account_type=account_type)
            account.set_account_name(account_name)
            account.set_secret_key(secret_key)
            
            self.current_account = account
            self.update_account_info()
            
            # Add to audit log
            self.audit_log.add_entry(account_name, datetime.now(), "ACCOUNT_CREATED")
            self.refresh_audit_log()
            
            self.status_var.set(f"Created account: {account_name}")
            messagebox.showinfo("Success", f"Account '{account_name}' created successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def add_contact(self):
        """Add contact to current account"""
        try:
            if not self.current_account:
                messagebox.showerror("Error", "No active account")
                return
            
            name = self.contact_name_var.get()
            address = self.contact_address_var.get()
            
            if not name or not address:
                messagebox.showerror("Error", "Contact name and address are required")
                return
            
            self.current_account.add_contact(name, address)
            self.update_account_info()
            
            self.status_var.set(f"Added contact: {name}")
            messagebox.showinfo("Success", f"Contact '{name}' added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def authenticate_account(self):
        """Test account authentication"""
        try:
            account_name = self.auth_name_var.get()
            password = self.auth_password_var.get()
            
            if not account_name:
                messagebox.showerror("Error", "Account name is required")
                return
                
            # Set the password to use for authentication
            self.auth_manager.test_password = password
            
            # Override account selection in User class for testing
            original_select_account = self.user._select_account
            self.user._select_account = lambda: account_name
            
            # Override password method for testing
            original_prompt_method = AuthenticationManager.prompt_for_password
            AuthenticationManager.prompt_for_password = lambda self: password.encode()
            
            try:
                # Use User class for login
                login_result = self.user.login()
                
                if login_result['success']:
                    # Authentication successful
                    self.current_account = self.user.get_current_account()
                    
                    # Update auth status
                    self.update_auth_status(True, account_name)
                    self.update_account_info()
                    
                    self.status_var.set(f"Authenticated as: {account_name}")
                    messagebox.showinfo("Success", f"Authenticated as '{account_name}'")
                else:
                    # Authentication failed
                    self.update_auth_status(False, account_name, login_result['error'])
                    messagebox.showerror("Authentication Failed", login_result['error'])
            finally:
                # Restore original methods
                self.user._select_account = original_select_account
                AuthenticationManager.prompt_for_password = original_prompt_method
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def simulate_failed_auth(self):
        """Simulate failed authentication attempts"""
        account_name = self.auth_name_var.get() or "test_account"
        
        # Add failed authentication entries
        for i in range(3):
            self.audit_log.add_entry(account_name, datetime.now(), "FAILED")
        
        self.update_auth_status(False, account_name, "Simulated 3 failed authentication attempts")
        self.refresh_audit_log()
        self.status_var.set("Simulated 3 failed authentication attempts")
    
    def save_account(self):
        """Save current account to file"""
        try:
            if not self.current_account:
                messagebox.showerror("Error", "No active account")
                return
                
            # Prompt for a save location
            dir_path = filedialog.askdirectory(
                title="Select Directory to Save Account",
                initialdir=self.file_manager.current_directory
            )
            
            if not dir_path:  # User cancelled
                return
            
            # Set temporary directory for saving
            old_dir = self.file_manager.current_directory
            self.file_manager.current_directory = dir_path
            
            # Get encryption key
            password = self.test_key_var.get().encode()
            biometric = b"test_biometric_data"
            encryption_key = self.auth_manager._generate_key(password, biometric)
            
            # Encrypt and save
            self.file_manager._encrypt_file(dir_path, encryption_key, self.current_account)
            
            # Reset directory
            self.file_manager.current_directory = old_dir
            
            self.status_var.set(f"Account saved to: {dir_path}")
            messagebox.showinfo("Success", f"Account saved to: {dir_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_account(self):
        """Load account from file"""
        try:
            # Prompt for file
            file_path = filedialog.askopenfilename(
                title="Select Account File",
                initialdir=self.file_manager.current_directory,
                filetypes=[("Encrypted Files", "*.enc"), ("All Files", "*.*")]
            )
            
            if not file_path:  # User cancelled
                return
                
            # Extract directory and account name
            dir_path = os.path.dirname(file_path)
            account_name = os.path.basename(file_path).split(".")[0]
            
            # Set temporary directory for loading
            old_dir = self.file_manager.current_directory
            self.file_manager.current_directory = dir_path
            
            # Get decryption key
            password = self.test_key_var.get().encode()
            biometric = b"test_biometric_data"
            decryption_key = self.auth_manager._generate_key(password, biometric)
            
            # Decrypt and load
            try:
                data = self.file_manager._decrypt_file(dir_path, decryption_key, account_name)
                account = Account(save_data=data)
                self.current_account = account
                
                self.update_account_info()
                self.audit_log.add_entry(account_name, datetime.now(), "ACCOUNT_LOADED")
                self.refresh_audit_log()
                
                self.status_var.set(f"Account loaded: {account_name}")
                messagebox.showinfo("Success", f"Account loaded: {account_name}")
            except Exception as e:
                messagebox.showerror("Decryption Failed", str(e))
            
            # Reset directory
            self.file_manager.current_directory = old_dir
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def test_encrypt(self):
        """Test encryption functionality"""
        try:
            content = self.test_content.get("1.0", tk.END)
            password = self.test_key_var.get().encode()
            
            if not content.strip():
                messagebox.showerror("Error", "No content to encrypt")
                return
                
            # Create a test encryption
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes
            
            # Generate salt and nonce
            salt = os.urandom(16)
            nonce = os.urandom(12)
            
            # Derive key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = kdf.derive(password)
            
            # Encrypt
            aesgcm = AESGCM(key)
            ciphertext = aesgcm.encrypt(nonce, content.encode('utf-8'), None)
            
            # Format result
            result = {
                "salt": salt.hex(),
                "nonce": nonce.hex(),
                "ciphertext": ciphertext.hex()
            }
            
            # Display result
            self.test_result.config(state=tk.NORMAL)
            self.test_result.delete(1.0, tk.END)
            self.test_result.insert(tk.END, str(result))
            self.test_result.config(state=tk.DISABLED)
            
            self.status_var.set("Content encrypted")
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))
    
    def test_decrypt(self):
        """Test decryption functionality"""
        try:
            import json
            
            try:
                # Parse input as JSON
                content = self.test_content.get("1.0", tk.END).strip()
                data = json.loads(content)
                
                # Extract components
                salt = bytes.fromhex(data["salt"])
                nonce = bytes.fromhex(data["nonce"])
                ciphertext = bytes.fromhex(data["ciphertext"])
            except:
                messagebox.showerror("Error", "Invalid encrypted data format. Must be JSON with salt, nonce, and ciphertext")
                return
                
            password = self.test_key_var.get().encode()
            
            # Decrypt
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes
            
            # Derive key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = kdf.derive(password)
            
            # Decrypt
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            
            # Display result
            self.test_result.config(state=tk.NORMAL)
            self.test_result.delete(1.0, tk.END)
            self.test_result.insert(tk.END, plaintext.decode('utf-8'))
            self.test_result.config(state=tk.DISABLED)
            
            self.status_var.set("Content decrypted")
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))

    # UI update methods
    def update_account_info(self):
        """Update the account info display"""
        self.account_info_text.config(state=tk.NORMAL)
        self.account_info_text.delete(1.0, tk.END)
        
        if not self.current_account:
            self.account_info_text.insert(tk.END, "No active account")
            self.account_info_text.config(state=tk.DISABLED)
            return
        
        info = f"Account Name: {self.current_account.get_account_name()}\n"
        info += f"Account Type: {self.current_account.get_account_type().get_type_name()}\n"
        info += f"Transaction Limit: {self.current_account.get_account_type().get_transaction_limit()}\n"
        info += f"Uses Real Funds: {self.current_account.get_account_type().uses_real_funds()}\n"
        
        info += "\nContacts:\n"
        contacts = self.current_account.get_contacts()
        if contacts:
            for name, address in contacts.items():
                info += f"  {name}: {address}\n"
        else:
            info += "  No contacts\n"
        
        self.account_info_text.insert(tk.END, info)
        self.account_info_text.config(state=tk.DISABLED)
    
    def update_auth_status(self, success, account_name, error=None):
        """Update authentication status display"""
        self.auth_status_text.config(state=tk.NORMAL)
        self.auth_status_text.delete(1.0, tk.END)
        
        info = f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        info += f"Account: {account_name}\n"
        info += f"Status: {'SUCCESS' if success else 'FAILED'}\n"
        
        if error:
            info += f"Error: {error}\n"
        
        # Show recent authentication attempts
        info += "\nRecent Authentication Attempts:\n"
        entries = self.audit_log.get_entries()
        if entries:
            for time, entry in sorted(entries.items(), key=lambda x: x[0], reverse=True)[:5]:
                info += f"  {time.strftime('%Y-%m-%d %H:%M:%S')} - "
                info += f"{entry['account_name']}: {entry['status']}\n"
        else:
            info += "  No entries\n"
        
        self.auth_status_text.insert(tk.END, info)
        self.auth_status_text.config(state=tk.DISABLED)
    
    def refresh_audit_log(self):
        """Update the audit log display"""
        self.audit_text.config(state=tk.NORMAL)
        self.audit_text.delete(1.0, tk.END)
        
        entries = self.audit_log.get_entries()
        if entries:
            for time, entry in sorted(entries.items(), key=lambda x: x[0]):
                info = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - "
                info += f"{entry['account_name']}: {entry['status']}\n"
                self.audit_text.insert(tk.END, info)
        else:
            self.audit_text.insert(tk.END, "No audit log entries")
        
        self.audit_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthenticationTestGUI(root)
    root.mainloop()

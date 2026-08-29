#!/usr/bin/env python3
"""
GUI ServiceDesk Automation dengan Bahasa Indonesia
- Dropdown untuk user tersimpan
- Otomatis tutup Excel jika terbuka
- Interface dalam Bahasa Indonesia
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import subprocess
import threading
import time
from servicedesk_automation_timing_fix import ServiceDeskAutomation

class ToolTip:
    """Simple tooltip class for tkinter widgets"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        if self.tooltip:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", 
                        relief="solid", borderwidth=1, font=("Arial", 8))
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ServiceDeskGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Otomasi ServiceDesk ADIRA")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # File untuk menyimpan kredensial
        self.credentials_file = "saved_credentials.json"
        self.saved_credentials = self.load_credentials()
        
        # File untuk menyimpan pengaturan
        self.settings_file = "gui_settings.json"
        self.saved_settings = self.load_settings()
        
        # Automation instance
        self.automation = None
        self.is_running = False
        
        # Password visibility toggle
        self.password_visible = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup antarmuka pengguna"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🚀 Otomasi ServiceDesk ADIRA", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Credentials section
        cred_frame = ttk.LabelFrame(main_frame, text="📋 Kredensial Login", padding="10")
        cred_frame.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=(0, 10))
        cred_frame.columnconfigure(1, weight=1)
        
        # Saved users dropdown
        ttk.Label(cred_frame, text="Pengguna Tersimpan:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.saved_user_var = tk.StringVar()
        
        # Handle old credentials format
        dropdown_values = list(self.saved_credentials.keys())
        if 'username' in self.saved_credentials and 'password' in self.saved_credentials:
            # Old format detected, add "Kredensial Lama" option
            dropdown_values = ["Kredensial Lama"] + dropdown_values
        
        self.saved_user_combo = ttk.Combobox(cred_frame, textvariable=self.saved_user_var, 
                                           values=dropdown_values,
                                           state="readonly", width=30)
        self.saved_user_combo.grid(row=0, column=1, sticky='w', padx=(0, 10))
        self.saved_user_combo.bind('<<ComboboxSelected>>', self.on_user_selected)
        
        # Auto-load old credentials if available
        if 'username' in self.saved_credentials and 'password' in self.saved_credentials:
            self.saved_user_var.set("Kredensial Lama")
            # Auto-load the old credentials
            try:
                import base64
                self.username_var = tk.StringVar(value=self.saved_credentials['username'])
                decoded_password = base64.b64decode(self.saved_credentials['password']).decode('utf-8')
                self.password_var = tk.StringVar(value=decoded_password)
            except:
                self.username_var = tk.StringVar(value=self.saved_credentials['username'])
                self.password_var = tk.StringVar(value=self.saved_credentials['password'])
        else:
            self.username_var = tk.StringVar()
            self.password_var = tk.StringVar()
        
        # Load user button
        load_btn = ttk.Button(cred_frame, text="📥 Muat", command=self.load_selected_user)
        load_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Profile management buttons with improved styling
        profile_buttons_frame = ttk.Frame(cred_frame)
        profile_buttons_frame.grid(row=0, column=3, padx=(10, 0))
        
        # Create styled buttons with better appearance
        style = ttk.Style()
        
        # Configure edit button style
        style.configure("Edit.TButton", 
                       foreground="blue", 
                       font=("Arial", 9, "bold"))
        
        # Configure delete button style  
        style.configure("Delete.TButton", 
                       foreground="red", 
                       font=("Arial", 9, "bold"))
        
        # Add hover effects
        style.map("Edit.TButton",
                 background=[('active', '#e6f3ff'),
                            ('pressed', '#cce7ff')])
        
        style.map("Delete.TButton", 
                 background=[('active', '#ffe6e6'),
                            ('pressed', '#ffcccc')])
        
        self.edit_btn = ttk.Button(profile_buttons_frame, 
                                  text="✏️ Edit", 
                                  command=self.edit_selected_profile, 
                                  style="Edit.TButton",
                                  width=8)
        self.edit_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.delete_btn = ttk.Button(profile_buttons_frame, 
                                    text="🗑️ Hapus", 
                                    command=self.delete_selected_profile, 
                                    style="Delete.TButton",
                                    width=8)
        self.delete_btn.grid(row=0, column=1)
        
        # Username
        ttk.Label(cred_frame, text="Username:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.username_entry = ttk.Entry(cred_frame, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=1, column=1, sticky='w', pady=(10, 0), padx=(0, 10))
        
        # Password with visibility toggle
        password_frame = ttk.Frame(cred_frame)
        password_frame.grid(row=2, column=0, columnspan=3, sticky='nsew', pady=(5, 0))
        password_frame.columnconfigure(1, weight=1)
        
        ttk.Label(password_frame, text="Password:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        # Password entry frame for better control
        password_entry_frame = ttk.Frame(password_frame)
        password_entry_frame.grid(row=0, column=1, sticky='nsew', padx=(0, 10))
        password_entry_frame.columnconfigure(0, weight=1)
        
        self.password_entry = ttk.Entry(password_entry_frame, textvariable=self.password_var, width=30)
        self.password_entry.grid(row=0, column=0, sticky='nsew')
        
        # Password visibility toggle button
        self.toggle_password_btn = ttk.Button(password_entry_frame, 
                                            text="👁️", 
                                            command=self.toggle_password_visibility,
                                            width=3)
        self.toggle_password_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Profile name for saving
        ttk.Label(cred_frame, text="Nama Profile:").grid(row=3, column=0, sticky='w', padx=(0, 10), pady=(5, 0))
        self.profile_name_var = tk.StringVar()
        self.profile_name_entry = ttk.Entry(cred_frame, textvariable=self.profile_name_var, width=30)
        self.profile_name_entry.grid(row=3, column=1, sticky='w', pady=(5, 0), padx=(0, 10))
        
        # Save credentials button
        ttk.Button(cred_frame, text="💾 Simpan", command=self.save_current_credentials).grid(row=3, column=2, padx=(5, 0), pady=(5, 0))
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Pengaturan", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky='nsew', pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Excel file
        ttk.Label(settings_frame, text="File Excel:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.excel_file_var = tk.StringVar(value="tickets.xlsx")
        self.excel_entry = ttk.Entry(settings_frame, textvariable=self.excel_file_var, width=40)
        self.excel_entry.grid(row=0, column=1, sticky='nsew', padx=(0, 10))
        ttk.Button(settings_frame, text="📁 Pilih", command=self.browse_excel_file).grid(row=0, column=2)

        # Location field
        ttk.Label(settings_frame, text="Location:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.location_var = tk.StringVar(value=self.saved_settings.get('location', ''))
        self.location_entry = ttk.Entry(settings_frame, textvariable=self.location_var, width=40)
        self.location_entry.grid(row=1, column=1, sticky='nsew', padx=(0, 10), pady=(10, 0))

        # Browser selection — Auto uses Firefox (project driver cache) then existing Chrome
        ttk.Label(settings_frame, text="Browser:").grid(row=2, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.browser_labels = {
            "auto": "Otomatis (Firefox, lalu Chrome yang sudah ada)",
            "firefox": "Firefox (driver di folder proyek)",
            "chrome": "Chrome (browser yang sudah terpasang)",
        }
        self.browser_label_to_value = {label: value for value, label in self.browser_labels.items()}
        saved_browser = self.saved_settings.get("browser", "auto")
        if saved_browser not in self.browser_labels:
            saved_browser = "auto"
        self.browser_var = tk.StringVar(value=self.browser_labels[saved_browser])
        self.browser_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.browser_var,
            values=list(self.browser_labels.values()),
            state="readonly",
            width=40,
        )
        self.browser_combo.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=(10, 0))
        
        # Options
        options_frame = ttk.Frame(settings_frame)
        options_frame.grid(row=3, column=0, columnspan=3, sticky='nsew', pady=(10, 0))
        
        # First row of options
        self.headless_var = tk.BooleanVar(value=self.saved_settings.get('headless_mode', False))
        ttk.Checkbutton(options_frame, text="🔇 Mode Tersembunyi (Headless)", 
                       variable=self.headless_var).grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        self.screenshots_var = tk.BooleanVar(value=self.saved_settings.get('screenshots', False))
        ttk.Checkbutton(options_frame, text="📸 Aktifkan Screenshot", 
                       variable=self.screenshots_var).grid(row=0, column=1, sticky='w')
        
        # Fast mode removed - using fixed automation with improved performance
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="🚀 Mulai Otomasi", 
                                     command=self.start_automation)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="⏹️ Berhenti", 
                                    command=self.stop_automation, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(control_frame, text="📊 Buka Excel", 
                  command=self.open_excel).grid(row=0, column=2, padx=(0, 10))
        
        ttk.Button(control_frame, text="📝 Buka Hasil", 
                  command=self.open_results).grid(row=0, column=3)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="📈 Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky='nsew', pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        # Mode indicator
        self.mode_var = tk.StringVar(value="Mode: Standar")
        self.mode_label = ttk.Label(progress_frame, textvariable=self.mode_var, 
                                   font=("Arial", 9, "bold"), foreground="blue")
        self.mode_label.grid(row=0, column=0, sticky='w')
        
        # Progress status
        self.progress_var = tk.StringVar(value="Siap untuk memulai...")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=1, column=0, sticky='w')
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=2, column=0, sticky='nsew', pady=(5, 0))
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log Aktivitas", padding="10")
        log_frame.grid(row=8, column=0, columnspan=2, sticky='nsew', pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky='nsew')
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Configure grid weights for responsive design
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        # Add tooltips for better user experience (after all elements are created)
        ToolTip(self.edit_btn, "Edit profil yang dipilih")
        ToolTip(self.delete_btn, "Hapus profil yang dipilih")
        ToolTip(self.toggle_password_btn, "Tampilkan/sembunyikan password")
        ToolTip(self.start_button, "Mulai otomasi pembuatan tiket")
        ToolTip(self.stop_button, "Hentikan proses otomasi")
        
        # Bind fast mode toggle to update mode indicator and save settings
        # Fast mode traces removed
        
        # Bind other settings to save automatically
        self.location_var.trace('w', lambda *args: self.save_settings())
        self.headless_var.trace('w', lambda *args: self.save_settings())
        self.screenshots_var.trace('w', lambda *args: self.save_settings())
        self.browser_var.trace('w', lambda *args: self.save_settings())
        
        # Initialize mode indicator
        self.update_mode_indicator()
        
        # Load saved credentials
        self.load_credentials()
        
        # Status bar
        self.status_var = tk.StringVar(value="Siap")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, columnspan=3, sticky='nsew', pady=(5, 0))
        
    def load_credentials(self):
        """Muat kredensial tersimpan"""
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading credentials: {str(e)}")
        return {}
    
    def save_credentials(self):
        """Simpan kredensial ke file"""
        try:
            with open(self.credentials_file, 'w', encoding='utf-8') as f:
                json.dump(self.saved_credentials, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving credentials: {str(e)}")
    
    def load_settings(self):
        """Muat pengaturan tersimpan"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
        return {}
    
    def save_settings(self):
        """Simpan pengaturan ke file"""
        try:
            settings = {
                # fast_mode removed
                'location': self.location_var.get().strip(),
                'headless_mode': self.headless_var.get(),
                'screenshots': self.screenshots_var.get(),
                'browser': self.browser_label_to_value.get(self.browser_var.get(), 'auto'),
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {str(e)}")
    
    def on_user_selected(self, event=None):
        """Handler ketika user dipilih dari dropdown"""
        selected_user = self.saved_user_var.get()
        if selected_user:
            self.load_selected_user(auto_load=True)
    
    def load_selected_user(self, auto_load=False):
        """Muat kredensial user yang dipilih"""
        selected_user = self.saved_user_var.get()
        
        if selected_user == "Kredensial Lama":
            # Handle old format
            if 'username' in self.saved_credentials and 'password' in self.saved_credentials:
                self.username_var.set(self.saved_credentials['username'])
                try:
                    import base64
                    decoded_password = base64.b64decode(self.saved_credentials['password']).decode('utf-8')
                    self.password_var.set(decoded_password)
                except:
                    self.password_var.set(self.saved_credentials['password'])
                
                if not auto_load:
                    self.log("📥 Kredensial lama dimuat")
        elif selected_user and selected_user in self.saved_credentials:
            # Handle new format
            user_data = self.saved_credentials[selected_user]
            self.username_var.set(user_data.get('username', ''))
            
            try:
                import base64
                decoded_password = base64.b64decode(user_data.get('password', '')).decode('utf-8')
                self.password_var.set(decoded_password)
            except:
                self.password_var.set(user_data.get('password', ''))
            
            if not auto_load:
                self.log(f"📥 Profil '{selected_user}' dimuat")
        else:
            if not auto_load:
                messagebox.showwarning("Peringatan", "Pilih profil yang valid!")
    
    def save_current_credentials(self):
        """Simpan kredensial saat ini"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        profile_name = self.profile_name_var.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan password harus diisi!")
            return
        
        if not profile_name:
            messagebox.showwarning("Peringatan", "Nama profil harus diisi!")
            return
        
        # Encode password
        import base64
        encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        
        # Save to new format
        self.saved_credentials[profile_name] = {
            'username': username,
            'password': encoded_password
        }
        
        self.save_credentials()
        
        # Update dropdown using the refresh function
        self.refresh_profile_dropdown()
        self.saved_user_var.set(profile_name)
        
        # Clear profile name field
        self.profile_name_var.set("")
        
        self.log(f"💾 Profil '{profile_name}' berhasil disimpan")
        messagebox.showinfo("Sukses", f"Profil '{profile_name}' berhasil disimpan!")
    
    def edit_selected_profile(self):
        """Edit profil yang dipilih"""
        selected_user = self.saved_user_var.get()
        
        if not selected_user:
            messagebox.showwarning("Peringatan", "Pilih profil yang akan diedit!")
            return
        
        if selected_user == "Kredensial Lama":
            messagebox.showinfo("Info", "Kredensial lama tidak dapat diedit.\nSilakan simpan sebagai profil baru.")
            return
        
        if selected_user not in self.saved_credentials:
            messagebox.showwarning("Peringatan", "Profil tidak ditemukan!")
            return
        
        # Load the selected profile data into the form
        self.load_selected_user()
        
        # Set the profile name in the profile name field for editing
        self.profile_name_var.set(selected_user)
        
        # Focus on the profile name field
        self.profile_name_entry.focus()
        
        self.log(f"✏️ Mode edit untuk profil '{selected_user}' - ubah data dan klik Simpan")
        messagebox.showinfo("Mode Edit", f"Profil '{selected_user}' dimuat untuk diedit.\n\nUbah data yang diperlukan dan klik 'Simpan' untuk menyimpan perubahan.")
    
    def delete_selected_profile(self):
        """Hapus profil yang dipilih"""
        selected_user = self.saved_user_var.get()
        
        if not selected_user:
            messagebox.showwarning("Peringatan", "Pilih profil yang akan dihapus!")
            return
        
        if selected_user == "Kredensial Lama":
            # Handle deletion of old credentials
            result = messagebox.askyesno("Konfirmasi Hapus", 
                                       "Apakah Anda yakin ingin menghapus kredensial lama?\n\nTindakan ini tidak dapat dibatalkan!")
            if result:
                # Remove old format credentials
                if 'username' in self.saved_credentials:
                    del self.saved_credentials['username']
                if 'password' in self.saved_credentials:
                    del self.saved_credentials['password']
                
                self.save_credentials()
                self.refresh_profile_dropdown()
                
                # Clear form
                self.username_var.set("")
                self.password_var.set("")
                self.profile_name_var.set("")
                
                self.log("🗑️ Kredensial lama berhasil dihapus")
                messagebox.showinfo("Sukses", "Kredensial lama berhasil dihapus!")
            return
        
        if selected_user not in self.saved_credentials:
            messagebox.showwarning("Peringatan", "Profil tidak ditemukan!")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Konfirmasi Hapus", 
                                   f"Apakah Anda yakin ingin menghapus profil '{selected_user}'?\n\nTindakan ini tidak dapat dibatalkan!")
        
        if result:
            # Delete the profile
            del self.saved_credentials[selected_user]
            self.save_credentials()
            
            # Refresh dropdown
            self.refresh_profile_dropdown()
            
            # Clear form
            self.username_var.set("")
            self.password_var.set("")
            self.profile_name_var.set("")
            
            self.log(f"🗑️ Profil '{selected_user}' berhasil dihapus")
            messagebox.showinfo("Sukses", f"Profil '{selected_user}' berhasil dihapus!")
    
    def refresh_profile_dropdown(self):
        """Refresh dropdown profil"""
        dropdown_values = list(self.saved_credentials.keys())
        if 'username' in self.saved_credentials and 'password' in self.saved_credentials:
            dropdown_values = ["Kredensial Lama"] + dropdown_values
        
        self.saved_user_combo['values'] = dropdown_values
        
        # Clear selection if the current selection no longer exists
        current_selection = self.saved_user_var.get()
        if current_selection not in dropdown_values:
            self.saved_user_var.set("")
    
    def browse_excel_file(self):
        """Browse untuk memilih file Excel"""
        filename = filedialog.askopenfilename(
            title="Pilih File Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.excel_file_var.set(filename)
    
    def log(self, message):
        """Tambahkan pesan ke log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_progress(self, message):
        """Update progress label"""
        self.progress_var.set(message)
        self.root.update_idletasks()
    
    def update_mode_indicator(self):
        """Update mode indicator - using fixed automation"""
        self.mode_var.set("Mode: ✅ FIXED (Improved Automation)")
        self.mode_label.config(foreground="green")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def start_automation(self):
        """Mulai otomasi"""
        # Validasi input
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        excel_file = self.excel_file_var.get().strip()
        location = self.location_var.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan password harus diisi!")
            return
        
        if not excel_file or not os.path.exists(excel_file):
            messagebox.showwarning("Peringatan", "File Excel tidak ditemukan!")
            return
        
        # Disable start button, enable stop button
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.is_running = True
        
        # Start progress bar
        self.progress_bar.start()
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Start automation in separate thread
        self.automation_thread = threading.Thread(target=self.run_automation, 
                                                 args=(username, password, excel_file, location))
        self.automation_thread.daemon = True
        self.automation_thread.start()
    
    def stop_automation(self):
        """Hentikan otomasi"""
        self.is_running = False
        self.update_progress("Menghentikan otomasi...")
        self.log("⏹️ Otomasi dihentikan oleh pengguna")
        
        if self.automation and hasattr(self.automation, 'driver') and self.automation.driver:
            try:
                self.automation.driver.quit()
                self.log("🔒 Browser ditutup")
            except:
                pass
        
        self.automation_finished()
    
    def automation_finished(self):
        """Dipanggil ketika otomasi selesai"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress_bar.stop()
        self.is_running = False
        self.update_status("Siap")
    
    def run_automation(self, username, password, excel_file, location):
        """Jalankan otomasi di thread terpisah"""
        try:
            self.log("🚀 Memulai Otomasi ServiceDesk ADIRA")
            self.log("=" * 50)
            
            # Setup automation
            self.automation = ServiceDeskAutomation()
            
            self.automation.browser_type = self.browser_label_to_value.get(
                self.browser_var.get(), "auto"
            )
            self.automation.location = location
            self.automation.ticket_file = excel_file
            
            self.update_progress("Menyiapkan browser...")
            self.update_status("Menyiapkan browser")
            
            # Setup driver
            headless = self.headless_var.get()
            if not self.automation.setup_driver(headless=headless):
                for line in getattr(self.automation, "setup_log", []):
                    self.log(line)
                self.log("❌ Gagal menyiapkan browser")
                self.log("Letakkan geckodriver di folder 'drivers/' atau pasang Firefox/Chrome.")
                self.automation_finished()
                return

            for line in getattr(self.automation, "setup_log", []):
                self.log(line)
            self.log("✅ Browser berhasil disiapkan!")
            
            if not self.is_running:
                return
        
            # Login
            self.update_progress("Melakukan login...")
            self.update_status("Login")
            self.log("🔐 Melakukan login...")
            
            if not self.automation.login(username, password):
                self.log("❌ Login gagal")
                self.automation_finished()
                return
            
            self.log("✅ Login berhasil!")
            
            if not self.is_running:
                return
            
            # Select role (skip if any known role is already on the dashboard)
            self.update_progress("Memeriksa role...")
            self.update_status("Memeriksa role")
            self.log("🎭 Memeriksa role...")
            
            if not self.automation.select_role():
                self.log("❌ Gagal memilih role")
                self.automation_finished()
                return
            
            if getattr(self.automation, "role_already_selected", False):
                role_name = getattr(self.automation, "detected_role", None) or "sudah aktif"
                self.log(f"✅ Role '{role_name}' sudah aktif — pemilihan role dilewati")
            else:
                self.log("✅ Role berhasil dipilih!")
            
            if not self.is_running:
                return
                
            # Process tickets
            self.update_progress("Memproses tiket...")
            self.update_status("Memproses tiket")
            self.log("📋 Memproses tiket dari Excel...")
            
            success = self.automation.process_tickets()
            
            if success:
                self.log("🎉 Otomasi selesai dengan sukses!")
                self.update_progress("Otomasi selesai!")
                messagebox.showinfo("Sukses", "Otomasi ServiceDesk selesai!\nPeriksa file Excel dan hasil untuk detail.")
            else:
                self.log("⚠️ Otomasi selesai dengan beberapa masalah")
                self.update_progress("Otomasi selesai dengan masalah")
                messagebox.showwarning("Selesai", "Otomasi selesai tetapi ada beberapa masalah.\nPeriksa log untuk detail.")
            
        except Exception as e:
            self.log(f"❌ Error dalam otomasi: {str(e)}")
            messagebox.showerror("Error", f"Terjadi error dalam otomasi:\n{str(e)}")
        
        finally:
            # Close browser
            if self.automation and hasattr(self.automation, 'driver') and self.automation.driver:
                try:
                    self.automation.driver.quit()
                    self.log("🔒 Browser ditutup")
                except:
                    pass
            
            self.automation_finished()
    
    def open_excel(self):
        """Buka file Excel"""
        excel_file = self.excel_file_var.get()
        if os.path.exists(excel_file):
            try:
                os.startfile(excel_file)
                self.log(f"📊 Membuka Excel: {os.path.basename(excel_file)}")
            except Exception as e:
                self.log(f"❌ Gagal membuka Excel: {str(e)}")
        else:
            messagebox.showwarning("Peringatan", "File Excel tidak ditemukan!")
    
    def open_results(self):
        """Buka file hasil"""
        results_file = "ticket_results.txt"
        if os.path.exists(results_file):
            try:
                os.startfile(results_file)
                self.log(f"📝 Membuka hasil: {results_file}")
            except Exception as e:
                self.log(f"❌ Gagal membuka hasil: {str(e)}")
        else:
            messagebox.showwarning("Peringatan", "File hasil tidak ditemukan!")

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password_entry.config(show="")
            self.toggle_password_btn.config(text="🙈")
        else:
            self.password_entry.config(show="*")
            self.toggle_password_btn.config(text="👁️")

def main():
    """Fungsi utama"""
    root = tk.Tk()
    app = ServiceDeskGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
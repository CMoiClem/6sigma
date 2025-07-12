import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import scipy.stats as stats

class ProcessCapabilityCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Six Sigma Process Capability Calculator")
        self.root.geometry("1920x1080")
        self.root.minsize(1200, 800)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Data variables
        self.data = None
        self.USL = tk.DoubleVar(value=0.0)
        self.LSL = tk.DoubleVar(value=0.0)
        self.target = tk.DoubleVar(value=0.0)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Analysis tab
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="📊 Analysis")
        
        # Data tab
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="📈 Data View")
        
        self.create_analysis_tab()
        self.create_data_tab()
        
    def create_analysis_tab(self):
        # Main container with padding
        main_container = ttk.Frame(self.analysis_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel for inputs and results
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Right panel for chart
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # === INPUT SECTION ===
        input_frame = ttk.LabelFrame(left_panel, text="📁 Data Input", padding="15")
        input_frame.pack(fill='x', pady=(0, 10))
        
        # File selection with status
        file_frame = ttk.Frame(input_frame)
        file_frame.pack(fill='x', pady=(0, 10))
        
        self.import_btn = ttk.Button(file_frame, text="📂 Import CSV File", 
                                    command=self.import_csv, width=20)
        self.import_btn.pack(side='left', padx=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file selected", 
                                   foreground='gray')
        self.file_label.pack(side='left', fill='x', expand=True)
        
        # Data preview
        self.data_preview = ttk.Label(input_frame, text="", font=('Arial', 9))
        self.data_preview.pack(fill='x', pady=(5, 0))
        
        # === SPECIFICATION LIMITS ===
        spec_frame = ttk.LabelFrame(left_panel, text="⚙️ Specification Limits", padding="15")
        spec_frame.pack(fill='x', pady=(0, 10))
        
        # USL
        usl_frame = ttk.Frame(spec_frame)
        usl_frame.pack(fill='x', pady=(0, 8))
        ttk.Label(usl_frame, text="Upper Spec Limit (USL):", width=20).pack(side='left')
        usl_entry = ttk.Entry(usl_frame, textvariable=self.USL, width=12, font=('Arial', 10))
        usl_entry.pack(side='right')
        
        # LSL
        lsl_frame = ttk.Frame(spec_frame)
        lsl_frame.pack(fill='x', pady=(0, 8))
        ttk.Label(lsl_frame, text="Lower Spec Limit (LSL):", width=20).pack(side='left')
        lsl_entry = ttk.Entry(lsl_frame, textvariable=self.LSL, width=12, font=('Arial', 10))
        lsl_entry.pack(side='right')
        
        # Target
        target_frame = ttk.Frame(spec_frame)
        target_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(target_frame, text="Target Value:", width=20).pack(side='left')
        target_entry = ttk.Entry(target_frame, textvariable=self.target, width=12, font=('Arial', 10))
        target_entry.pack(side='right')
        
        # Calculate button
        self.calc_btn = ttk.Button(spec_frame, text="🔄 Calculate Process Capabilities", 
                                  command=self.calculate_capabilities, 
                                  style='Accent.TButton')
        self.calc_btn.pack(fill='x', pady=(10, 0))
        
        # === RESULTS SECTION ===
        results_frame = ttk.LabelFrame(left_panel, text="📋 Results", padding="15")
        results_frame.pack(fill='both', expand=True)
        
        # Results with better formatting
        results_container = ttk.Frame(results_frame)
        results_container.pack(fill='both', expand=True)
        
        self.results_text = tk.Text(results_container, height=20, width=45, 
                                   wrap=tk.WORD, font=('Consolas', 9),
                                   bg='#f8f9fa', relief='flat', padx=10, pady=10)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(results_container, orient=tk.VERTICAL, 
                                 command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # === CHART SECTION ===
        chart_frame = ttk.LabelFrame(right_panel, text="📊 Process Distribution Chart", padding="15")
        chart_frame.pack(fill='both', expand=True)
        
        # Chart controls
        chart_controls = ttk.Frame(chart_frame)
        chart_controls.pack(fill='x', pady=(0, 10))
        
        ttk.Label(chart_controls, text="Chart Options:").pack(side='left')
        
        self.show_normal_curve = tk.BooleanVar(value=True)
        ttk.Checkbutton(chart_controls, text="Normal Curve", 
                       variable=self.show_normal_curve, 
                       command=self.update_chart).pack(side='left', padx=(10, 0))
        
        self.show_spec_limits = tk.BooleanVar(value=True)
        ttk.Checkbutton(chart_controls, text="Spec Limits", 
                       variable=self.show_spec_limits, 
                       command=self.update_chart).pack(side='left', padx=(10, 0))
        
        # Export button
        ttk.Button(chart_controls, text="💾 Export Chart", 
                  command=self.export_chart).pack(side='right')
        
        # Matplotlib figure
        self.fig = Figure(figsize=(10, 7), dpi=100, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief='sunken', 
                                   font=('Arial', 9))
        self.status_bar.pack(side='bottom', fill='x')
        
    def create_data_tab(self):
        # Data view with table
        data_container = ttk.Frame(self.data_frame)
        data_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Data table
        columns = ('Index', 'Value', 'Within Spec')
        self.data_tree = ttk.Treeview(data_container, columns=columns, show='headings', height=20)
        
        # Configure columns
        self.data_tree.heading('Index', text='Index')
        self.data_tree.heading('Value', text='Value')
        self.data_tree.heading('Within Spec', text='Within Spec')
        
        self.data_tree.column('Index', width=80, anchor='center')
        self.data_tree.column('Value', width=120, anchor='center')
        self.data_tree.column('Within Spec', width=100, anchor='center')
        
        # Scrollbars for data table
        data_scroll_y = ttk.Scrollbar(data_container, orient='vertical', command=self.data_tree.yview)
        data_scroll_x = ttk.Scrollbar(data_container, orient='horizontal', command=self.data_tree.xview)
        self.data_tree.configure(yscrollcommand=data_scroll_y.set, xscrollcommand=data_scroll_x.set)
        
        self.data_tree.pack(side='left', fill='both', expand=True)
        data_scroll_y.pack(side='right', fill='y')
        data_scroll_x.pack(side='bottom', fill='x')
        
    def import_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.status_bar.config(text="Loading CSV file...")
                self.root.update()
                
                df = pd.read_csv(file_path)
                
                # Try to identify the data column
                mass_column = None
                for col in df.columns:
                    if any(keyword in col.lower() for keyword in ['mass', 'value', 'measurement', 'data']):
                        mass_column = col
                        break
                
                if mass_column is None:
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        mass_column = numeric_cols[-1]
                    else:
                        messagebox.showerror("Error", "No numeric columns found in CSV file")
                        return
                
                self.data = df[mass_column].dropna().values
                filename = file_path.split('/')[-1]
                
                self.file_label.config(text=f"✓ {filename}", foreground='green')
                self.data_preview.config(text=f"📊 {len(self.data)} data points from '{mass_column}' column")
                
                # Update data table
                self.update_data_table()
                
                # Enable calculate button
                self.calc_btn.config(state='normal')
                
                self.status_bar.config(text=f"Successfully loaded {len(self.data)} data points")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")
                self.status_bar.config(text="Error loading file")
    
    def update_data_table(self):
        # Clear existing data
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        if self.data is None:
            return
            
        USL = self.USL.get()
        LSL = self.LSL.get()
        
        # Add data to table
        for i, value in enumerate(self.data):
            within_spec = "✓" if LSL <= value <= USL else "✗"
            self.data_tree.insert('', 'end', values=(i+1, f"{value:.4f}", within_spec))
    
    def calculate_capabilities(self):
        if self.data is None:
            messagebox.showwarning("Warning", "Please import a CSV file first")
            return
        
        try:
            self.status_bar.config(text="Calculating process capabilities...")
            self.root.update()
            
            # Basic statistics
            mu = np.mean(self.data)
            sigma = np.std(self.data, ddof=1)
            n = len(self.data)
            
            USL = self.USL.get()
            LSL = self.LSL.get()
            target = self.target.get()
            
            # Validation
            if USL <= LSL:
                messagebox.showerror("Error", "USL must be greater than LSL")
                return
            
            # Process capability indices
            Cp = (USL - LSL) / (6 * sigma)
            Cpk = min((USL - mu) / (3 * sigma), (mu - LSL) / (3 * sigma))
            Cpu = (USL - mu) / (3 * sigma)
            Cpl = (mu - LSL) / (3 * sigma)
            
            # Cpm (Taguchi index)
            Cpm = (USL - LSL) / (6 * np.sqrt(sigma**2 + (mu - target)**2))
            
            # Process yield calculations
            yield_within_spec = np.sum((self.data >= LSL) & (self.data <= USL)) / n * 100
            
            # Sigma level
            sigma_level = 3 * Cpk + 1.5 if Cpk > 0 else 0
            
            # Display results with enhanced formatting
            self.results_text.delete(1.0, tk.END)
            
            # Insert formatted results
            self.insert_colored_text("SIX SIGMA PROCESS CAPABILITY ANALYSIS\n", 'header')
            self.insert_colored_text("="*50 + "\n\n", 'separator')
            
            self.insert_colored_text("📊 BASIC STATISTICS:\n", 'section')
            self.insert_colored_text(f"Sample Size (n): {n}\n", 'normal')
            self.insert_colored_text(f"Mean (μ): {mu:.4f}\n", 'normal')
            self.insert_colored_text(f"Standard Deviation (σ): {sigma:.4f}\n", 'normal')
            self.insert_colored_text(f"Range: {np.max(self.data) - np.min(self.data):.4f}\n\n", 'normal')
            
            self.insert_colored_text("⚙️ SPECIFICATION LIMITS:\n", 'section')
            self.insert_colored_text(f"Upper Spec Limit (USL): {USL:.4f}\n", 'normal')
            self.insert_colored_text(f"Lower Spec Limit (LSL): {LSL:.4f}\n", 'normal')
            self.insert_colored_text(f"Target Value: {target:.4f}\n", 'normal')
            self.insert_colored_text(f"Spec Width: {USL - LSL:.4f}\n\n", 'normal')
            
            self.insert_colored_text("🎯 PROCESS CAPABILITY INDICES:\n", 'section')
            self.insert_colored_text(f"Cp (Potential Capability): {Cp:.4f}\n", 'normal')
            self.insert_colored_text(f"Cpk (Actual Capability): {Cpk:.4f}\n", 'capability')
            self.insert_colored_text(f"Cpu (Upper Capability): {Cpu:.4f}\n", 'normal')
            self.insert_colored_text(f"Cpl (Lower Capability): {Cpl:.4f}\n", 'normal')
            self.insert_colored_text(f"Cpm (Taguchi Index): {Cpm:.4f}\n\n", 'normal')
            
            self.insert_colored_text("📋 PROCESS METRICS:\n", 'section')
            self.insert_colored_text(f"Yield within Spec: {yield_within_spec:.2f}%\n", 'yield')
            self.insert_colored_text(f"Sigma Level: {sigma_level:.2f}σ\n", 'normal')
            self.insert_colored_text(f"Process Centering: {abs(mu - target):.4f}\n\n", 'normal')
            
            self.insert_colored_text("🔍 INTERPRETATION:\n", 'section')
            self.insert_colored_text("Cp/Cpk ≥ 1.33: Capable process\n", 'normal')
            self.insert_colored_text("Cp/Cpk ≥ 1.00: Marginally capable\n", 'normal')
            self.insert_colored_text("Cp/Cpk < 1.00: Incapable process\n\n", 'normal')
            
            self.insert_colored_text("🎯 CURRENT STATUS: ", 'section')
            
            if Cpk >= 1.33:
                self.insert_colored_text("✅ CAPABLE PROCESS", 'success')
            elif Cpk >= 1.00:
                self.insert_colored_text("⚠️ MARGINALLY CAPABLE", 'warning')
            else:
                self.insert_colored_text("❌ INCAPABLE PROCESS", 'error')
            
            # Update chart and data table
            self.update_chart()
            self.update_data_table()
            
            self.status_bar.config(text=f"Analysis complete - Process Cpk: {Cpk:.3f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")
            self.status_bar.config(text="Calculation failed")
    
    def insert_colored_text(self, text, tag):
        self.results_text.insert(tk.END, text, tag)
        
        # Configure text tags for colors
        self.results_text.tag_configure('header', foreground='#2c3e50', font=('Arial', 10, 'bold'))
        self.results_text.tag_configure('section', foreground='#3498db', font=('Arial', 9, 'bold'))
        self.results_text.tag_configure('separator', foreground='#7f8c8d')
        self.results_text.tag_configure('normal', foreground='#2c3e50')
        self.results_text.tag_configure('capability', foreground='#e74c3c', font=('Arial', 9, 'bold'))
        self.results_text.tag_configure('yield', foreground='#27ae60', font=('Arial', 9, 'bold'))
        self.results_text.tag_configure('success', foreground='#27ae60', font=('Arial', 9, 'bold'))
        self.results_text.tag_configure('warning', foreground='#f39c12', font=('Arial', 9, 'bold'))
        self.results_text.tag_configure('error', foreground='#e74c3c', font=('Arial', 9, 'bold'))
    
    def update_chart(self):
        self.fig.clear()
        
        if self.data is None:
            return
        
        ax = self.fig.add_subplot(111)
        
        # Enhanced histogram
        ax.hist(self.data, bins=30, density=True, alpha=0.7, color='lightblue', 
                edgecolor='navy', linewidth=0.5, label='Process Data')
        
        # Normal distribution curve
        if self.show_normal_curve.get():
            mu = np.mean(self.data)
            sigma = np.std(self.data, ddof=1)
            x = np.linspace(np.min(self.data), np.max(self.data), 100)
            y = stats.norm.pdf(x, mu, sigma)
            ax.plot(x, y, 'navy', linewidth=2, label='Normal Distribution')
        
        # Specification limits
        if self.show_spec_limits.get():
            USL = self.USL.get()
            LSL = self.LSL.get()
            target = self.target.get()
            mu = np.mean(self.data)
            
            if USL > 0:
                ax.axvline(USL, color='red', linestyle='--', linewidth=2, label=f'USL = {USL:.2f}')
            if LSL > 0:
                ax.axvline(LSL, color='red', linestyle='--', linewidth=2, label=f'LSL = {LSL:.2f}')
            if target > 0:
                ax.axvline(target, color='green', linestyle=':', linewidth=2, label=f'Target = {target:.2f}')
            
            ax.axvline(mu, color='blue', linestyle='-', linewidth=2, alpha=0.7, label=f'Mean = {mu:.2f}')
            
            # Shade out-of-spec areas
            if USL > 0 and LSL > 0:
                x_fill = np.linspace(np.min(self.data), np.max(self.data), 1000)
                y_fill = stats.norm.pdf(x_fill, mu, np.std(self.data, ddof=1))
                
                mask_lower = x_fill < LSL
                mask_upper = x_fill > USL
                
                ax.fill_between(x_fill[mask_lower], y_fill[mask_lower], 
                               alpha=0.3, color='red', label='Out of Spec')
                ax.fill_between(x_fill[mask_upper], y_fill[mask_upper], 
                               alpha=0.3, color='red')
        
        # Styling
        ax.set_xlabel('Value', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        ax.set_title('Process Distribution with Specification Limits', fontsize=14, fontweight='bold')
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Improve layout
        self.fig.tight_layout()
        self.canvas.draw()
    
    def export_chart(self):
        if self.data is None:
            messagebox.showwarning("Warning", "No data to export")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Chart exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export chart: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessCapabilityCalculator(root)
    root.mainloop()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

class DartPlungerSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dart-Plunger Springer Simulator")
        self.root.geometry("1600x900")  # Large window
        
        # Try to maximize window (platform-specific)
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                pass  # If maximizing fails, just use the set geometry
        
        # Default parameters
        self.params = {
            'p_0': 101325,          # Initial pressure inside plunger tube (Pa)
            'p_2': 101325,          # Ambient pressure (Pa)
            'D_b': 0.0127,          # Diameter of barrel (m)
            'D_p': 0.035052,        # Diameter of plunger (m)
            'gamma': 1.4,           # Adiabatic index cp/cv for air
            'mass_d': 0.0012,       # Mass of dart (kg)
            'mass_p': 0.06,         # Mass of plunger (kg)
            'fric1': 0.4,           # Static friction force (N)
            'fric2': 0.2,           # Dynamic friction term (N)
            'xso': 0.0254,          # Spring compression before priming (m)
            'L_0': 0.1016,          # Initial plunger length (m)
            'k': 523 * (11/5),      # Spring constant (N/m)
            'end_time': 0.02,       # Simulation end time (s)
            'n_points': 1500        # Number of evaluation points
        }
        
        self.setup_gui()
        self.run_simulation()  # Initial simulation
        
    def setup_gui(self):
        # Create main frames with very generous spacing
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for controls - compact but readable
        control_frame = ttk.Frame(main_container, width=350)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)  # Maintain fixed width
        
        # Right panel for plots - takes up most space
        plot_frame = ttk.Frame(main_container)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Setup control panel
        self.setup_controls(control_frame)
        
        # Setup plot area with maximum space
        self.create_plots(plot_frame)
        
    def setup_controls(self, parent):
        # Title
        title_label = ttk.Label(parent, text="Dart-Plunger Simulator", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Create scrollable parameter frame
        canvas = tk.Canvas(parent, height=500, width=330)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Parameter definitions
        param_info = {
            'p_0': ('Initial Pressure (Pa)', 50000, 200000),
            'p_2': ('Ambient Pressure (Pa)', 50000, 200000),
            'D_b': ('Barrel Diameter (m)', 0.005, 0.02),
            'D_p': ('Plunger Diameter (m)', 0.02, 0.05),
            'gamma': ('Adiabatic Index', 1.0, 2.0),
            'mass_d': ('Dart Mass (kg)', 0.0005, 0.005),
            'mass_p': ('Plunger Mass (kg)', 0.01, 0.2),
            'fric1': ('Static Friction (N)', 0, 2),
            'fric2': ('Dynamic Friction (N)', 0, 1),
            'xso': ('Spring Precompression (m)', 0.01, 0.05),
            'L_0': ('Initial Plunger Length (m)', 0.05, 0.2),
            'k': ('Spring Constant (N/m)', 100, 2000),
            'end_time': ('End Time (s)', 0.005, 0.1),
            'n_points': ('Number of Points', 500, 3000)
        }
        
        self.param_vars = {}
        
        for key, (label, min_val, max_val) in param_info.items():
            param_frame = ttk.Frame(scrollable_frame)
            param_frame.pack(fill=tk.X, pady=3)
            
            # Label with fixed width
            ttk.Label(param_frame, text=label, width=22).pack(side=tk.LEFT)
            
            # Entry with larger font for readability
            var = tk.DoubleVar(value=self.params[key])
            self.param_vars[key] = var
            
            entry = ttk.Entry(param_frame, textvariable=var, width=12, font=('Arial', 10))
            entry.pack(side=tk.LEFT, padx=5)
            entry.bind('<Return>', lambda e: self.run_simulation_threaded())
        
        # Buttons with larger spacing
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20, fill=tk.X)
        
        run_button = ttk.Button(button_frame, text="🚀 Run Simulation", 
                               command=self.run_simulation_threaded)
        run_button.pack(fill=tk.X, pady=5)
        
        reset_button = ttk.Button(button_frame, text="🔄 Reset Defaults", 
                                 command=self.reset_parameters)
        reset_button.pack(fill=tk.X, pady=5)
        
        # Results display
        results_label = ttk.Label(parent, text="Results Summary:", font=('Arial', 12, 'bold'))
        results_label.pack(pady=(20, 5))
        
        self.results_text = scrolledtext.ScrolledText(parent, height=8, width=40, 
                                                     font=('Courier', 9))
        self.results_text.pack(fill=tk.X, pady=5)
        
        # Status
        self.status_label = ttk.Label(parent, text="Ready", foreground="green", 
                                     font=('Arial', 10))
        self.status_label.pack(pady=10)
        
    def create_plots(self, parent):
        # Create very large matplotlib figure for maximum readability
        self.fig = Figure(figsize=(16, 12), dpi=100)
        self.fig.suptitle('Dart-Plunger Springer Simulation Results', fontsize=20, fontweight='bold')
        
        # Create 3x2 subplot layout with generous spacing
        self.axes = []
        for i in range(6):
            ax = self.fig.add_subplot(3, 2, i+1)
            self.axes.append(ax)
        
        # Adjust subplot parameters for maximum readability
        self.fig.subplots_adjust(
            left=0.08,      # Left margin
            bottom=0.08,    # Bottom margin  
            right=0.95,     # Right margin
            top=0.92,       # Top margin
            wspace=0.25,    # Width spacing between subplots
            hspace=0.35     # Height spacing between subplots
        )
        
        # Embed in tkinter with scrollbars if needed
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = FigureCanvasTkAgg(self.fig, canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar (with error handling)
        toolbar_frame = tk.Frame(canvas_frame)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        try:
            from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
            nav_toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
            nav_toolbar.update()
        except Exception as e:
            print(f"Navigation toolbar not available: {e}")
        
    def system(self, t, x):
        """Define the system of first-order ODEs"""
        d1, d2, p1, p2 = x  # dart and plunger variables
        
        # Calculate areas
        area_b = np.pi * (self.params['D_b']**2) / 4
        area_p = np.pi * (self.params['D_p']**2) / 4
        v_0 = self.params['L_0'] * area_p
        xsf = self.params['xso'] + self.params['L_0']
        
        # Internal pressure calculation (with safety checks)
        volume_ratio = np.maximum(
            ((self.params['L_0'] - p1) * area_p + d1 * area_b) / v_0,
            1e-10  # Prevent division by zero
        )
        p_t = self.params['p_0'] / (volume_ratio ** self.params['gamma'])
        
        # Derivatives
        dd1dt = d2  # dart velocity
        dp1dt = p2  # plunger velocity
        
        # Accelerations
        dp2dt = ((self.params['p_2'] - p_t) * area_p + 
                self.params['k'] * (xsf - p1)) / self.params['mass_p']
        dd2dt = ((p_t - self.params['p_2']) * area_b) / self.params['mass_d']
        
        return [dd1dt, dd2dt, dp1dt, dp2dt]
        
    def run_simulation(self):
        try:
            # Update parameters
            for key, var in self.param_vars.items():
                self.params[key] = var.get()
            
            # Solve ODE
            x0 = [0, 0, 0, 0]
            t_span = (0, self.params['end_time'])
            t_eval = np.linspace(0, self.params['end_time'], int(self.params['n_points']))
            
            sol = solve_ivp(self.system, t_span, x0, t_eval=t_eval)
            
            if not sol.success:
                raise Exception("ODE solver failed")
            
            # Extract results
            d1_pos, d1_vel, p1_pos, p1_vel = sol.y
            
            # Calculate derived quantities
            area_b = np.pi * (self.params['D_b']**2) / 4
            area_p = np.pi * (self.params['D_p']**2) / 4
            v_0 = self.params['L_0'] * area_p
            xsf = self.params['xso'] + self.params['L_0']
            
            # Avoid division by zero or negative values
            volume_ratio = np.maximum(
                ((self.params['L_0'] - p1_pos) * area_p + d1_pos * area_b) / v_0,
                1e-10
            )
            p_t_array = self.params['p_0'] / (volume_ratio ** self.params['gamma'])
            v_t_array = (self.params['L_0'] - p1_pos) * area_p + area_b * d1_pos
            spring_force = self.params['k'] * (xsf - p1_pos)
            
            # Clear and plot with large, readable formatting
            for ax in self.axes:
                ax.clear()
            
            # Configure all axes for maximum readability
            plot_configs = [
                (d1_pos, 'Dart Position', 'Position (m)', 'blue'),
                (d1_vel, 'Dart Velocity', 'Velocity (m/s)', 'red'),
                (p1_pos, 'Plunger Position', 'Position (m)', 'green'),
                (p1_vel, 'Plunger Velocity', 'Velocity (m/s)', 'magenta'),
                (p_t_array, 'System Pressure', 'Pressure (Pa)', 'cyan'),
                (v_t_array, 'System Volume', 'Volume (m³)', 'orange')
            ]
            
            for i, (data, title, ylabel, color) in enumerate(plot_configs):
                ax = self.axes[i]
                ax.plot(sol.t, data, color=color, linewidth=3)
                ax.set_title(f'{title} vs Time', fontsize=14, fontweight='bold')
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel(ylabel, fontsize=12)
                ax.grid(True, alpha=0.3)
                ax.tick_params(labelsize=11)
                
                # Use scientific notation for small/large numbers
                ax.ticklabel_format(style='scientific', scilimits=(-3, 3))
            
            self.canvas.draw()
            
            # Update results summary
            self.update_results_summary(sol, d1_pos, d1_vel, p1_pos, p1_vel, p_t_array, v_t_array)
            
            self.status_label.config(text="✅ Simulation completed successfully", 
                                   foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")
            self.status_label.config(text="❌ Simulation failed", foreground="red")
    
    def update_results_summary(self, sol, d1_pos, d1_vel, p1_pos, p1_vel, p_t_array, v_t_array):
        """Update the results text widget"""
        results = f"""SIMULATION RESULTS
{'='*40}
Time: {self.params['end_time']:.4f} s
Points: {len(sol.t)}
Success: {sol.success}

DART RESULTS
{'-'*20}
Final Position: {d1_pos[-1]:.6f} m
Final Velocity: {d1_vel[-1]:.3f} m/s
Max Velocity: {np.max(d1_vel):.3f} m/s

PLUNGER RESULTS  
{'-'*20}
Final Position: {p1_pos[-1]:.6f} m
Final Velocity: {p1_vel[-1]:.3f} m/s
Max Velocity: {np.max(np.abs(p1_vel)):.3f} m/s

SYSTEM RESULTS
{'-'*20}
Final Pressure: {p_t_array[-1]:.0f} Pa
Min Pressure: {np.min(p_t_array):.0f} Pa
Final Volume: {v_t_array[-1]:.2e} m³
Max Volume: {np.max(v_t_array):.2e} m³
"""
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
    
    def run_simulation_threaded(self):
        """Run simulation in thread to prevent GUI freezing"""
        self.status_label.config(text="🔄 Running simulation...", foreground="orange")
        thread = threading.Thread(target=self.run_simulation)
        thread.daemon = True
        thread.start()
    
    def reset_parameters(self):
        """Reset to default values"""
        defaults = {
            'p_0': 101325, 'p_2': 101325, 'D_b': 0.0127, 'D_p': 0.035052,
            'gamma': 1.4, 'mass_d': 0.0012, 'mass_p': 0.06, 'fric1': 0.4,
            'fric2': 0.2, 'xso': 0.0254, 'L_0': 0.1016, 'k': 523 * (11/5),
            'end_time': 0.02, 'n_points': 1500
        }
        
        for key, value in defaults.items():
            self.param_vars[key].set(value)
        
        self.run_simulation_threaded()

def main():
    root = tk.Tk()
    app = DartPlungerSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
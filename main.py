import tkinter as tk
from tkinter import messagebox
import random

class DeadlockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Deadlock Detection & Safety Simulator")
        self.root.geometry("850x650")
        self.root.configure(bg="#F4F6F9")

        # Core OS Data Structs (5 Processes, 3 Resource Types)
        self.num_processes = 5
        self.num_resources = 3

        # Allocation Matrix
        self.allocation = [
            [0, 1, 0],  # P0
            [2, 0, 0],  # P1
            [3, 0, 2],  # P2
            [2, 1, 1],  # P3
            [0, 0, 2]   # P4
        ]
        
        # Max Demand Matrix
        self.max_demand = [
            [7, 5, 3],  # P0
            [3, 2, 2],  # P1
            [9, 0, 2],  # P2
            [2, 2, 2],  # P3
            [4, 3, 3]   # P4
        ]
        
        # Available Vectors [R1, R2, R3]
        self.available = [3, 3, 2]

        # UI Grid Trackers
        self.alloc_entries = []
        self.max_entries = []
        self.avail_entries = []

        self.setup_ui()

    def setup_ui(self):
        # Header Canvas Label
        header = tk.Label(self.root, text="Banker's Algorithm & Deadlock Analyzer", 
                          font=("Helvetica", 18, "bold"), bg="#1E293B", fg="white", padx=12, pady=12)
        header.pack(fill=tk.X)

        # Main Workspace Frame
        main_frame = tk.Frame(self.root, bg="#F4F6F9", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Column: Matrices Input Layout
        matrix_frame = tk.LabelFrame(main_frame, text=" Matrix State Configurations ", 
                                      font=("Helvetica", 11, "bold"), bg="white", padx=15, pady=15)
        matrix_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Helper column headers
        for j in range(self.num_resources):
            tk.Label(matrix_frame, text=f"R{j}", font=("Helvetica", 10, "bold"), bg="white").grid(row=0, column=j+1, padx=5)
            tk.Label(matrix_frame, text=f"R{j}", font=("Helvetica", 10, "bold"), bg="white").grid(row=0, column=j+5, padx=5)

        tk.Label(matrix_frame, text="Allocation Matrix", font=("Helvetica", 10, "italic", "bold"), bg="white").grid(row=0, column=1, columnspan=3, pady=(0, 10))
        tk.Label(matrix_frame, text="Max Demand Matrix", font=("Helvetica", 10, "italic", "bold"), bg="white").grid(row=0, column=5, columnspan=3, pady=(0, 10))

        # Build Entry Grid Rows for Processes
        for i in range(self.num_processes):
            tk.Label(matrix_frame, text=f"P{i}: ", font=("Helvetica", 10, "bold"), bg="white").grid(row=i+1, column=0, padx=5, pady=2)
            
            alloc_row = []
            for j in range(self.num_resources):
                e = tk.Entry(matrix_frame, width=4, justify="center", font=("Helvetica", 10))
                e.insert(0, str(self.allocation[i][j]))
                e.grid(row=i+1, column=j+1, padx=3, pady=3)
                alloc_row.append(e)
            self.alloc_entries.append(alloc_row)

            tk.Label(matrix_frame, text="  |  ", bg="white", fg="#CBD5E1").grid(row=i+1, column=4)

            max_row = []
            for j in range(self.num_resources):
                e = tk.Entry(matrix_frame, width=4, justify="center", font=("Helvetica", 10))
                e.insert(0, str(self.max_demand[i][j]))
                e.grid(row=i+1, column=j+5, padx=3, pady=3)
                max_row.append(e)
            self.max_entries.append(max_row)

        # Vector Configs (Available Vectors System Wide)
        vector_frame = tk.LabelFrame(main_frame, text=" Available System Resources ", 
                                     font=("Helvetica", 11, "bold"), bg="white", padx=15, pady=15)
        vector_frame.grid(row=1, column=0, sticky="ew", pady=(15, 0), padx=(0, 10))

        for j in range(self.num_resources):
            tk.Label(vector_frame, text=f"Resource R{j}: ", bg="white", font=("Helvetica", 10)).grid(row=0, column=j*2, padx=5)
            e = tk.Entry(vector_frame, width=5, justify="center", font=("Helvetica", 10, "bold"))
            e.insert(0, str(self.available[j]))
            e.grid(row=0, column=j*2+1, padx=5)
            self.avail_entries.append(e)

        # Right Column: Operations Panel & Terminal Log Out
        control_frame = tk.Frame(main_frame, bg="#F4F6F9")
        control_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Action Core Buttons
        btn_run = tk.Button(control_frame, text="Check Deadlock State", command=self.run_bankers,
                            bg="#10B981", fg="white", font=("Helvetica", 11, "bold"), cursor="hand2", bd=0, padx=8, pady=8)
        btn_run.pack(fill=tk.X, pady=(0, 10))

        btn_random = tk.Button(control_frame, text="Inject Random Vectors", command=self.inject_random,
                               bg="#3B82F6", fg="white", font=("Helvetica", 11, "bold"), cursor="hand2", bd=0, padx=8, pady=8)
        btn_random.pack(fill=tk.X, pady=5)

        btn_deadlock = tk.Button(control_frame, text="Force Attack Deadlock", command=self.force_deadlock,
                                 bg="#EF4444", fg="white", font=("Helvetica", 11, "bold"), cursor="hand2", bd=0, padx=8, pady=8)
        btn_deadlock.pack(fill=tk.X, pady=5)

        # Console Visualizer output
        tk.Label(control_frame, text="Simulation Trace Terminal Log Log:", font=("Helvetica", 10, "bold"), bg="#F4F6F9").pack(anchor="w", pady=(15, 2))
        self.log_box = tk.Text(control_frame, width=40, height=22, bg="#0F172A", fg="#38BDF8", font=("Courier", 10), wrap=tk.WORD)
        self.log_box.pack(fill=tk.BOTH, expand=True)
        
        self.log("System Initialized.\nReady to run safety matrix check analysis.")

    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def read_inputs(self):
        try:
            for i in range(self.num_processes):
                for j in range(self.num_resources):
                    self.allocation[i][j] = int(self.alloc_entries[i][j].get())
                    self.max_demand[i][j] = int(self.max_entries[i][j].get())
            for j in range(self.num_resources):
                self.available[j] = int(self.avail_entries[j].get())
            return True
        except ValueError:
            messagebox.showerror("Parsing Error", "All matrix entries values must be clean integers.")
            return False

    def run_bankers(self):
        if not self.read_inputs():
            return
        
        self.log("\n--- Executing Banker's Safety Matrix Check ---")
        
        # Calculate Need Matrix: Need = Max - Allocation
        need = [[self.max_demand[i][j] - self.allocation[i][j] for j in range(self.num_resources)] for i in range(self.num_processes)]
        
        work = list(self.available)
        finish = [False] * self.num_processes
        safe_sequence = []

        # Reset grid highlights before check
        for row in self.alloc_entries:
            for e in row: e.configure(bg="white")

        # Safety checking processing sequence loop logic
        while len(safe_sequence) < self.num_processes:
            allocated_in_this_round = False
            for p in range(self.num_processes):
                if not finish[p]:
                    # Verify if system resource needs are lesser than working threshold availability
                    if all(need[p][r] <= work[r] for r in range(self.num_resources)):
                        self.log(f"Process P{p} requirements satisfied by resource pool. Allocating...")
                        # Assume process runs to finish and yields its allocated resources back to pool
                        for r in range(self.num_resources):
                            work[r] += self.allocation[p][r]
                        finish[p] = True
                        safe_sequence.append(p)
                        allocated_in_this_round = True
                        self.log(f"-> P{p} finished. Dynamic System Work Pool Vector now: {work}")
                        break
            
            if not allocated_in_this_round:
                break

        # Check results
        if len(safe_sequence) == self.num_processes:
            seq_str = " -> ".join([f"P{x}" for x in safe_sequence])
            self.log(f"\n🟢 SUCCESS: System state is perfectly SAFE.\nExecution order sequence: {seq_str}")
            messagebox.showinfo("Safe System State Verified", f"No Deadlock detected!\nSafe Sequence: {seq_str}")
        else:
            deadlocked_procs = [f"P{i}" for i in range(self.num_processes) if not finish[i]]
            self.log(f"\n🔴 CRITICAL ALERT: OS Deadlock State Detected!\nDeadlocked structural units: {', '.join(deadlocked_procs)}")
            
            # Highlight problem rows in red interface visual window
            for p_idx in range(self.num_processes):
                if not finish[p_idx]:
                    for e in self.alloc_entries[p_idx]:
                        e.configure(bg="#FEE2E2")
            
            messagebox.showerror("OS System Deadlock Fault", f"Deadlock Detected!\nProcesses locked: {', '.join(deadlocked_procs)}")

    def inject_random(self):
        # Generate random allocations safely within scope bounds
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                alloc_val = random.randint(0, 4)
                max_val = alloc_val + random.randint(0, 5)
                
                self.alloc_entries[i][j].delete(0, tk.END)
                self.alloc_entries[i][j].insert(0, str(alloc_val))
                
                self.max_entries[i][j].delete(0, tk.END)
                self.max_entries[i][j].insert(0, str(max_val))
        
        for j in range(self.num_resources):
            self.avail_entries[j].delete(0, tk.END)
            self.avail_entries[j].insert(0, str(random.randint(2, 6)))
        self.log("\n[Update] Generated a completely new clean process resource state.")
    def force_deadlock(self):
        # Set allocation demands artificially high and drop working availability down to zero
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                self.alloc_entries[i][j].delete(0, tk.END)
                self.alloc_entries[i][j].insert(0, "4")
                self.max_entries[i][j].delete(0, tk.END)
                self.max_entries[i][j].insert(0, "9")

        for entry in self.avail_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "0")

        self.log("\n[Attack Triggered] Forced high allocation profile dependencies with 0 system resource availability.")
        self.run_bankers()

if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockSimulator(root)
    root.mainloop()

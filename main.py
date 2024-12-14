import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import matplotlib.pyplot as plt
from is_safe_state import is_safe_state
from bankers_algorithm import process_request

class BankersAlgorithmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banker's Algorithm GUI")
        self.root.option_add("*Font", "Helvetica 14")

        # Input fields
        self.num_processes_label = tk.Label(root, text="Number of Processes:")
        self.num_processes_label.grid(row=0, column=0, pady=5, padx=10, sticky="e")
        self.num_processes_entry = tk.Entry(root, width=30)
        self.num_processes_entry.grid(row=0, column=1, pady=5, padx=10)

        self.num_resources_label = tk.Label(root, text="Number of Resources:")
        self.num_resources_label.grid(row=1, column=0, pady=5, padx=10, sticky="e")
        self.num_resources_entry = tk.Entry(root, width=30)
        self.num_resources_entry.grid(row=1, column=1, pady=5, padx=10)

        self.allocation_label = tk.Label(root, text="Allocation Matrix (comma-separated rows):")
        self.allocation_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.allocation_entry = tk.Entry(root, width=30)
        self.allocation_entry.grid(row=2, column=1, pady=5, padx=10)

        self.max_need_label = tk.Label(root, text="Max Need Matrix (comma-separated rows):")
        self.max_need_label.grid(row=3, column=0, pady=5, padx=10, sticky="e")
        self.max_need_entry = tk.Entry(root, width=30)
        self.max_need_entry.grid(row=3, column=1, pady=5, padx=10)

        self.available_label = tk.Label(root, text="Available Resources (space-separated):")
        self.available_label.grid(row=4, column=0, pady=5, padx=10, sticky="e")
        self.available_entry = tk.Entry(root, width=30)
        self.available_entry.grid(row=4, column=1, pady=5, padx=10)

        # Buttons
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_data, width=20)
        self.submit_button.grid(row=5, column=0, pady=20, padx=10, sticky="e")

        self.request_button = tk.Button(root, text="Make Resource Request", command=self.make_request, width=20)
        self.request_button.grid(row=5, column=1, pady=20, padx=10, sticky="w")

        self.plot_button = tk.Button(root, text="Show Resource Allocation Graph", command=self.plot_allocation, width=30)
        self.plot_button.grid(row=6, column=0, pady=20, padx=10, columnspan=2)

        # Internal data
        self.num_processes = 0
        self.num_resources = 0
        self.allocation = []
        self.max_need = []
        self.available = []

    def submit_data(self):
        try:
            self.num_processes = int(self.num_processes_entry.get())
            self.num_resources = int(self.num_resources_entry.get())
            self.allocation = [list(map(int, row.split())) for row in self.allocation_entry.get().split(",")]
            self.max_need = [list(map(int, row.split())) for row in self.max_need_entry.get().split(",")]
            self.available = list(map(int, self.available_entry.get().split()))

            safe, sequence = is_safe_state(self.available, self.allocation, self.max_need, self.num_processes, self.num_resources)
            if safe:
                messagebox.showinfo("System Status", f"The system is in a safe state. Safe sequence: {sequence}")
            else:
                messagebox.showwarning("System Status", "The system is NOT in a safe state!")
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def make_request(self):
        try:
            process = simpledialog.askinteger("Resource Request", "Enter the process number:")
            if process is None or process < 0 or process >= self.num_processes:
                raise ValueError("Invalid process number.")

            request_str = simpledialog.askstring("Resource Request", "Enter the request vector (space-separated):")
            if not request_str:
                raise ValueError("Request vector cannot be empty.")

            request = list(map(int, request_str.split()))
            if len(request) != self.num_resources:
                raise ValueError("Request vector must match the number of resources.")

            granted, result = process_request(process, request, self.available, self.allocation, self.max_need, self.num_resources)
            if granted:
                messagebox.showinfo("Request Status", f"Request granted. Safe sequence: {result}")
            else:
                messagebox.showwarning("Request Status", f"Request denied. {result}")
        except Exception as e:
            messagebox.showerror("Request Error", f"Invalid request: {e}")

    def plot_allocation(self):
        try:
            fig, ax = plt.subplots()
            processes = [f"P{i}" for i in range(self.num_processes)]
            for r in range(self.num_resources):
                resource_allocation = [self.allocation[p][r] for p in range(self.num_processes)]
                ax.bar(processes, resource_allocation, label=f"R{r}", bottom=[sum(self.allocation[p][:r]) for p in range(self.num_processes)])

            ax.set_ylabel("Allocated Resources")
            ax.set_title("Resource Allocation by Process")
            ax.legend()
            plt.show()
        except Exception as e:
            messagebox.showerror("Plot Error", f"Error generating plot: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankersAlgorithmApp(root)
    root.mainloop()

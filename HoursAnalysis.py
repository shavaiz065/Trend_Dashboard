import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
from tkcalendar import DateEntry


class DataFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Filter Application")
        self.root.attributes("-fullscreen", True)  # Full-screen mode

        # Left Panel for Controls
        control_frame = tk.Frame(root, width=300, bg="#ddd")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Select File Button
        self.file_label = tk.Label(control_frame, text="Select CSV File:", bg="#ddd")
        self.file_label.pack(pady=10)
        self.select_file_btn = tk.Button(control_frame, text="Select File", command=self.load_file)
        self.select_file_btn.pack(pady=5)

        # Select Date Button
        self.date_label = tk.Label(control_frame, text="Select Date:", bg="#ddd")
        self.date_label.pack(pady=10)
        self.date_entry = DateEntry(control_frame, width=20, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        # Employer Dropdown
        self.emp_label = tk.Label(control_frame, text="Filter Employer:", bg="#ddd")
        self.emp_label.pack(pady=10)
        self.employer_var = tk.StringVar()
        self.employer_dropdown = ttk.Combobox(control_frame, textvariable=self.employer_var)
        self.employer_dropdown.pack(pady=5)
        self.employer_dropdown.bind("<<ComboboxSelected>>", self.filter_data)

        # Exit Button
        self.exit_btn = tk.Button(control_frame, text="Exit", command=root.quit, bg="red", fg="white")
        self.exit_btn.pack(pady=20)

        # Data Display Area
        self.data_frame = tk.Frame(root)
        self.data_frame.pack(expand=True, fill=tk.BOTH)
        self.tree = ttk.Treeview(self.data_frame)
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.df = None  # Dataframe placeholder

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.display_data(self.df)
            self.update_employer_dropdown()

    def update_employer_dropdown(self):
        if self.df is not None:
            employers = self.df['Employer'].unique().tolist()
            self.employer_dropdown['values'] = employers

    def filter_data(self, event=None):
        if self.df is not None and self.employer_var.get():
            filtered_df = self.df[self.df['Employer'] == self.employer_var.get()]
            self.display_data(filtered_df)

    def display_data(self, data):
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.data_frame)
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.tree["columns"] = list(data.columns)
        self.tree["show"] = "headings"

        for col in data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for _, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))


if __name__ == "__main__":
    root = tk.Tk()
    app = DataFilterApp(root)
    root.mainloop()
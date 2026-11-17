import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import educsys_api

class EducationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Education Information System")
        self.spreadsheet = educsys_api.get_spreadsheet("EducSysDB")
        self.sheet = self.spreadsheet.sheet1

        self.create_widgets()
        self.display_records()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Name")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        self.email_label = tk.Label(self.root, text="Email")
        self.email_label.grid(row=1, column=0)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=1, column=1)

        self.age_label = tk.Label(self.root, text="Age")
        self.age_label.grid(row=2, column=0)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=2, column=1)

        self.grade_label = tk.Label(self.root, text="Grade")
        self.grade_label.grid(row=3, column=0)
        self.grade_entry = tk.Entry(self.root)
        self.grade_entry.grid(row=3, column=1)

        self.add_button = tk.Button(self.root, text="Add", command=self.add_record)
        self.add_button.grid(row=4, column=0)
        self.update_button = tk.Button(self.root, text="Update", command=self.update_record)
        self.update_button.grid(row=4, column=1)
        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_record)
        self.delete_button.grid(row=4, column=2)
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=4, column=3)

        self.records_tree = ttk.Treeview(self.root, columns=('Name', 'Email', 'Age', 'Grade'), show='headings')
        self.records_tree.heading('Name', text='Name')
        self.records_tree.heading('Email', text='Email')
        self.records_tree.heading('Age', text='Age')
        self.records_tree.heading('Grade', text='Grade')
        self.records_tree.grid(row=5, column=0, columnspan=4)
        self.records_tree.bind('<<TreeviewSelect>>', self.load_selected_record)

    def add_record(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        age = self.age_entry.get()
        grade = self.grade_entry.get()
        if name and email and age and grade:
            self.sheet.append_row([name, email, age, grade])
            self.display_records()
        else:
            messagebox.showerror("Error", "All fields are required")

    def update_record(self):
        selected_index = self.records_tree.selection()
        if selected_index:
            selected_record = self.records_tree.item(selected_index)['values']
            if selected_record:
                name, email, age, grade = selected_record
                new_name = self.name_entry.get()
                new_email = self.email_entry.get()
                new_age = self.age_entry.get()
                new_grade = self.grade_entry.get()
                new_record = [new_name, new_email, new_age, new_grade]
                for i in range(len(new_record)):
                    if new_record[i] == "":
                        new_record[i] = selected_record[i]
                # Find the row index of the selected record
                row_index = self.records_tree.index(selected_index)
                # Update the values in the corresponding row
                self.sheet.update([[new_name, new_email, new_age, new_grade]], f"A{row_index + 2}")
                self.display_records()
        else:
            messagebox.showerror("Error", "No record selected")

    def delete_record(self):
        selected_index = self.records_tree.selection()
        if selected_index:
            # Find the row index of the selected record
            row_index = self.records_tree.index(selected_index)
            # Delete the row from the sheet
            self.sheet.delete_rows(row_index + 2)  # Adding 2 to account for header and 0-based index
            self.display_records()
        else:
            messagebox.showerror("Error", "No record selected")

    def display_records(self):
        self.records_tree.delete(*self.records_tree.get_children())
        records = self.sheet.get_all_records()
        headers = records[0].keys() if records else []  # Get column headers
        for record in records:
            name = record.get('Name', '')  # Get the value of 'Name' or '' if not present
            email = record.get('Email', '')  # Get the value of 'Email' or '' if not present
            age = record.get('Age', '')    # Get the value of 'Age' or '' if not present
            grade = record.get('Grade', '')  # Get the value of 'Grade' or '' if not present
            self.records_tree.insert('', tk.END, values=(name, email, age, grade))


    def load_selected_record(self, event):
        selected_index = self.records_tree.selection()
        if selected_index:
            selected_record = self.records_tree.item(selected_index)['values']
            if selected_record:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(tk.END, selected_record[0])
                self.email_entry.delete(0, tk.END)
                self.email_entry.insert(tk.END, selected_record[1])
                self.age_entry.delete(0, tk.END)
                self.age_entry.insert(tk.END, selected_record[2])
                self.grade_entry.delete(0, tk.END)
                self.grade_entry.insert(tk.END, selected_record[3])

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = EducationSystem(root)
    root.mainloop()

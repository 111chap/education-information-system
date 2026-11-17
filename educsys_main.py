import tkinter as tk
from tkinter import messagebox
import educsys_api
import customtkinter as ctk
from tkinter import ttk

class EducationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Education Information System")
        self.root.geometry("980x370")
        self.root.configure(bg="#b2c7f7")
        self.create_widgets()
        self.spreadsheet = educsys_api.get_spreadsheet("EducSysDB")
        self.sheet = self.spreadsheet.sheet1
        self.display_records()

    def create_widgets(self):
        self.font1 = ("times", 10, "bold")
        self.font2 = ("times", 14, "bold")

        #self.design_frame = ctk.CTkFrame(self.root, width=1000, height=2, fg_color="#6DAFFE")
        #self.design_frame.place(x=0, y=0)

        self.header_frame = ctk.CTkFrame(self.root, width=450, height=90, fg_color="#437FC7",corner_radius=20)
        self.header_frame.place(x=-30, y=-30)

        tk.Label(self.header_frame, text= "Educational Information System", font=("times", 21, "bold"), bg="#437FC7", fg="#ffffff").place(x=40,y=38)

        self.entry_frame = ctk.CTkFrame(self.root, width=470, height=320, fg_color="#437FC7",corner_radius=20)
        self.entry_frame.place(x=-50, y=80)

        self.name_label = tk.Label(self.entry_frame, text="Name:", font=self.font1,bg="#437FC7", fg="#ffffff")
        self.name_label.place(x=90, y=20)
        self.name_entry = ctk.CTkEntry(self.entry_frame, font=self.font1,width= 285,height=27, fg_color="#437FC7", text_color="#FFFFFF",corner_radius=30)
        self.name_entry.place(x=150, y=20)

        self.email_label = tk.Label(self.entry_frame, text="Email:", font=self.font1,bg="#437FC7", fg="#ffffff")
        self.email_label.place(x=90, y=60)
        self.email_entry = ctk.CTkEntry(self.entry_frame, font=self.font1,width= 285,height=27, fg_color="#437FC7", text_color="#FFFFFF",corner_radius=30)
        self.email_entry.place(x=150, y=60)

        self.age_label = tk.Label(self.entry_frame, text="Age:", font=self.font1, bg="#437FC7", fg="#ffffff")
        self.age_label.place(x=90,y=100)
        self.age_entry = ctk.CTkEntry(self.entry_frame, font=self.font1,width= 285,height=27, fg_color="#437FC7", text_color="#FFFFFF",corner_radius=30)
        self.age_entry.place(x=150,y=100)

        self.grade_label = tk.Label(self.entry_frame, text="Grade:", font=self.font1,bg="#437FC7", fg="#ffffff")
        self.grade_label.place(x=90,y=140)
        self.grade_entry = ctk.CTkEntry(self.entry_frame, font=self.font1,width= 285,height=27, fg_color="#437FC7", text_color="#FFFFFF",corner_radius=30)
        self.grade_entry.place(x=150,y=140)

        self.button_frame = ctk.CTkFrame(self.entry_frame, width=380, height=90, fg_color="#649bf8",corner_radius=15)
        self.button_frame.place(x=70,y=180)

        self.add_button = ctk.CTkButton(self.button_frame, text="Add", command=self.add_record, font=self.font2,height=35, width=175,corner_radius=10, fg_color="#437FC7", hover_color="#00FF00")
        self.add_button.place(x=10,y=6)
        self.update_button = ctk.CTkButton(self.button_frame, text="Update", command=self.update_record, font=self.font2,height=35, width=175,corner_radius=10, fg_color="#437FC7", hover_color="#09036e")
        self.update_button.place(x=195,y=6 )
        self.delete_button = ctk.CTkButton(self.button_frame, text="Delete", command=self.delete_record, font=self.font2,height=35, width=175,corner_radius=10, fg_color="#437FC7", hover_color="#A52A2A")
        self.delete_button.place(x=10,y=50)
        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear", command=self.clear_fields, font=self.font2,height=35, width=175,corner_radius=10, fg_color="#437FC7", hover_color="#808080")
        self.clear_button.place(x=195,y=50)

        self.tree_frame = ctk.CTkFrame(self.root, fg_color="#437FC7", width=630, height=350,corner_radius=20)
        self.tree_frame.place(x=440, y=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Vertical.TScrollbar", background="#2a76f7", troughcolor="#437FC7", bordercolor="#649bf8", arrowcolor="#ffffff",relief="flat")
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", style="Custom.Vertical.TScrollbar")

        self.scrollbar.place(x=517, y=26,height=300)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("times", 11, "bold"), background="#2a76f7", foreground="#ffffff", relief="flat")
        style.configure("Treeview", font=("Helvitica", 9, "bold"), background="#649bf8", foreground="#ffffff", fieldbackground="#649bf8")
        style.map("Custom.Treeview", background=[("selected", "#008080")])

        self.tree = ttk.Treeview(self.tree_frame, height=14, columns=("Name","Email", "Age", "Grade"), style="Custom.Treeview", yscrollcommand=self.scrollbar.set)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Grade", text="Grade")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Name", anchor=tk.CENTER, width=160, stretch=tk.NO)
        self.tree.column("Email", anchor=tk.CENTER, width=160)
        self.tree.column("Age", anchor=tk.CENTER, width=85)
        self.tree.column("Grade", anchor=tk.CENTER, width=85)

        self.tree.place(x=25,y=25)
        self.scrollbar.config(command=self.tree.yview)
        self.tree.bind("<ButtonRelease-1>", self.load_selected_record)

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
        selected_index = self.tree.selection()
        if selected_index:
            selected_record = self.tree.item(selected_index)['values']
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
                row_index = self.tree.index(selected_index)
                # Update the values in the corresponding row
                self.sheet.update([[new_name, new_email, new_age, new_grade]], f"A{row_index + 2}")
                self.display_records()
        else:
            messagebox.showerror("Error", "No record selected")

    def delete_record(self):
        selected_index = self.tree.selection()
        if selected_index:
            # Find the row index of the selected record
            row_index = self.tree.index(selected_index)
            # Delete the row from the sheet
            self.sheet.delete_rows(row_index + 2)  # Adding 2 to account for header and 0-based index
            self.display_records()
        else:
            messagebox.showerror("Error", "No record selected")

    def display_records(self):
        self.tree.delete(*self.tree.get_children())
        records = self.sheet.get_all_records()
        headers = records[0].keys() if records else []  # Get column headers
        for record in records:
            name = record.get('Name', '')  # Get the value of 'Name' or '' if not present
            email = record.get('Email', '')  # Get the value of 'Email' or '' if not present
            age = record.get('Age', '')    # Get the value of 'Age' or '' if not present
            grade = record.get('Grade', '')  # Get the value of 'Grade' or '' if not present
            self.tree.insert('', tk.END, values=(name, email, age, grade))

    def load_selected_record(self, event):
        selected_index = self.tree.selection()
        if selected_index:
            selected_record = self.tree.item(selected_index)['values']
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

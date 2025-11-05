import tkinter as tk #tkinter gui module
from tkinter import ttk, messagebox
import os

DATA_FILE = "studentMarks.txt"      #data file path 
def load_students():     #loads student record from library

    if not os.path.exists(DATA_FILE):    #file not exists
        return []       #return empty list 
    students = []       #list to hold student records 
    with open(DATA_FILE, encoding="utf-8") as f:     
        lines = [line.strip() for line in f if line.strip()]      #read non-empty lines
    if lines and lines[0].isdigit():  #first line is count of records
        lines = lines[1:] #skip first line 
    for ln in lines: #process each line 
        parts = [p.strip() for p in ln.split(",")]  #split by comma
        if len(parts) == 6:  #valid record 
            try:  #convert and store data 
                students.append({   #dictionary for student record 
                    "code": int(parts[0]),    #student code 
                    "name": parts[1],     #student name 
                    "cw": [int(parts[2]), int(parts[3]), int(parts[4])],    #coursework marks 
                    "exam": int(parts[5]) #exam mark 
                })

            except ValueError:   #invalid data
                pass   #skip invalid record 
    return students    #return list of student record 
  
def save_students(students):   #saves record to file 
    with open(DATA_FILE, "w", encoding="utf-8") as f: #open file for writing 
        f.write(str(len(students)) + "\n") #write count of records

        for s in students: #write each record 
            f.write(f"{s['code']}, {s['name']}, {s['cw'][0]}, {s['cw'][1]}, {s['cw'][2]}, {s['exam']}\n")   #write student data 

def coursework_total(s): return sum(s["cw"])    #calculate coursework total 

def overall_percentage(s): return (coursework_total(s) + s["exam"]) / 160 * 100    #calculate overall percentage 

def grade(p):    #determine grade from percentage 
    return "A" if p >= 70 else "B" if p >= 60 else "C" if p >= 50 else "D" if p >= 40 else "F" #fail 

class StudentApp:   #main application class 
    
    def __init__(self, root):   #initialize app 
        self.root = root         #reference to the root window
        self.root.title("Student Marks Manager")    #window title 
        self.root.geometry("750x480")    #window size
        self.root.configure(bg="lightgrey")   #background color 
        self.students = load_students() 
           #load existing student records
        tk.Label(
            root, text="Student Marks Manager",   #title 
            font=("century", 20, "bold"),    #font style 
        ).pack(pady=10)     #title label
        
        form_frame = tk.Frame(root, bg="white", bd=2, relief="groove")     #form frame 
        form_frame.pack(padx=10, pady=5, fill="x")    #pack frame 
        self.code = self.make_entry(form_frame, "Code:", 0, 0)    #student code entry 
        self.name = self.make_entry(form_frame, "Name:", 0, 2)    #student name entry 
        self.c1 = self.make_entry(form_frame, "CW1:", 1, 0)       #coursework 1 entry 
        self.c2 = self.make_entry(form_frame, "CW2:", 1, 2)       #coursework 2 entry 
        self.c3 = self.make_entry(form_frame, "CW3:", 2, 0)       #coursework 3 entry 
        self.exam = self.make_entry(form_frame, "Exam:", 2, 2)  
          #exam entry 
        btn_frame = tk.Frame(root, bg="#d9d9d9")                #button frame 
        btn_frame.pack(fill="x", pady=10)                         #pack frame 

        tk.Button(btn_frame, text="Add", width=12, bg="lightgrey", command=self.add_student).pack(side="left", padx=10)   #add button 
        tk.Button(btn_frame, text="Update", width=12, bg="lightgrey", command=self.update_student).pack(side="left", padx=10)   #update button 
        tk.Button(btn_frame, text="Delete", width=12, bg="lightgrey", command=self.delete_student).pack(side="left", padx=10)   #delete button 
        tk.Button(btn_frame, text="Save All", width=12, bg="lightgrey", command=self.save_all).pack(side="left", padx=10)       #save all button 
        
        table_frame = tk.Frame(root, bg="grey", bd=2, relief="sunken")  #table frame
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)  #pack frame 
       
        cols = ("Code", "Name", "CW1", "CW2", "CW3", "Exam", "Total", "%", "Grade")   #table columns 
        self.table = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)  
        
        for c in cols:    #set up table heading 
            self.table.heading(c, text=c)   #column heading 
            self.table.column(c, width=80 if c != "Name" else 140)   #column width 
        self.table.pack(fill="both", expand=True, padx=5, pady=5)    #pack table 
        self.table.bind("<<TreeviewSelect>>", self.load_selected)    #bind selection event 
        self.refresh_table()    #initial table load 
    
    def make_entry(self, frame, text, row, col):   #create label and entry 
        tk.Label(frame, text=text, bg="white", font=("century", 10, "bold")).grid(row=row, column=col, padx=10, pady=5, sticky="w") #label 
        entry = tk.Entry(frame, width=15, font=("century", 10))   #entry 
        entry.grid(row=row, column=col + 1, padx=10, pady=5)      #grid entry 
        return entry    #return entry reference 
    
    def refresh_table(self):   #refresh table data 
        for row in self.table.get_children():    #clear existing rows 
            self.table.delete(row)    #delete row
        for s in self.students:     #add each student record 
            pct = overall_percentage(s) #calculate overall percentage 
            self.table.insert("", "end", values=(
                s["code"], s["name"], s["cw"][0], s["cw"][1], s["cw"][2],
                s["exam"], coursework_total(s), f"{pct:.1f}", grade(pct)
            ))
    def get_data(self):   #retrieve data from entries
        try:
            return {
                "code": int(self.code.get()),   #student code 
                "name": self.name.get().strip(),   #student name 
                "cw": [int(self.c1.get()), int(self.c2.get()), int(self.c3.get())],   #COURSEWORK MARKS 
                "exam": int(self.exam.get())   #exam mark
            }
        except ValueError:     #invalid input 
            messagebox.showerror("Invalid Input", "Please enter valid numbers for marks.")   #show error 
            return None    #return none 

    def add_student(self):    #add new student record 
        s = self.get_data()   #get data fro  entries 
        if not s:   #invalid data 
            return   #return 
        if any(st["code"] == s["code"] for st in self.students):   #check duplicate data 
            messagebox.showwarning("Duplicate Code", "That student code already exists.")   #show warning 
            return    #return 
        self.students.append(s)    #add students to list 
        self.refresh_table()    # refresh table 
        messagebox.showinfo("Success", f"{s['name']} added successfully!")    #show success message 

    def update_student(self):  #uddate
        s = self.get_data()    #get data from entries 
        if not s:   #invalid data 
            return
        for i, st in enumerate(self.students):   #find student to update 
            if st["code"] == s["code"]:         #match found 
                self.students[i] = s              #update record 
                self.refresh_table()              #refresh table 
                messagebox.showinfo("Updated", f"{s['name']}'s record updated.")        
                return  
        messagebox.showwarning("Not Found", "No student found with that code.")    #messsage display

    def delete_student(self):                   #function to delete a student 
        code = self.code.get().strip()          # Get the student code from the input field
        if not code.isdigit():                  # Validate input — must be a number
            messagebox.showerror("Error", "Enter valid code to delete.")
            return
        code = int(code)                        # Convert to integer for comparison
        for s in self.students:                 # Loop through the list of students to find the one to delete
            if s["code"] == code:               #match found 
                self.students.remove(s)         #remove the student record 
                self.refresh_table()            # Update the table display
                messagebox.showinfo("Deleted", f"{s['name']} removed successfully.")
                return
        messagebox.showwarning("Not Found", "Student not found.")         # If no matching student code is found, show a warning

    def save_all(self):              #Function to Save All Records to File
        save_students(self.students) # Call the helper function to write all student data to the file
        messagebox.showinfo("Saved", "All records saved successfully!")          # Notify the user that the data has been successfully saved

    def load_selected(self, event):      #Function to Load Selected Row into Input Fields
        sel = self.table.focus()         # Get the currently selected row in the Treeview table

        if not sel:
            return     # If nothing is selected, do nothing
        v = self.table.item(sel, "values")       # Retrieve the values (columns) of the selected row
        entries = [self.code, self.name, self.c1, self.c2, self.c3, self.exam]        # Define all the input entry boxes to update
        for i, e in enumerate(entries):         # Loop through each entry and fill it with the corresponding value
            e.delete(0, tk.END)     # Clear the old value
            e.insert(0, v[i])       #enter new value from table 

if __name__ == "__main__":           # Run App 
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from taskManager import TaskManager, Task, Priority, TaskStatus
class TaskManagerUI(ctk.CTk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        
        # Configure window
        self.title("Task Manager")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self._create_widgets()
        self._setup_layout()
        
    def _create_widgets(self):
        # Create main frames
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.main_frame = ctk.CTkFrame(self)
        
        # Sidebar buttons
        self.add_task_btn = ctk.CTkButton(
            self.sidebar,
            text="Add Task",
            command=self._show_add_task_dialog
        )
        self.view_tasks_btn = ctk.CTkButton(
            self.sidebar,
            text="View Tasks",
            command=self._refresh_task_list
        )
        self.statistics_btn = ctk.CTkButton(
            self.sidebar,
            text="Statistics",
            command=self._show_statistics
        )
        
        # Task list
        self.task_tree = ttk.Treeview(
            self.main_frame,
            columns=("ID", "Title", "Priority", "Deadline", "Status"),
            show="headings"
        )
        self._setup_treeview()
        
        # Search frame
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search tasks..."
        )
        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            command=self._search_tasks
        )
        
    def _setup_treeview(self):
        # Configure columns
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Deadline", text="Deadline")
        self.task_tree.heading("Status", text="Status")
        
        # Configure column widths
        self.task_tree.column("ID", width=50)
        self.task_tree.column("Title", width=200)
        self.task_tree.column("Priority", width=100)
        self.task_tree.column("Deadline", width=150)
        self.task_tree.column("Status", width=100)
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.task_tree.yview
        )
        self.task_tree.configure(yscrollcommand=self.scrollbar.set)
        
    def _setup_layout(self):
        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Place main frames
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Sidebar layout
        self.add_task_btn.pack(pady=10, padx=20)
        self.view_tasks_btn.pack(pady=10, padx=20)
        self.statistics_btn.pack(pady=10, padx=20)
        
        # Search frame layout
        self.search_frame.pack(fill="x", pady=10)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_btn.pack(side="left", padx=5)
        
        # Task list layout
        self.task_tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _show_add_task_dialog(self):
        dialog = AddTaskDialog(self, self.task_manager)
        self.wait_window(dialog)
        self._refresh_task_list()

    def _refresh_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        for task in self.task_manager.tasks:
            self.task_tree.insert(
                "",
                "end",
                values=(
                    task.id,
                    task.title,
                    task.priority.label,
                    task.deadline,
                    task.status.value
                )
            )

    def _search_tasks(self):
        keyword = self.search_entry.get().lower()
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        for task in self.task_manager.tasks:
            if (keyword in task.title.lower() or 
                keyword in task.description.lower()):
                self.task_tree.insert(
                    "",
                    "end",
                    values=(
                        task.id,
                        task.title,
                        task.priority.label,
                        task.deadline,
                        task.status.value
                    )
                )
    # Di dalam class TaskManagerUI, tambahkan method berikut:
    def _show_statistics(self):
        # Create statistics window
        stats_window = ctk.CTkToplevel(self)
        stats_window.title("Task Statistics")
        stats_window.geometry("400x500")
        stats_window.grab_set()  # Make the window modal
        
        # Calculate statistics
        total_tasks = len(self.task_manager.tasks)
        if total_tasks == 0:
            label = ctk.CTkLabel(
                stats_window,
                text="No tasks available!",
                font=("Arial", 14)
            )
            label.pack(pady=20)
            return
            
        completed_tasks = sum(1 for task in self.task_manager.tasks 
                            if task.status == TaskStatus.COMPLETED)
        pending_tasks = total_tasks - completed_tasks
        
        now = datetime.now()
        overdue_tasks = sum(1 for task in self.task_manager.tasks 
                           if task.status == TaskStatus.PENDING 
                           and datetime.strptime(task.deadline, "%Y-%m-%d %H:%M") < now)
        
        priority_counts = {priority: sum(1 for task in self.task_manager.tasks 
                                       if task.priority == priority)
                          for priority in Priority}
        
        # Create frames
        overview_frame = ctk.CTkFrame(stats_window)
        overview_frame.pack(fill="x", padx=20, pady=10)
        
        priority_frame = ctk.CTkFrame(stats_window)
        priority_frame.pack(fill="x", padx=20, pady=10)
        
        # Overview statistics
        ctk.CTkLabel(
            overview_frame,
            text="Overview",
            font=("Arial", 16, "bold")
        ).pack(pady=5)
        
        stats_text = f"""
Total Tasks: {total_tasks}
Completed Tasks: {completed_tasks}
Pending Tasks: {pending_tasks}
Overdue Tasks: {overdue_tasks}
        """
        
        ctk.CTkLabel(
            overview_frame,
            text=stats_text,
            justify="left",
            font=("Arial", 14)
        ).pack(pady=10)
        
        # Priority statistics
        ctk.CTkLabel(
            priority_frame,
            text="Tasks by Priority",
            font=("Arial", 16, "bold")
        ).pack(pady=5)
        
        for priority, count in priority_counts.items():
            priority_text = f"{priority.icon} {priority.label}: {count}"
            ctk.CTkLabel(
                priority_frame,
                text=priority_text,
                font=("Arial", 14)
            ).pack(pady=2)
            
        # Completion rate
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            completion_frame = ctk.CTkFrame(stats_window)
            completion_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                completion_frame,
                text="Completion Rate",
                font=("Arial", 16, "bold")
            ).pack(pady=5)
            
            progress_bar = ctk.CTkProgressBar(completion_frame)
            progress_bar.pack(pady=10)
            progress_bar.set(completion_rate / 100) 
            
            ctk.CTkLabel(
                completion_frame,
                text=f"{completion_rate:.1f}%",
                font=("Arial", 14)
            ).pack()
        
        # Close button
        ctk.CTkButton(
            stats_window,
            text="Close",
            command=stats_window.destroy
        ).pack(pady=20)
        
class AddTaskDialog(ctk.CTkToplevel):
    def __init__(self, parent, task_manager):
        super().__init__(parent)
        self.task_manager = task_manager
        
        self.title("Add New Task")
        self.geometry("500x600")
        
        self._create_widgets()
        self._setup_layout()
        
    def _create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="Task Title:")
        self.title_entry = ctk.CTkEntry(self)
        
        # Description
        self.desc_label = ctk.CTkLabel(self, text="Description:")
        self.desc_text = ctk.CTkTextbox(self, height=100)
        
        # Priority
        self.priority_label = ctk.CTkLabel(self, text="Priority:")
        self.priority_var = tk.StringVar(value="MEDIUM")
        self.priority_frame = ctk.CTkFrame(self)
        
        for priority in Priority:
            ctk.CTkRadioButton(
                self.priority_frame,
                text=f"{priority.label} {priority.icon}",
                variable=self.priority_var,
                value=priority.name
            ).pack(side="left", padx=10)
        
        # Deadline
        self.deadline_label = ctk.CTkLabel(self, text="Deadline:")
        self.deadline_frame = ctk.CTkFrame(self)
        self.date_picker = DateEntry(
            self.deadline_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.time_spinbox = ttk.Spinbox(
            self.deadline_frame,
            from_=0,
            to=23,
            width=5,
            format="%02.0f:00"
        )
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Save",
            command=self._save_task
        )
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy
        )
        
    def _setup_layout(self):
        padding = {'padx': 20, 'pady': 5}
        
        self.title_label.pack(**padding)
        self.title_entry.pack(**padding)
        
        self.desc_label.pack(**padding)
        self.desc_text.pack(**padding)
        
        self.priority_label.pack(**padding)
        self.priority_frame.pack(**padding)
        
        self.deadline_label.pack(**padding)
        self.deadline_frame.pack(**padding)
        self.date_picker.pack(side="left", padx=5)
        self.time_spinbox.pack(side="left", padx=5)
        
        self.button_frame.pack(pady=20)
        self.save_btn.pack(side="left", padx=10)
        self.cancel_btn.pack(side="left", padx=10)
        
    def _save_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required!")
            return
            
        description = self.desc_text.get("1.0", "end-1c").strip()
        priority = Priority[self.priority_var.get()]
        
        date = self.date_picker.get_date()
        time = int(self.time_spinbox.get().split(':')[0])
        deadline = datetime.combine(date, datetime.min.time()) + timedelta(hours=time)
        
        task = Task(
            id=self.task_manager.task_id_counter,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING,
            deadline=deadline.strftime("%Y-%m-%d %H:%M"),
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        
        self.task_manager.tasks.append(task)
        self.task_manager.task_id_counter += 1
        messagebox.showinfo("Success", f"Task '{title}' added successfully!")
        self.destroy()
        
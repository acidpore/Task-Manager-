import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from taskManager import TaskManager, Task, Priority, TaskStatus
from PIL import Image, ImageTk
import os

class ModernTaskManagerUI(ctk.CTk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        
        # Configure window
        self.title("Modern Task Manager")
        self.geometry("1300x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Load and store images
        self.images = self._load_images()
        
        self._create_widgets()
        self._setup_layout()
        self._apply_custom_style()
        
    def _load_images(self):
        # Directory containing images
        image_dir = "icons"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            
        # Dictionary to store images
        images = {}
        
        # Define image paths and sizes
        image_config = {
            "add": ("add.png", 20),
            "view": ("view.png", 20),
            "stats": ("stats.png", 20),
            "search": ("search.png", 20),
            "logo": ("logo.png", 40)
        }
        
        return images

    def _create_widgets(self):
        # Create main frames with modern styling
        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=15
        )
        
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )
        
        # Logo and title in sidebar
        self.logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        
        self.app_title = ctk.CTkLabel(
            self.logo_frame,
            text="Task Manager",
            font=("Roboto", 24, "bold"),
            text_color="#4A90E2"
        )
        
        # Sidebar buttons with improved styling
        button_configs = [
            ("Add Task", self._show_add_task_dialog, "#4CAF50"),
            ("View Tasks", self._refresh_task_list, "#2196F3"),
            ("Statistics", self._show_statistics, "#9C27B0")
        ]
        
        self.nav_buttons = []
        for text, command, color in button_configs:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                font=("Roboto", 14),
                height=40,
                corner_radius=8,
                fg_color=color,
                hover_color=self._adjust_color(color, -20)
            )
            self.nav_buttons.append(btn)
        
        # Modern search bar
        self.search_frame = ctk.CTkFrame(
            self.main_frame,
            height=50,
            corner_radius=10
        )
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search tasks...",
            font=("Roboto", 12),
            height=35,
            corner_radius=8
        )
        
        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100,
            height=35,
            corner_radius=8,
            command=self._search_tasks,
            font=("Roboto", 12),
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        
        # Enhanced Treeview
        self.task_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10
        )
        
        self.task_tree = ttk.Treeview(
            self.task_frame,
            columns=("ID", "Title", "Priority", "Deadline", "Status", "Progress"),
            show="headings",
            style="Modern.Treeview"
        )
        self._setup_treeview()
        
        # Action buttons frame
        self.action_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10,
            fg_color="transparent"
        )
        
        action_buttons = [
            ("Complete", self._complete_task, "#4CAF50"),
            ("Edit", self._edit_task, "#2196F3"),
            ("Delete", self._delete_task, "#F44336")
        ]
        
        self.action_buttons = []
        for text, command, color in action_buttons:
            btn = ctk.CTkButton(
                self.action_frame,
                text=text,
                command=command,
                width=100,
                height=35,
                corner_radius=8,
                font=("Roboto", 12),
                fg_color=color,
                hover_color=self._adjust_color(color, -20)
            )
            self.action_buttons.append(btn)

    def _setup_treeview(self):
        # Configure columns
        columns = {
            "ID": 50,
            "Title": 300,
            "Priority": 100,
            "Deadline": 150,
            "Status": 100,
            "Progress": 150
        }
        
        for col, width in columns.items():
            self.task_tree.heading(col, text=col, anchor="w")
            self.task_tree.column(col, width=width, anchor="w")
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.task_frame,
            orient="vertical",
            command=self.task_tree.yview
        )
        self.task_tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind selection event
        self.task_tree.bind("<<TreeviewSelect>>", self._on_select_task)
        
    def _setup_layout(self):
        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Place main frames
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        # Sidebar layout
        self.logo_frame.pack(fill="x", pady=20, padx=15)
        self.app_title.pack(side="left", padx=10)
        
        for btn in self.nav_buttons:
            btn.pack(pady=10, padx=15, fill="x")
        
        # Main frame layout
        self.search_frame.pack(fill="x", padx=15, pady=15)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(15, 10))
        self.search_btn.pack(side="right", padx=15)
        
        self.task_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.task_tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.action_frame.pack(fill="x", padx=15, pady=(0, 15))
        for btn in self.action_buttons:
            btn.pack(side="left", padx=5)

    def _apply_custom_style(self):
        # Create and configure ttk style
        style = ttk.Style()
        
        # Configure Treeview
        style.configure(
            "Modern.Treeview",
            background="#2B2B2B",
            foreground="white",
            fieldbackground="#2B2B2B",
            borderwidth=0,
            font=("Roboto", 11)
        )
        
        style.configure(
            "Modern.Treeview.Heading",
            background="#333333",
            foreground="white",
            borderwidth=1,
            font=("Roboto", 12, "bold")
        )
        
        # Remove borders
        style.layout("Modern.Treeview", [
            ('Modern.Treeview.treearea', {'sticky': 'nswe'})
        ])

    def _adjust_color(self, hex_color, adjustment):
        """Adjust color brightness"""
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Adjust brightness
        new_rgb = tuple(
            max(0, min(255, c + adjustment))
            for c in rgb
        )
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

    def _refresh_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        for task in self.task_manager.tasks:
            deadline = datetime.strptime(task.deadline, "%Y-%m-%d %H:%M")
            now = datetime.now()
            
            # Calculate progress
            if task.status == TaskStatus.COMPLETED:
                progress = "100%"
            else:
                total_time = (deadline - datetime.strptime(task.created_at, "%Y-%m-%d %H:%M")).total_seconds()
                elapsed_time = (now - datetime.strptime(task.created_at, "%Y-%m-%d %H:%M")).total_seconds()
                progress = f"{min(100, int((elapsed_time / total_time) * 100))}%"
            
            self.task_tree.insert(
                "",
                "end",
                values=(
                    task.id,
                    task.title,
                    f"{task.priority.icon} {task.priority.label}",
                    deadline.strftime("%Y-%m-%d %H:%M"),
                    task.status.value,
                    progress
                ),
                tags=('completed',) if task.status == TaskStatus.COMPLETED else ()
            )
        
        # Configure tag colors
        self.task_tree.tag_configure('completed', foreground='#888888')
        
    def _search_tasks(self):
        search_term = self.search_entry.get().lower()
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
    
        for task in self.task_manager.tasks:
            if search_term in task.title.lower() or search_term in task.description.lower():
                self.task_tree.insert(
                    "",
                    "end",
                    values=(
                        task.id,
                        task.title,
                        f"{task.priority.icon} {task.priority.label}",
                        datetime.strptime(task.deadline, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M"),
                        task.status.value,
                        "100%" if task.status == TaskStatus.COMPLETED else "0%"
                    )
                )

    def _show_add_task_dialog(self):
        dialog = ModernAddTaskDialog(self, self.task_manager)
        self.wait_window(dialog)
        self._refresh_task_list()

    def _complete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to complete")
            return
            
        task_id = int(self.task_tree.item(selected[0])['values'][0])
        task = next((t for t in self.task_manager.tasks if t.id == task_id), None)
        
        if task:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")
            messagebox.showinfo("Success", f"Task '{task.title}' marked as completed!")
            self._refresh_task_list()

    def _edit_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit")
            return
            
        task_id = int(self.task_tree.item(selected[0])['values'][0])
        task = next((t for t in self.task_manager.tasks if t.id == task_id), None)
        
        if task:
            dialog = ModernEditTaskDialog(self, self.task_manager, task)
            self.wait_window(dialog)
            self._refresh_task_list()

    def _delete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete")
            return
            
        task_id = int(self.task_tree.item(selected[0])['values'][0])
        task = next((t for t in self.task_manager.tasks if t.id == task_id), None)
        
        if task:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task '{task.title}'?"):
                self.task_manager.tasks.remove(task)
                messagebox.showinfo("Success", f"Task '{task.title}' deleted!")
                self._refresh_task_list()

    def _on_select_task(self, event):
        # Enable/disable action buttons based on selection
        selected = self.task_tree.selection()
        for btn in self.action_buttons:
            btn.configure(state="normal" if selected else "disabled")

    def _show_statistics(self):
        ModernStatisticsDialog(self, self.task_manager)

# Kelas untuk dialog penambahan tugas baru
class ModernAddTaskDialog(ctk.CTkToplevel):
    def __init__(self, parent, task_manager):
        super().__init__(parent)
        self.task_manager = task_manager
        
        self.title("Add New Task")
        self.geometry("600x700")
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._setup_layout()
        
    def _create_widgets(self):
        # Title
        self.title_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Create New Task",
            font=("Roboto", 24, "bold"),
            text_color="#4A90E2"
        )
        
        # Input fields
        self.input_frame = ctk.CTkFrame(self, corner_radius=15)
        
        # Task title
        self.title_entry_label = ctk.CTkLabel(
            self.input_frame,
            text="Task Title",
            font=("Roboto", 14, "bold")
        )
        self.title_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter task title...",
            height=40,
            font=("Roboto", 12)
        )
        
        # Description
        self.desc_label = ctk.CTkLabel(
            self.input_frame,
            text="Description",
            font=("Roboto", 14, "bold")
        )
        self.desc_text = ctk.CTkTextbox(
            self.input_frame,
            height=100,
            font=("Roboto", 12)
        )
        
        # Priority
        self.priority_label = ctk.CTkLabel(
            self.input_frame,
            text="Priority Level",
            font=("Roboto", 14, "bold")
        )
        self.priority_var = tk.StringVar(value="MEDIUM")
        self.priority_frame = ctk.CTkFrame(
            self.input_frame,
            fg_color="transparent"
        )
        
        priority_colors = {
            Priority.HIGH: "#F44336",
            Priority.MEDIUM: "#FF9800",
            Priority.LOW: "#4CAF50"
        }
        
        for priority in Priority:
            rb = ctk.CTkRadioButton(
                self.priority_frame,
                text=priority.label,
                variable=self.priority_var,
                value=priority.name,
                font=("Roboto", 12),
                fg_color=priority_colors[priority],
                hover_color=self._adjust_color(priority_colors[priority], -20)
            )
            rb.pack(side="left", padx=10)
        
        # Deadline
        self.deadline_label = ctk.CTkLabel(
            self.input_frame,
            text="Deadline",
            font=("Roboto", 14, "bold")
        )
        self.deadline_frame = ctk.CTkFrame(
            self.input_frame,
            fg_color="transparent"
        )
        
        # Use tkcalendar's DateEntry for date selection
        self.date_picker = DateEntry(
            self.deadline_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        
        # Time selection
        self.time_spinbox = ttk.Spinbox(
            self.deadline_frame,
            from_=0,
            to=23,
            width=5,
            format="%02.0f:00"
        )
        self.time_spinbox.set("12:00")
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Save Task",
            command=self._save_task,
            width=150,
            height=40,
            corner_radius=8,
            font=("Roboto", 14),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy,
            width=150,
            height=40,
            corner_radius=8,
            font=("Roboto", 14),
            fg_color="#F44336",
            hover_color="#d32f2f"
        )

    def _setup_layout(self):
        # Title
        self.title_frame.pack(fill="x", padx=20, pady=20)
        self.title_label.pack()
        
        # Input frame
        self.input_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Task title
        self.title_entry_label.pack(anchor="w", padx=15, pady=(15, 5))
        self.title_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Description
        self.desc_label.pack(anchor="w", padx=15, pady=(0, 5))
        self.desc_text.pack(fill="x", padx=15, pady=(0, 15))
        
        # Priority
        self.priority_label.pack(anchor="w", padx=15, pady=(0, 5))
        self.priority_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Deadline
        self.deadline_label.pack(anchor="w", padx=15, pady=(0, 5))
        self.deadline_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.date_picker.pack(side="left", padx=(15, 5))
        self.time_spinbox.pack(side="left")
        
        # Buttons
        self.button_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.cancel_btn.pack(side="right", padx=5)
        self.save_btn.pack(side="right", padx=5)

    def _save_task(self):
        # Get input values
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", "end-1c").strip()
        priority = Priority[self.priority_var.get()]
        
        # Get deadline
        date = self.date_picker.get_date()
        time = self.time_spinbox.get()
        hour = int(time.split(':')[0])
        deadline = datetime.combine(date, datetime.min.time().replace(hour=hour))
        
        # Validate inputs
        if not title:
            messagebox.showwarning("Warning", "Please enter a task title")
            return
            
        if deadline < datetime.now():
            messagebox.showwarning("Warning", "Deadline cannot be in the past")
            return
        
        # Create new task
        task = Task(
            title=title,
            description=description,
            priority=priority,
            deadline=deadline.strftime("%Y-%m-%d %H:%M")
        )
        
        # Add to task manager
        self.task_manager.add_task(task)
        messagebox.showinfo("Success", "Task added successfully!")
        self.destroy()

    def _adjust_color(self, hex_color, adjustment):
        """Adjust color brightness"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(max(0, min(255, c + adjustment)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

class ModernEditTaskDialog(ModernAddTaskDialog):
    def __init__(self, parent, task_manager, task):
        self.task = task
        super().__init__(parent, task_manager)
        self.title("Edit Task")
        self.title_label.configure(text="Edit Task")
        self._load_task_data()
        
    def _load_task_data(self):
        # Fill form with task data
        self.title_entry.insert(0, self.task.title)
        self.desc_text.insert("1.0", self.task.description)
        self.priority_var.set(self.task.priority.name)
        
        # Set deadline
        deadline = datetime.strptime(self.task.deadline, "%Y-%m-%d %H:%M")
        self.date_picker.set_date(deadline.date())
        self.time_spinbox.set(f"{deadline.hour:02d}:00")
        
    def _save_task(self):
        # Get input values
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", "end-1c").strip()
        priority = Priority[self.priority_var.get()]
        
        # Get deadline
        date = self.date_picker.get_date()
        time = self.time_spinbox.get()
        hour = int(time.split(':')[0])
        deadline = datetime.combine(date, datetime.min.time().replace(hour=hour))
        
        # Validate inputs
        if not title:
            messagebox.showwarning("Warning", "Please enter a task title")
            return
        
        # Update task
        self.task.title = title
        self.task.description = description
        self.task.priority = priority
        self.task.deadline = deadline.strftime("%Y-%m-%d %H:%M")
        
        messagebox.showinfo("Success", "Task updated successfully!")
        self.destroy()

class ModernStatisticsDialog(ctk.CTkToplevel):
    def __init__(self, parent, task_manager):
        super().__init__(parent)
        self.task_manager = task_manager
        
        self.title("Task Statistics")
        self.geometry("800x600")
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._setup_layout()
        self._load_statistics()
        
    def _create_widgets(self):
        # Title
        self.title_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Task Statistics & Analytics",
            font=("Roboto", 24, "bold"),
            text_color="#4A90E2"
        )
        
        # Stats containers
        self.stats_frame = ctk.CTkFrame(self, corner_radius=15)
        
        # Create stat cards
        self.cards = []
        card_configs = [
            ("Total Tasks", "0", "#4CAF50"),
            ("Completed Tasks", "0", "#2196F3"),
            ("Pending Tasks", "0", "#FF9800"),
            ("Overdue Tasks", "0", "#F44336")
        ]
        
        self.cards_frame = ctk.CTkFrame(
            self.stats_frame,
            fg_color="transparent"
        )
        
        for title, value, color in card_configs:
            card = self._create_stat_card(title, value, color)
            self.cards.append(card)
            
        # Priority distribution
        self.priority_frame = ctk.CTkFrame(
            self.stats_frame,
            corner_radius=10
        )
        
        self.priority_label = ctk.CTkLabel(
            self.priority_frame,
            text="Priority Distribution",
            font=("Roboto", 16, "bold")
        )
        
        self.priority_stats = ctk.CTkTextbox(
            self.priority_frame,
            height=100,
            font=("Roboto", 12)
        )
        
        # Button
        self.close_btn = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            width=150,
            height=40,
            corner_radius=8,
            font=("Roboto", 14)
        )
        
    def _create_stat_card(self, title, value, color):
        card = ctk.CTkFrame(
            self.cards_frame,
            corner_radius=10,
            border_width=2,
            border_color=color,
            width=150,
            height=100
        )
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Roboto", 14)
        )
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Roboto", 24, "bold"),
            text_color=color
        )
        
        title_label.pack(pady=(15, 5))
        value_label.pack(pady=(5, 15))
        
        return {
            'frame': card,
            'title': title_label,
            'value': value_label
        }
        
    def _setup_layout(self):
        # Title
        self.title_frame.pack(fill="x", padx=20, pady=20)
        self.title_label.pack()
        
        # Stats frame
        self.stats_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Cards
        self.cards_frame.pack(fill="x", padx=15, pady=15)
        for card in self.cards:
            card['frame'].pack(side="left", padx=10, fill="both", expand=True)
            
        # Priority distribution
        self.priority_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.priority_label.pack(pady=(15, 10))
        self.priority_stats.pack(padx=15, pady=(0, 15), fill="x")
        
        # Close button
        self.close_btn.pack(pady=(0, 20))
        
    def _load_statistics(self):
        now = datetime.now()
        
        # Calculate statistics
        total_tasks = len(self.task_manager.tasks)
        completed_tasks = len([t for t in self.task_manager.tasks if t.status == TaskStatus.COMPLETED])
        pending_tasks = total_tasks - completed_tasks
        overdue_tasks = len([
            t for t in self.task_manager.tasks
            if t.status != TaskStatus.COMPLETED and
            datetime.strptime(t.deadline, "%Y-%m-%d %H:%M") < now
        ])
        
        # Update stat cards
        stats = [total_tasks, completed_tasks, pending_tasks, overdue_tasks]
        for card, value in zip(self.cards, stats):
            card['value'].configure(text=str(value))
            
        # Calculate priority distribution
        priority_counts = {priority: 0 for priority in Priority}
        for task in self.task_manager.tasks:
            priority_counts[task.priority] += 1
            
        # Format priority statistics
        priority_stats = "Priority Distribution:\n\n"
        for priority, count in priority_counts.items():
            percentage = (count / total_tasks * 100) if total_tasks > 0 else 0
            priority_stats += f"{priority.label}: {count} tasks ({percentage:.1f}%)\n"
            
        self.priority_stats.delete("1.0", "end")
        self.priority_stats.insert("1.0", priority_stats)

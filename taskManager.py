import json
from tabulate import tabulate
from datetime import datetime, timedelta
import threading
from enum import Enum
import os
import colorama
from colorama import Fore, Style
from dataclasses import dataclass, asdict
from typing import Optional, List, Union

colorama.init()

class Priority(Enum):
    HIGH = ("Tinggi", "🔴")
    MEDIUM = ("Sedang", "🟡")
    LOW = ("Rendah", "🟢")

    def __init__(self, label: str, icon: str):
        self.label = label
        self.icon = icon

class TaskStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: Priority
    status: TaskStatus
    deadline: str
    created_at: str
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data['priority'] = self.priority.name
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        data['priority'] = Priority[data['priority']]
        data['status'] = TaskStatus(data['status'])
        return cls(**data)

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.task_id_counter = 1
        self.stop_thread = False
        self.deadline_check_thread = None

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_colored(text: str, color: str = Fore.WHITE):
        print(f"{color}{text}{Style.RESET_ALL}")

    def get_time_remaining(self, deadline: str) -> str:
        now = datetime.now()
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        if deadline_date < now:
            return "Terlambat"
        
        delta = deadline_date - now
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        
        if days > 0:
            return f"{days} hari {hours} jam"
        elif hours > 0:
            return f"{hours} jam {minutes} menit"
        return f"{minutes} menit"

    def add_task(self):
        while True:
            title = input("Masukkan nama tugas: ").strip()
            if title:
                break
            self.print_colored("Nama tugas tidak boleh kosong!", Fore.RED)
        
        description = input("Masukkan deskripsi tugas (opsional): ").strip()
        priority = self._get_priority()
        deadline = self._get_deadline()
        
        task = Task(
            id=self.task_id_counter,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING,
            deadline=deadline.strftime("%Y-%m-%d %H:%M"),
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        
        self.tasks.append(task)
        self.print_colored(f"\nTugas '{title}' berhasil ditambahkan!", Fore.GREEN)
        print(f"Deadline: {deadline.strftime('%Y-%m-%d %H:%M')}")
        self.task_id_counter += 1

    def _get_priority(self) -> Priority:
        print("\nPilih prioritas tugas:")
        for priority in Priority:
            print(f"{priority.value[0]}. {priority.label} {priority.icon}")
        
        while True:
            try:
                choice = int(input("Pilih prioritas (1-3): "))
                if 1 <= choice <= 3:
                    return list(Priority)[choice - 1]
                self.print_colored("Pilihan tidak valid!", Fore.RED)
            except ValueError:
                self.print_colored("Masukkan angka yang valid!", Fore.RED)

    def _get_deadline(self) -> datetime:
        now = datetime.now()
        deadline_options = {
            1: lambda: now.replace(hour=23, minute=59, second=0, microsecond=0),
            2: lambda: (now + timedelta(days=1)).replace(hour=23, minute=59, second=0, microsecond=0),
            3: lambda: (now + timedelta(days=(6 - now.weekday()))).replace(hour=23, minute=59, second=0, microsecond=0),
            4: lambda: now + timedelta(days=7),
            5: lambda: (now.replace(day=1, month=now.month + 1 if now.month < 12 else 1, 
                                  year=now.year + 1 if now.month == 12 else now.year) - timedelta(days=1))
                       .replace(hour=23, minute=59, second=0, microsecond=0),
            6: lambda: now + timedelta(days=30)
        }

        print("\nPilih opsi deadline:")
        deadline_descriptions = [
            "Hari ini (23:59)",
            "Besok (23:59)",
            "Minggu ini (Minggu, 23:59)",
            "Seminggu dari sekarang",
            "Akhir bulan ini",
            "Sebulan dari sekarang",
            "Custom (format: YYYY-MM-DD HH:MM)",
            "Custom (masukkan dalam hari)",
            "Custom (masukkan dalam jam)"
        ]

        for idx, desc in enumerate(deadline_descriptions, 1):
            print(f"{idx}. {desc}")

        while True:
            try:
                choice = int(input("\nPilih opsi deadline (1-9): "))
                if choice in deadline_options:
                    return deadline_options[choice]()
                elif choice == 7:
                    return self._get_custom_deadline()
                elif choice == 8:
                    return self._get_deadline_in_days()
                elif choice == 9:
                    return self._get_deadline_in_hours()
                self.print_colored("Pilihan tidak valid!", Fore.RED)
            except ValueError:
                self.print_colored("Masukkan angka yang valid!", Fore.RED)

    def _get_custom_deadline(self) -> datetime:
        while True:
            try:
                deadline_str = input("Masukkan deadline (format: YYYY-MM-DD HH:MM): ").strip()
                return datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            except ValueError:
                self.print_colored("Format deadline tidak valid! Gunakan format: YYYY-MM-DD HH:MM", Fore.RED)

    def _get_deadline_in_days(self) -> datetime:
        while True:
            try:
                days = int(input("Masukkan jumlah hari: "))
                if days > 0:
                    return datetime.now() + timedelta(days=days)
                self.print_colored("Jumlah hari harus lebih dari 0!", Fore.RED)
            except ValueError:
                self.print_colored("Masukkan angka yang valid!", Fore.RED)

    def _get_deadline_in_hours(self) -> datetime:
        while True:
            try:
                hours = int(input("Masukkan jumlah jam: "))
                if hours > 0:
                    return datetime.now() + timedelta(hours=hours)
                self.print_colored("Jumlah jam harus lebih dari 0!", Fore.RED)
            except ValueError:
                self.print_colored("Masukkan angka yang valid!", Fore.RED)

    def format_tasks_table(self, task_list: List[Task]) -> str:
        if not task_list:
            return "Tidak ada tugas!"
        
        table_data = []
        now = datetime.now()
        
        for task in task_list:
            status = "✔️" if task.status == TaskStatus.COMPLETED else "❌"
            deadline = datetime.strptime(task.deadline, "%Y-%m-%d %H:%M")
            
            if task.status != TaskStatus.COMPLETED:
                if deadline < now:
                    deadline_status = "🔴 Terlambat"
                elif (deadline - now) <= timedelta(days=1):
                    deadline_status = "🟡 Segera"
                else:
                    deadline_status = "🟢 Masih ada waktu"
                time_remaining = self.get_time_remaining(task.deadline)
            else:
                deadline_status = "✔️ Selesai"
                time_remaining = "-"

            description = task.description if task.description else "-"
            completed_at = task.completed_at if task.completed_at else "-"

            table_data.append([
                task.id,
                status,
                task.title,
                description[:30] + "..." if len(description) > 30 else description,
                task.priority.icon,
                task.deadline,
                deadline_status,
                time_remaining,
                completed_at
            ])
        
        headers = ["ID", "Status", "Judul", "Deskripsi", "Prioritas", "Deadline", 
                  "Status Deadline", "Sisa Waktu", "Selesai Pada"]
        return tabulate(table_data, headers=headers, tablefmt="grid")

    def view_tasks(self):
        self.clear_screen()
        print(self.format_tasks_table(self.tasks))

    def mark_task_completed(self):
        self.view_tasks()
        try:
            task_id = int(input("\nMasukkan ID tugas yang ingin ditandai selesai: "))
            task = next((t for t in self.tasks if t.id == task_id), None)
            if task:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.print_colored(f"Tugas '{task.title}' berhasil ditandai selesai!", Fore.GREEN)
            else:
                self.print_colored("ID tugas tidak ditemukan!", Fore.RED)
        except ValueError:
            self.print_colored("ID harus berupa angka!", Fore.RED)

    def delete_task(self):
        self.view_tasks()
        try:
            task_id = int(input("\nMasukkan ID tugas yang ingin dihapus: "))
            task = next((t for t in self.tasks if t.id == task_id), None)
            if task:
                self.tasks.remove(task)
                self.print_colored(f"Tugas '{task.title}' berhasil dihapus!", Fore.GREEN)
            else:
                self.print_colored("ID tugas tidak ditemukan!", Fore.RED)
        except ValueError:
            self.print_colored("ID harus berupa angka!", Fore.RED)

    def edit_task(self):
        self.view_tasks()
        try:
            task_id = int(input("\nMasukkan ID tugas yang ingin diedit: "))
            task = next((t for t in self.tasks if t.id == task_id), None)
            if task:
                print("\nBiarkan kosong jika tidak ingin mengubah")
                
                title = input(f"Judul baru (sekarang: {task.title}): ").strip()
                if title:
                    task.title = title
                
                description = input(f"Deskripsi baru (sekarang: {task.description}): ").strip()
                if description:
                    task.description = description
                
                if input("Ubah prioritas? (y/n): ").lower() == 'y':
                    task.priority = self._get_priority()
                
                if input("Ubah deadline? (y/n): ").lower() == 'y':
                    task.deadline = self._get_deadline().strftime("%Y-%m-%d %H:%M")
                
                self.print_colored(f"Tugas '{task.title}' berhasil diperbarui!", Fore.GREEN)
            else:
                self.print_colored("ID tugas tidak ditemukan!", Fore.RED)
        except ValueError:
            self.print_colored("ID harus berupa angka!", Fore.RED)

    def search_task(self):
        keyword = input("Masukkan kata kunci pencarian: ").lower()
        found_tasks = [
            task for task in self.tasks
            if keyword in task.title.lower() or 
               keyword in task.description.lower()
        ]
        self.clear_screen()
        print(self.format_tasks_table(found_tasks))

    def save_tasks(self):
        filename = input("Masukkan nama file untuk menyimpan tugas (contoh: tasks.json): ")
        try:
            with open(filename, 'w') as file:
                json.dump([task.to_dict() for task in self.tasks], file, indent=4)
            self.print_colored(f"Tugas berhasil disimpan ke file '{filename}'!", Fore.GREEN)
        except Exception as e:
            self.print_colored(f"Gagal menyimpan file: {str(e)}", Fore.RED)

    def load_tasks(self):
        filename = input("Masukkan nama file untuk memuat tugas (contoh: tasks.json): ")
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
                if self.tasks:
                    self.task_id_counter = max(task.id for task in self.tasks) + 1
            self.print_colored(f"Tugas berhasil dimuat dari file '{filename}'!", Fore.GREEN)
        except FileNotFoundError:
            self.print_colored(f"File '{filename}' tidak ditemukan!", Fore.RED)
        except json.JSONDecodeError:
            self.print_colored("Format file tidak valid!", Fore.RED)
        except Exception as e:
            self.print_colored(f"Gagal memuat file: {str(e)}", Fore.RED)

    def show_statistics(self):
        self.clear_screen()
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            self.print_colored("Belum ada tugas yang ditambahkan!", Fore.YELLOW)
            return

        completed_tasks = sum(1 for task in self.tasks if task.status == TaskStatus.COMPLETED)
        pending_tasks = total_tasks - completed_tasks
        now = datetime.now()
        overdue_tasks = sum(1 for task in self.tasks 
                           if task.status == TaskStatus.PENDING 
                           and datetime.strptime(task.deadline, "%Y-%m-%d %H:%M") < now)
        
        priority_counts = {priority: sum(1 for task in self.tasks if task.priority == priority)
                         for priority in Priority}
        
        self.print_colored(f"\nStatistik Tugas:", Fore.CYAN)
        print(f"Total tugas         : {total_tasks}")
        print(f"Tugas selesai       : {completed_tasks}")
        print(f"Tugas pending       : {pending_tasks}")
        print(f"Tugas terlambat     : {overdue_tasks}")
        
        print("\nJumlah tugas berdasarkan prioritas:")
        for priority, count in priority_counts.items():
            print(f"{priority.icon} {priority.label}: {count}")

    def deadline_check_worker(self):
        while not self.stop_thread:
            now = datetime.now()
            for task in self.tasks:
                if (
                    task.status == TaskStatus.PENDING and
                    datetime.strptime(task.deadline, "%Y-%m-%d %H:%M") < now
                ):
                    self.print_colored(f"\n⚠️ Tugas '{task.title}' telah melewati deadline!", Fore.RED)
            threading.Event().wait(60)  # Tunggu 60 detik sebelum mengecek lagi

    def start_deadline_check(self):
        if self.deadline_check_thread is None or not self.deadline_check_thread.is_alive():
            self.deadline_check_thread = threading.Thread(target=self.deadline_check_worker, daemon=True)
            self.deadline_check_thread.start()

    def stop_deadline_check(self):
        self.stop_thread = True
        if self.deadline_check_thread is not None:
            self.deadline_check_thread.join()

    def run(self):
        self.start_deadline_check()
        while True:
            self.clear_screen()
            print("=== Task Manager ===")
            print("1. Tambah Tugas")
            print("2. Lihat Semua Tugas")
            print("3. Tandai Tugas Selesai")
            print("4. Hapus Tugas")
            print("5. Edit Tugas")
            print("6. Cari Tugas")
            print("7. Simpan Tugas ke File")
            print("8. Muat Tugas dari File")
            print("9. Lihat Statistik")
            print("0. Keluar")
            
            try:
                choice = int(input("\nPilih menu: "))
                if choice == 1:
                    self.add_task()
                elif choice == 2:
                    self.view_tasks()
                    input("\nTekan Enter untuk kembali ke menu...")
                elif choice == 3:
                    self.mark_task_completed()
                    input("\nTekan Enter untuk kembali ke menu...")
                elif choice == 4:
                    self.delete_task()
                    input("\nTekan Enter untuk kembali ke menu...")
                elif choice == 5:
                    self.edit_task()
                    input("\nTekan Enter untuk kembali ke menu...")
                elif choice == 6:
                    self.search_task()
                    input("\nTekan Enter untuk kembali ke menu...")
                elif choice == 7:
                    self.save_tasks()
                    input("\nTekan Enter untuk kembali ke menu...")
                elif choice == 8:
                    self.load_tasks()
                    input("\nTekan Enter untuk kembali ke menu...")
                elif choice == 9:
                    self.show_statistics()
                    input("\nTekan Enter untuk kembali ke menu...")
                elif choice == 0:
                    self.stop_deadline_check()
                    self.print_colored("Terima kasih telah menggunakan Task Manager!", Fore.CYAN)
                    break
                else:
                    self.print_colored("Pilihan tidak valid!", Fore.RED)
            except ValueError:
                self.print_colored("Masukkan angka yang valid!", Fore.RED)
            except Exception as e:
                self.print_colored(f"Terjadi kesalahan: {str(e)}", Fore.RED)
if __name__ == "__main__":
    try:
        print("Pilih mode aplikasi:")
        print("1. Command Line Interface (CLI)")
        print("2. Graphical User Interface (GUI)")
        
        choice = input("Pilihan (1/2): ").strip()
        
        task_manager = TaskManager()
        
        if choice == "1":
            task_manager.run()
        elif choice == "2":
            from taskManagerUI import TaskManagerUI
            app = TaskManagerUI(task_manager)
            app.mainloop()
        else:
            TaskManager.print_colored("Pilihan tidak valid!", Fore.RED)
            
    except KeyboardInterrupt:
        task_manager.stop_deadline_check()
        TaskManager.print_colored("\nProgram dihentikan oleh pengguna.", Fore.CYAN)
    except Exception as e:
        TaskManager.print_colored(f"Terjadi kesalahan fatal: {str(e)}", Fore.RED)

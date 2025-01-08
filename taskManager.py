import json
from tabulate import tabulate
from datetime import datetime, timedelta
import time
import threading
import os

tasks = []
task_id_counter = 1
deadline_check_thread = None
stop_thread = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    print("\n=== Task Manager ===")
    print("1. Tambahkan tugas")
    print("2. Lihat semua tugas")
    print("3. Tandai tugas selesai")
    print("4. Hapus tugas")
    print("5. Edit tugas")
    print("6. Filter tugas berdasarkan status")
    print("7. Cari tugas")
    print("8. Simpan tugas ke file")
    print("9. Muat tugas dari file")
    print("10. Keluar")

def parse_deadline(deadline_str):
    try:
        return datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

def get_deadline_from_option():
    now = datetime.now()
    print("\nPilih opsi deadline:")
    print("1. Hari ini (23:59)")
    print("2. Besok (23:59)")
    print("3. Minggu ini (Minggu, 23:59)")
    print("4. Seminggu dari sekarang")
    print("5. Akhir bulan ini")
    print("6. Sebulan dari sekarang")
    print("7. Custom (format: YYYY-MM-DD HH:MM)")
    print("8. Custom (masukkan dalam hari)")
    
    choice = input("\nPilih opsi deadline (1-8): ")
    
    if choice == "1":
        return now.replace(hour=23, minute=59, second=0, microsecond=0)
    elif choice == "2":
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=23, minute=59, second=0, microsecond=0)
    elif choice == "3":
        days_until_sunday = 6 - now.weekday()
        sunday = now + timedelta(days=days_until_sunday)
        return sunday.replace(hour=23, minute=59, second=0, microsecond=0)
    elif choice == "4":
        return now + timedelta(days=7)
    elif choice == "5":
        if now.month == 12:
            next_month = now.replace(year=now.year + 1, month=1, day=1)
        else:
            next_month = now.replace(month=now.month + 1, day=1)
        end_of_month = next_month - timedelta(days=1)
        return end_of_month.replace(hour=23, minute=59, second=0, microsecond=0)
    elif choice == "6":
        return now + timedelta(days=30)
    elif choice == "7":
        while True:
            deadline_str = input("Masukkan deadline (format: YYYY-MM-DD HH:MM): ").strip()
            deadline = parse_deadline(deadline_str)
            if deadline:
                return deadline
            print("Format deadline tidak valid! Gunakan format: YYYY-MM-DD HH:MM")
    elif choice == "8":
        while True:
            try:
                days = int(input("Masukkan jumlah hari: "))
                if days > 0:
                    return now + timedelta(days=days)
                print("Jumlah hari harus lebih dari 0!")
            except ValueError:
                print("Masukkan angka yang valid!")
    else:
        print("Pilihan tidak valid! Menggunakan default: seminggu dari sekarang")
        return now + timedelta(days=7)

def add_task():
    global task_id_counter
    while True:
        title = input("Masukkan nama tugas: ").strip()
        if title:
            break
        print("Nama tugas tidak boleh kosong!")
    
    deadline = get_deadline_from_option()
    
    task = {
        "id": task_id_counter,
        "title": title,
        "status": "Pending",
        "deadline": deadline.strftime("%Y-%m-%d %H:%M"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    print(f"\nTugas '{title}' berhasil ditambahkan!")
    print(f"Deadline: {deadline.strftime('%Y-%m-%d %H:%M')}")
    task_id_counter += 1

def format_tasks_table(task_list):
    if not task_list:
        return "Tidak ada tugas!"
    
    table_data = []
    for task in task_list:
        status = "✔️" if task["status"] == "Completed" else "❌"
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
        now = datetime.now()
        
        if task["status"] != "Completed":
            if deadline < now:
                deadline_status = "🔴 Terlambat"
            elif (deadline - now) <= timedelta(days=1):
                deadline_status = "🟡 Segera"
            else:
                deadline_status = "🟢 Masih ada waktu"
        else:
            deadline_status = "✔️ Selesai"

        table_data.append([
            task["id"],
            status,
            task["title"],
            task["deadline"],
            deadline_status
        ])
    
    headers = ["ID", "Status", "Judul", "Deadline", "Status Deadline"]
    return tabulate(table_data, headers=headers, tablefmt="grid")

def view_tasks():
    clear_screen()
    print(format_tasks_table(tasks))

def check_deadlines():
    global stop_thread
    while not stop_thread:
        now = datetime.now()
        for task in tasks:
            if task["status"] != "Completed":
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
                if deadline > now and (deadline - now) <= timedelta(minutes=15):
                    print(f"\n⚠️ PENGINGAT: Tugas '{task['title']}' akan berakhir dalam {int((deadline - now).total_seconds() / 60)} menit!")
        time.sleep(60)  # Cek setiap menit

def mark_task_completed():
    view_tasks()
    try:
        task_id = int(input("\nMasukkan ID tugas yang ingin ditandai selesai: "))
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "Completed"
                print(f"Tugas '{task['title']}' berhasil ditandai selesai!")
                return
        print("ID tugas tidak ditemukan!")
    except ValueError:
        print("ID harus berupa angka!")

def delete_task():
    view_tasks()
    try:
        task_id = int(input("\nMasukkan ID tugas yang ingin dihapus: "))
        for task in tasks:
            if task["id"] == task_id:
                tasks.remove(task)
                print(f"Tugas '{task['title']}' berhasil dihapus!")
                return
        print("ID tugas tidak ditemukan!")
    except ValueError:
        print("ID harus berupa angka!")

def edit_task():
    view_tasks()
    try:
        task_id = int(input("\nMasukkan ID tugas yang ingin diubah: "))
        for task in tasks:
            if task["id"] == task_id:
                new_title = input(f"Masukkan nama baru untuk tugas '{task['title']}' (kosongkan jika tidak ingin mengubah): ")
                if new_title.strip():
                    task["title"] = new_title

                new_deadline = input(f"Masukkan deadline baru (format: YYYY-MM-DD HH:MM) (kosongkan jika tidak ingin mengubah): ")
                if new_deadline.strip():
                    deadline = parse_deadline(new_deadline)
                    if deadline:
                        task["deadline"] = deadline.strftime("%Y-%m-%d %H:%M")
                    else:
                        print("Format deadline tidak valid! Deadline tidak diubah.")
                
                print(f"Tugas berhasil diubah!")
                return
        print("ID tugas tidak ditemukan!")
    except ValueError:
        print("ID harus berupa angka!")

def filter_tasks():
    status = input("Masukkan status untuk memfilter tugas (Pending/Completed): ").capitalize()
    filtered_tasks = [task for task in tasks if task["status"] == status]
    clear_screen()
    print(format_tasks_table(filtered_tasks))

def search_task():
    keyword = input("Masukkan kata kunci untuk mencari tugas: ").lower()
    found_tasks = [task for task in tasks if keyword in task["title"].lower()]
    clear_screen()
    print(format_tasks_table(found_tasks))

def save_tasks_to_file():
    filename = input("Masukkan nama file untuk menyimpan tugas (contoh: tasks.json): ")
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)
    print(f"Tugas berhasil disimpan ke file '{filename}'!")

def load_tasks_from_file():
    global task_id_counter
    filename = input("Masukkan nama file untuk memuat tugas (contoh: tasks.json): ")
    try:
        with open(filename, 'r') as file:
            global tasks
            tasks = json.load(file)
            if tasks:
                task_id_counter = max(task["id"] for task in tasks) + 1
        print(f"Tugas berhasil dimuat dari file '{filename}'!")
    except FileNotFoundError:
        print(f"File '{filename}' tidak ditemukan!")
    except (json.JSONDecodeError, ValueError):
        print("Format file tidak valid! Tidak ada tugas yang dimuat.")

def main():
    global stop_thread, deadline_check_thread
    
    # Memulai thread untuk mengecek deadline
    deadline_check_thread = threading.Thread(target=check_deadlines)
    deadline_check_thread.daemon = True
    deadline_check_thread.start()
    
    while True:
        show_menu()
        choice = input("Pilih opsi (1-10): ")
        clear_screen()
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_task_completed()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            edit_task()
        elif choice == "6":
            filter_tasks()
        elif choice == "7":
            search_task()
        elif choice == "8":
            save_tasks_to_file()
        elif choice == "9":
            load_tasks_from_file()
        elif choice == "10":
            stop_thread = True
            if deadline_check_thread:
                deadline_check_thread.join(timeout=1)
            print("Keluar dari program. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()

import json

tasks = []
task_id_counter = 1

def show_menu():
    print("\nTask Manager")
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

def add_task():
    global task_id_counter
    title = input("Masukkan nama tugas: ")
    task = {
        "id": task_id_counter,
        "title": title,
        "status": "Pending"
    }
    tasks.append(task)
    print(f"Tugas '{title}' berhasil ditambahkan!")
    task_id_counter += 1

def view_tasks():
    if not tasks:
        print("Tidak ada tugas!")
    else:
        for i, task in enumerate(tasks, start=1):
            status = "✔️" if task["status"] == "Completed" else "❌"
            print(f"{i}. [{status}] {task['title']} (ID: {task['id']})")

def mark_task_completed():
    view_tasks()
    try:
        task_id = int(input("Masukkan ID tugas yang ingin ditandai selesai: "))
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
        task_id = int(input("Masukkan ID tugas yang ingin dihapus: "))
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
        task_id = int(input("Masukkan ID tugas yang ingin diubah: "))
        for task in tasks:
            if task["id"] == task_id:
                new_title = input(f"Masukkan nama baru untuk tugas '{task['title']}': ")
                task["title"] = new_title
                print(f"Tugas '{task['title']}' berhasil diubah!")
                return
        print("ID tugas tidak ditemukan!")
    except ValueError:
        print("ID harus berupa angka!")

def filter_tasks():
    status = input("Masukkan status untuk memfilter tugas (Pending/Completed): ").capitalize()
    filtered_tasks = [task for task in tasks if task["status"] == status]
    if not filtered_tasks:
        print(f"Tidak ada tugas dengan status '{status}'!")
    else:
        for i, task in enumerate(filtered_tasks, start=1):
            print(f"{i}. {task['title']} (ID: {task['id']})")

def search_task():
    keyword = input("Masukkan kata kunci untuk mencari tugas: ").lower()
    found_tasks = [task for task in tasks if keyword in task["title"].lower()]
    if not found_tasks:
        print(f"Tidak ada tugas yang cocok dengan kata kunci '{keyword}'!")
    else:
        for i, task in enumerate(found_tasks, start=1):
            print(f"{i}. {task['title']} (ID: {task['id']})")

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
    except json.JSONDecodeError:
        print("Format file tidak valid!")

def main():
    while True:
        show_menu()
        choice = input("Pilih opsi (1-10): ")
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
            print("Keluar dari program. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()

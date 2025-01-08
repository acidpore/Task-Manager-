tasks = []
task_id_counter = 1

def show_menu():
    print("\nTask Manager")
    print("1. Tambahkan tugas")
    print("2. Lihat semua tugas")
    print("3. Tandai tugas selesai")
    print("4. Hapus tugas")
    print("5. Keluar")

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

def main():
    while True:
        show_menu()
        choice = input("Pilih opsi (1-5): ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_task_completed()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Keluar dari program. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()

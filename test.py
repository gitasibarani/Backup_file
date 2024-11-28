import os
import shutil
import time
from plyer import notification

def backup_files(source_dir, backup_dir):
    """
    Fungsi untuk melakukan backup file dari satu direktori sumber ke direktori tujuan.
    Hanya file yang baru atau telah diubah yang akan disalin.
    """
    try:
        # Memastikan direktori tujuan ada, jika tidak buat baru
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Menyalin file satu per satu dari sumber ke tujuan
        for filename in os.listdir(source_dir):
            source_path = os.path.join(source_dir, filename)
            backup_path = os.path.join(backup_dir, filename)

            if os.path.isfile(source_path):
                if os.path.exists(backup_path):
                    # Cek timestamp terakhir modifikasi file
                    source_time = os.path.getmtime(source_path)
                    backup_time = os.path.getmtime(backup_path)
                    if source_time > backup_time:
                        shutil.copy2(source_path, backup_path)
                        print(f"File {filename} diperbarui di backup.")
                    else:
                        print(f"File {filename} tidak berubah, tidak perlu di-backup.")
                else:
                    shutil.copy2(source_path, backup_path)
                    print(f"File baru {filename} di-backup.")

        # Menampilkan notifikasi ketika backup selesai
        notification.notify(
            title="Backup Selesai",
            message=f"Backup file dari {source_dir} ke {backup_dir} berhasil.",
            timeout=10
        )

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def backup_multiple_directories(source_dirs, backup_dir, interval):
    """
    Fungsi untuk melakukan backup dari beberapa direktori sumber ke satu direktori tujuan.
    
    Parameters:
    - source_dirs: list, daftar direktori sumber yang akan di-backup.
    - backup_dir: string, path dari direktori tujuan.
    - interval: int, waktu (dalam detik) antar backup.
    """
    while True:
        for source_dir in source_dirs:
            # Membuat sub-direktori di backup_dir berdasarkan nama folder sumber
            source_folder_name = os.path.basename(source_dir.rstrip(os.sep))
            current_backup_dir = os.path.join(backup_dir, source_folder_name)

            print(f"\nBackup folder: {source_dir} ke {current_backup_dir}")
            backup_files(source_dir, current_backup_dir)

        time.sleep(interval)

if __name__ == "__main__":
   
    source_directories = [
        r"D:\Tugas",
        r"D:\LAPORAN"
    ]
    
    # Direktori tujuan untuk backup
    backup_directory = r"D:\DevOps\hasil_backup"
    
    # Interval backup dalam detik
    backup_interval = 3600

    # Jalankan backup otomatis dari beberapa direktori
    backup_multiple_directories(source_directories, backup_directory, backup_interval)

import os
import shutil
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Konfigurasi
SOURCE_DIR = "D:\\msib_SEAL"  
BACKUP_DIR = "D:\\DevOps\\hasil_backup"  
LOG_FILE = "backup_log.txt"    

# Konfigurasi email notifikasi
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "itsmeurfavgirl01@gmail.com"  
EMAIL_PASSWORD = "Grs270121"       
EMAIL_RECEIVER = "gitasyalalalin27@gmail.com"  

def backup_files():
    """Fungsi untuk melakukan backup file dari source ke backup directory."""
    try:
        # Tanggal dan waktu saat ini
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Cek apakah folder tujuan ada
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

        # Lakukan backup file
        for filename in os.listdir(SOURCE_DIR):
            source_path = os.path.join(SOURCE_DIR, filename)
            backup_path = os.path.join(BACKUP_DIR, filename)

            # Salin file jika belum ada di folder backup atau jika diupdate
            if os.path.isfile(source_path):
                if not os.path.exists(backup_path) or os.path.getmtime(source_path) > os.path.getmtime(backup_path):
                    shutil.copy2(source_path, backup_path)

        # Catat riwayat backup
        with open(LOG_FILE, "a") as log:
            log.write(f"{timestamp} - Backup successful\n")

        # Kirim notifikasi email
        send_notification(f"Backup completed at {timestamp}")
        print(f"Backup completed at {timestamp}")

    except Exception as e:
        error_message = f"Backup failed: {e}"
        with open(LOG_FILE, "a") as log:
            log.write(f"{timestamp} - {error_message}\n")
        send_notification(error_message)
        print(error_message)


def send_notification(message):
    """Fungsi untuk mengirim notifikasi email."""
    try:
        # Buat pesan email
        msg = MIMEText(message)
        msg["Subject"] = "Backup Notification"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        # Kirim email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print("Notification email sent.")

    except Exception as e:
        print(f"Failed to send notification email: {e}")


if __name__ == "__main__":
    backup_files()

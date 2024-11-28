import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Konfigurasi Logging
logging.basicConfig(
    filename='backup_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def send_notification(email_config, subject, body):
    """
    Mengirim notifikasi email.
    :param email_config: Dictionary berisi konfigurasi email
    :param subject: Subjek email
    :param body: Isi email
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = email_config['sender_email']
        msg['To'] = email_config['recipient_email']
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Koneksi ke SMTP Server
        with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.starttls()
            server.login(email_config['sender_email'], email_config['password'])
            server.send_message(msg)
            logger.info("Notification email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send notification email: {e}")

def backup_folder(source, destination):
    """
    Melakukan backup folder dan isinya (termasuk folder kosong).
    :param source: Path folder sumber
    :param destination: Path folder tujuan
    """
    try:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source folder '{source}' not found.")
        if not os.path.exists(destination):
            os.makedirs(destination)
        
        for item in os.listdir(source):
            source_path = os.path.join(source, item)
            destination_path = os.path.join(destination, item)
            if os.path.isdir(source_path):  
                backup_folder(source_path, destination_path)  
            else:  
                shutil.copy2(source_path, destination_path)
        logger.info(f"Backup '{source}' to '{destination}' completed.")
    except Exception as e:
        logger.error(f"Error during backup: {e}")
        raise e

def backup_folder(source, destination):
    """
    Melakukan backup folder dan isinya (termasuk folder kosong).
    :param source: Path folder sumber
    :param destination: Path folder tujuan
    """
    try:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source folder '{source}' not found.")
        if not os.path.exists(destination):
            os.makedirs(destination)
        
        for item in os.listdir(source):
            # Mengabaikan folder .git
            if item == '.git':
                continue
            
            source_path = os.path.join(source, item)
            destination_path = os.path.join(destination, item)
            try:
                if os.path.isdir(source_path):  
                    backup_folder(source_path, destination_path)  
                else:  
                    shutil.copy2(source_path, destination_path)
            except PermissionError:
                # Jika ada PermissionError, catat di log dan lanjutkan ke file berikutnya
                logger.error(f"Permission denied: {source_path}")
                continue  # Abaikan file/folder yang tidak dapat diakses

        logger.info(f"Backup '{source}' to '{destination}' completed.")
    except Exception as e:
        logger.error(f"Error during backup: {e}")
        raise e


# Konfigurasi Email
email_config = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'gitarosalinasibarani@gmail.com', 
    'password': 'w a a x o m v v k i i s g z n p',  
    'recipient_email': 'sibaranigitarosalina@gmail.com'  
}

# Path Backup
source_folder = "C:\\sib7"  
destination_folder = "D:\\Devops\\backup_result" 

# Proses Backup
try:
    backup_folder(source_folder, destination_folder)
    message = f"Backup from '{source_folder}' to '{destination_folder}' completed successfully."
    logger.info(message)
    send_notification(email_config, "Backup Success", message)
except Exception as e:
    error_message = f"Backup failed: {e}"
    logger.error(error_message)
    send_notification(email_config, "Backup Failed", error_message)

from ecpy.curves import Curve
from crypto_operations import generate_keypair, encrypt,decrypt, calculate_md5
from file_operations import file_read
from mail_operations import send_email
from authentication.user_management import UserManagement
import tkinter as tk
from tkinter import filedialog
import os
import socket
import ssl
import threading
import logging

global curve, public_key, private_key, original_md5, message


logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup():
    global curve, public_key, private_key, original_md5, message
    curve = Curve.get_curve('secp384r1')
    public_key, private_key = generate_keypair(curve)

    root = tk.Tk()

    # Dosya seçme penceresini aç
    input_file_path = filedialog.askopenfilename(title="Select Input File", initialdir=os.path.expanduser("~/Desktop"))

    if input_file_path:
        # Kontrol etmek için dosyanın varlığını kontrol et
        if os.path.exists(input_file_path):
            message = file_read(input_file_path)
            original_md5 = calculate_md5(message)
            root.destroy()
        else:
            print("File not found. Please select a valid file.")
            root.destroy()
    else:
        print("No file selected. Exiting setup.")
        
   
# mesajı şifrele ve private keyi mail ile gönder 
def encrypt_and_send_mail():
    try:
        to_email = "smpt@gmail.com"
        subject = "Private Key"
        body = f"Özel Anahtar:\n{private_key}"

        smtp_server = "smtp.gmail.com"
        smtp_port = 465 #587
        smtp_user = "smtp@gmail.com"
        smtp_password = "2 fa auth şifre alımı gerekiyor"

        send_email(to_email, subject, body, smtp_server, smtp_port, smtp_user, smtp_password)
        print('Private key E-posta ile Gönderildi')
        #print("Private key: ",private_key)
        
        ciphertext = encrypt(public_key, message, curve)
        
        print('Encrypted:', ciphertext.hex())
        print('Original MD5:', original_md5.hex())
        logging.info('Desifreleme ve Dogrulama islemi basariyla tamamlandi.')
        return ciphertext
    except Exception as e:
        # Loglama - Hata durumu
        logging.error(f'Hata oluştu: {str(e)}')
        print('Hata oluştu. Detaylar için log dosyasına bakınız.')
        


def decrypt_and_verify(ciphertext):
    try:  
        private_key = int(input("Mail yoluyla gelen private key: "))
        
        decrypted = decrypt(curve, private_key, ciphertext).decode('utf-8')
        print('Decrypted:', decrypted)

        # Şifre çözülmüş verinin MD5 hash'ini hesapla
        decrypted_md5 = calculate_md5(decrypted.encode('utf-8'))
        print('Decrypted MD5:', decrypted_md5.hex())

        # Veri bütünlüğünü kontrol et
        if original_md5 == decrypted_md5:
            print("Veri bütünlüğü doğrulandı.")
        else:
            print("Veri bütünlüğü doğrulanamadı.")
    except Exception as e:
        # Loglama - Genel hata durumu
        logging.error(f'Uygulama çalışırken bir hata oluştu: {str(e)}')
        print('Uygulama çalışırken bir hata oluştu. Detaylar için log dosyasına bakınız.')




def main():
    try:
        logging.info('Uygulama baslatildi.')
        user_manager = UserManagement()
        global user
        global ciphertext
        while True:
            print("\n1. Kullanici Kaydı\n2. Kullanici Girişi\n3. Kullanici Silme\n4. Dosya şifrele\n5. Deşifrele\n6. Çıkış")
            choice = input("Seçiminizi yapın (1/2/3/4/5/6): ")

            if choice == "1":
                logging.info("Kullanici secenek 1'i seçti.")
                user_manager.register_user()
                logging.info('Kullanici başarıyla kayıt oldu.')
            elif choice == "2":
                logging.info("Kullanici secenek 2'yi seçti.")
                user = user_manager.login()
                logging.info('Kullanici başarıyla giriş yaptı.')
            elif choice == "3":
                logging.info("Kullanici secenek 3'ü seçti.")
                user_manager.delete_user()
                logging.info('Kullanici başarıyla silindi.')
            elif choice == "4":
                logging.info("Kullanici secenek 4'ü seçti.")
                if user: 
                    setup()   
                    ciphertext = encrypt_and_send_mail()
                    logging.info('Dosya sifrelendi ve private key mail yoluyla gonderildi.')
            elif choice == "5":
                logging.info("Kullanici secenek 5'i seçti.")
                if user:                
                    decrypt_and_verify(ciphertext) 
            elif choice == "6":
                logging.info("Kullanici cikis yapti.")
                print("Çıkılıyor.")
                break
            else:
                logging.error(f'Geçersiz seçenek. Lütfen tekrar deneyin: {str(e)}')
                print("Geçersiz seçenek. Lütfen tekrar deneyin.")
    except Exception as e:
        # Loglama - Genel hata durumu
        logging.error(f'Uygulama calisirken bir hata oluştu: {str(e)}')
        print('Uygulama calisirken bir hata oluştu. Detaylar için log dosyasina bakiniz.')


if __name__ == "__main__":
    main()


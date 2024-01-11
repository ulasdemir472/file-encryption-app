import sqlite3
import getpass
from hash import sha256
import math

class UserManagement:
    def __init__(self, db_file='user_database.db'):
        self.db_file = db_file
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Kullanıcı tablosunu oluştur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def register_user(self):
        username = input("Kullanıcı Adı: ")
        password = getpass.getpass("Şifre: ")

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Kullanıcıyı veritabanına ekle
        try:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hex(sha256(password.encode()))))
            print(f"{username} başarıyla kaydedildi.")
        except sqlite3.IntegrityError:
            print(f"{username} zaten var. Lütfen farklı bir kullanıcı adı seçin.")

        conn.commit()
        conn.close()

    def login(self):
        username = input("Kullanıcı Adı: ")
        password = getpass.getpass("Şifre: ")

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Kullanıcıyı kontrol et
        cursor.execute('SELECT * FROM users WHERE username=? AND password_hash=?', (username,hex(sha256(password.encode()))))
        user = cursor.fetchone()

        conn.close()

        if user:
            print(f"{username} başarıyla giriş yaptı.")
            return user
        else:
            print("Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.")
            return False
        
        
    def delete_user(self):
        username = input("Silmek istediğiniz kullanıcı adını girin: ")
        password = getpass.getpass("Şifrenizi girin: ")

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Kullanıcıyı kontrol et
        cursor.execute('SELECT * FROM users WHERE username=? AND password_hash=?', (username, hex(sha256(password.encode()))))
        user = cursor.fetchone()

        if user:
            # Kullanıcıyı sil
            cursor.execute('DELETE FROM users WHERE username=?', (username,))
            print(f"{username} başarıyla silindi.")
        else:
            print("Kullanıcı adı veya şifre hatalı. Silme işlemi başarısız.")

        conn.commit()
        conn.close()
        



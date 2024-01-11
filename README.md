# Proje açmak için
git clone https://github.com/ulasdemir472/file-encryption-app.git
python main.py

# Proje Açıklaması
Kullanıcının dosya şifrelemek için öncelikle kayıt olup giriş yapması lazım.
Parola hash.py dosyasında bulunan sha256 algoritmasının koduyla şifrelenir ve db ye kaydedilir.
Şifrelenecek dosya seçildikten sonra private key mail yoluyla gönderilir seçilen maile.
Mail için bir şifre gerekiyor.(Google dan bakılabilir)
Encrypt kısmında eliptik eğri ve bütünlük için md5 yöntemi kullanılır.
Decrypt seçeneği ile de deşifrelenme sağlanır.
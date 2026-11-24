# Talabalar boshqaruvi (PyQt5 + MySQL)

Desktop dastur: talabalar, o'qituvchilar, fakultetlar, guruhlar, fanlar va baholarni boshqarish,
bosh sahifada hisoblagich va diagrammalar, hisobotni Excelga eksport qilish.

## Talablar
- Python 3.10+ (3.13 da tekshirilgan)
- MySQL 8.0.16+ (26.10 da tekshirilgan, CHECK cheklovlari uchun kerak), ishlab turgan bo'lishi kerak

## MySQL o'rnatish (macOS, bir marta)
```bash
brew install mysql
brew services start mysql      # root foydalanuvchi, parolsiz (faqat o'z kompyuteringizda)
```

## O'rnatish va ishga tushirish (macOS / Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m app.init_db      # baza + 8 jadval + namuna ma'lumot (qayta ishga tushirsa ham xavfsiz)
python -m app.main         # dasturni ochish
```
Windows: `.venv\Scripts\activate` (qolgani bir xil).

## MySQL sozlamalari
Default: `localhost:3306`, baza `talaba_db`, foydalanuvchi `root`, parolsiz. Boshqacha bo'lsa:
```bash
export DB_USER=root DB_PASSWORD=sirparol DB_HOST=localhost DB_PORT=3306 DB_NAME=talaba_db
```

## Tekshirish
```bash
DB_NAME=talaba_test python -m app.init_db
DB_NAME=talaba_test python -m tests.smoke_test      # "Hammasi OK" chiqishi kerak
```

## Tuzilma
```
sql/schema.sql, sql/seed.sql   jadvallar va namuna ma'lumot
app/config.py                  baza sozlamasi
app/style.py                   dizayn (QSS)
app/db.py                      query() va execute()
app/init_db.py                 bazani yaratish
app/widgets.py                 diagramma
app/pages/crud.py              universal CRUD sahifa
app/pages/modules.py           8 jadval ta'rifi
app/pages/dashboard.py         bosh sahifa
app/pages/report.py            hisobot + Excel
app/main.py                    asosiy oyna
```
To'liq tushuntirish: [HISOBOT.md](HISOBOT.md)

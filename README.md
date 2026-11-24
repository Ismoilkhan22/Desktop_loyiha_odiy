# Talabalar boshqaruvi (PyQt5 + PostgreSQL)

Desktop dastur: talabalar, o'qituvchilar, fakultetlar, guruhlar, fanlar va baholarni boshqarish,
bosh sahifada hisoblagich va diagrammalar, hisobotni Excelga eksport qilish.

> Topshiriqda MySQL ko'rsatilgan, bu loyihada **PostgreSQL** ishlatilgan. Qolgan hamma narsa topshiriqdagidek.

## Talablar
- Python 3.10+ (3.13 da tekshirilgan)
- PostgreSQL 14+ (16 da tekshirilgan), ishlab turgan bo'lishi kerak

## O'rnatish va ishga tushirish (macOS / Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m app.init_db      # baza + 8 jadval + namuna ma'lumot (qayta ishga tushirsa ham xavfsiz)
python -m app.main         # dasturni ochish
```
Windows: `.venv\Scripts\activate` (qolgani bir xil).

## PostgreSQL sozlamalari
Default: `localhost:5432`, baza `talaba_db`, foydalanuvchi = kompyuter login nomi, parolsiz
(Homebrew PostgreSQL shunday). Boshqacha bo'lsa, muhit o'zgaruvchisi bilan o'zgartiring:
```bash
export DB_USER=postgres DB_PASSWORD=sirparol DB_HOST=localhost DB_PORT=5432 DB_NAME=talaba_db
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

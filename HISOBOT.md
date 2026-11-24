# Hisobot: loyiha qanday qurildi (dars uchun ketma-ketlik)

## 0. Loyiha nima qiladi
`docs/AIFU_02_Desktop_natija.docx` talabiga ko'ra: bosh sahifa (4 hisoblagich + 2 diagramma), talabalar
ro'yxati (qidiruv, guruh filtri, tahrirlash, tasdiqlab o'chirish), 6 ta akademik modul, baholar
(0–100), hisobot + Excelga eksport. Hammasi **PyQt5** (oyna) va **MySQL** (baza).

## 1. Arxitektura (3 qatlam, oddiy)
```
 [ Oyna (PyQt5) ]  ->  [ db.py: query / execute ]  ->  [ MySQL: 8 jadval ]
  app/main.py            SQL yuboradi                    sql/schema.sql
  app/pages/*
```
- **Oyna** faqat ko'rsatadi va tugmalarni eshitadi.
- **db.py** yagona joy: SQL shu yerdan bazaga ketadi, `commit` / `rollback` shu yerda.
- **Baza** qoidalarni ham saqlaydi (ball 0–100, kurs 1–6, bog'liqlik), shuning uchun dasturdagi xato ham bazada ushlanadi.

Eng muhim g'oya: **8 ta jadval uchun 8 ta sahifa yozmadik**. Bitta universal `CrudPage` bor, jadvallar
farqi `modules.py` da qisqa ta'rif sifatida turadi. Yangi jadval = bitta `Module(...)`.

## 2. Ishni boshlash ketma-ketligi (qadamlar)

| # | Qadam | Fayl | Nima uchun |
|---|-------|------|-----------|
| 1 | Muhit: `python3 -m venv .venv`, `pip install -r requirements.txt` | `requirements.txt` | Kutubxonalar loyihaga xos, tizimni buzmaydi |
| 2 | Jadvallar (8 ta) | `sql/schema.sql` | Avval ma'lumot tuzilmasi, keyin dastur |
| 3 | Namuna ma'lumot (3 talaba, 2 o'qituvchi, 2 fakultet, 2 guruh) | `sql/seed.sql` | Dasturni ochganda bo'sh bo'lmasin |
| 4 | Baza sozlamasi | `app/config.py` | Parol/host kodga yozilmaydi, muhitdan olinadi |
| 5 | Ulanish va 2 ta funksiya | `app/db.py` | Qolgan kod faqat `query()` / `execute()` ishlatadi |
| 6 | Bazani yaratuvchi skript | `app/init_db.py` | Bitta buyruq bilan hammasi tayyor |
| 7 | Diagramma vidjeti | `app/widgets.py` | Qo'shimcha kutubxonasiz, ~30 qator |
| 8 | Universal CRUD sahifa | `app/pages/crud.py` | Qo'shish/tahrirlash/o'chirish/qidirish/filtr, hammasi bir joyda |
| 9 | 8 jadval ta'rifi | `app/pages/modules.py` | Har jadval: SELECT, maydonlar, sarlavhalar |
| 10 | Bosh sahifa | `app/pages/dashboard.py` | `COUNT(*)` va diagrammalar |
| 11 | Hisobot + Excel | `app/pages/report.py` | Filtrlangan natijani `.xlsx` ga yozish |
| 12 | Asosiy oyna | `app/main.py` | Chap menyu + sahifalar to'plami |
| 13 | Dizayn (QSS: yon panel, kartalar, jadval, tugmalar) | `app/style.py` | Ko'rinish mantiqdan alohida, bitta faylda |
| 14 | Tekshiruv | `tests/smoke_test.py` | CRUD, qidiruv, cheklovlar, Excel avtomatik tekshiriladi |

## 3. Kod qayerda yozilgan (talabdan koddagi joygacha)

| Talab | Qayerda |
|-------|---------|
| 4 ta hisoblagich `COUNT(*)` | `dashboard.py`, `refresh()` ichida |
| Diagrammalar bazadan yangilanadi | `dashboard.py` `refresh()` + `widgets.py` `BarChart` |
| Chap menyu, 8 jadvalga kirish | `main.py`, `MainWindow.__init__` |
| Ism/familiya bo'yicha qidiruv | `crud.py`, `refresh()` (`LIKE`), `modules.py` `STUDENTS.search` |
| Guruh filtri | `crud.py`, `refresh()`, `modules.py` `STUDENTS.filter_col` |
| Tahrirlash tanlangan ID bo'yicha | `crud.py`, `on_edit()` va `update()` |
| O'chirishdan oldin tasdiq | `crud.py`, `on_delete()` (`QMessageBox.question`) |
| Saqlash → INSERT → COMMIT → jadval yangilanadi | `crud.py` `insert()` → `db.py` `_run()` (`commit`) → `refresh()` |
| ComboBox: ekranda nom, bazada ID | `crud.py`, `FormDialog._make()`, `kind="fk"` |
| 6 akademik modul | `modules.py` |
| Ball 0–100, 100 dan kattasi rad | `modules.py` `GRADES` (`hi=100`) + `schema.sql` `CHECK` |
| Excelga eksport | `report.py`, `save_xlsx()` |
| Bog'liq yozuvni o'chirishda xabar | `crud.py`, `_save()` (MySQL xato kodi 1451) |

## 4. Bitta amal oxirigacha qanday o'tadi (darsda ko'rsatish uchun)
"Yangi talaba qo'shish" tugmasi:
1. `on_add()` → `FormDialog` oynasi ochiladi, guruhlar `SELECT id, name FROM groups` dan to'ldiriladi.
2. "Saqlash" → `values()` qiymatlarni yig'adi (guruh uchun **ID**).
3. `_save(self.insert, ...)` → `insert()` → `INSERT INTO students (...) VALUES (%s, %s, %s)`.
4. `db._run()` → `execute` → **`commit()`** (xato bo'lsa `rollback()`).
5. `refresh()` jadvalni bazadan qayta o'qiydi. Bosh sahifaga o'tganda hisoblagich 3 → 4 bo'ladi.

SQL ga qiymatlar doim `%s` bilan beriladi (matn ichiga qo'shib yozilmaydi), shuning uchun SQL injection yo'q.

## 5. MySQL haqida
- Topshiriqdagi baza: **MySQL**. `brew install mysql` va `brew services start mysql` bilan o'rnatiladi.
- Python bilan ulash: rasmiy `mysql-connector-python` (kompilyatsiya kerak emas).
- Muhim farqlar (darsda aytish mumkin): `groups` MySQL da zahiralangan so'z, shuning uchun jadval `student_groups`;
  matnlarni qo'shish `CONCAT(a, ' ', b)` bilan (`||` MySQL da "YOKI" degani); `LIKE` katta-kichik harfni farqlamaydi.
- Cheklovlarni baza o'zi ushlaydi: `CHECK` (ball 0–100) xato kodi 3819, bog'liq yozuvni o'chirish xato kodi 1451.
- Parol kerak bo'lsa `DB_PASSWORD` o'zgaruvchisi (README da).

## 6. Tekshirilgani va tekshirilmagani
- Tekshirildi: `tests/smoke_test.py` o'tdi (oyna yaratish, barcha sahifalar, qo'shish/tahrirlash/o'chirish, qidiruv, ball > 100 rad, bog'liq yozuv himoyasi, Excel fayl). Bosh sahifa skrinshoti ko'rildi.
- **Tekshirilmadi:** oynani qo'lda bosib chiqish (dialoglarning ko'rinishi), Windows. Dastur jonli ko'rinishda birinchi marta ochilganda bir ko'ring.
- Qisqartirilgan joylar: login/rol yo'q, qidiruv faqat talabalarda, diagramma oddiy ustunli (yangilanish sahifaga o'tganda, jonli emas).

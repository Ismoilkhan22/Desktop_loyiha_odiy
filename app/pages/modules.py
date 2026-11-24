"""6-qadam: 8 ta jadvalning ta'rifi. Yangi jadval qo'shish = bu yerga bitta Module qo'shish."""
from .crud import Field, Module

GROUPS_FK = "SELECT id, name FROM groups ORDER BY name"

STUDENTS = Module(
    "Talabalar", "students",
    "SELECT s.id, s.first_name, s.last_name, g.name FROM students s JOIN groups g ON g.id = s.group_id",
    ["ID", "Ism", "Familiya", "Guruh"],
    [Field("first_name", "Ism"), Field("last_name", "Familiya"), Field("group_id", "Guruh", "fk", GROUPS_FK)],
    search=("s.first_name", "s.last_name"), filter_col="s.group_id", filter_sql=GROUPS_FK,
)

GRADES = Module(
    "Baholar", "grades",
    "SELECT gr.id, st.last_name || ' ' || st.first_name, sub.name, gr.score, gr.graded_at FROM grades gr "
    "JOIN students st ON st.id = gr.student_id JOIN subjects sub ON sub.id = gr.subject_id",
    ["ID", "Talaba", "Fan", "Ball", "Sana"],
    [Field("student_id", "Talaba", "fk", "SELECT id, last_name || ' ' || first_name FROM students ORDER BY 2"),
     Field("subject_id", "Fan", "fk", "SELECT id, name FROM subjects ORDER BY name"),
     Field("score", "Ball (0-100)", "int", lo=0, hi=100),
     Field("graded_at", "Sana", "date")],
)

FACULTIES = Module(
    "Fakultetlar", "faculties", "SELECT id, name FROM faculties", ["ID", "Nomi"], [Field("name", "Nomi")],
)

FACULTY_FK = "SELECT id, name FROM faculties ORDER BY name"

DEPARTMENTS = Module(
    "Kafedralar", "departments",
    "SELECT d.id, f.name, d.name FROM departments d JOIN faculties f ON f.id = d.faculty_id",
    ["ID", "Fakultet", "Nomi"],
    [Field("faculty_id", "Fakultet", "fk", FACULTY_FK), Field("name", "Nomi")],
)

DIRECTIONS = Module(
    "Yo'nalishlar", "directions",
    "SELECT d.id, f.name, d.name FROM directions d JOIN faculties f ON f.id = d.faculty_id",
    ["ID", "Fakultet", "Nomi"],
    [Field("faculty_id", "Fakultet", "fk", FACULTY_FK), Field("name", "Nomi")],
)

GROUPS = Module(
    "Guruhlar", "groups",
    "SELECT g.id, d.name, g.name, g.course FROM groups g JOIN directions d ON d.id = g.direction_id",
    ["ID", "Yo'nalish", "Nomi", "Kurs"],
    [Field("direction_id", "Yo'nalish", "fk", "SELECT id, name FROM directions ORDER BY name"),
     Field("name", "Nomi"), Field("course", "Kurs", "int", lo=1, hi=6)],
)

TEACHERS = Module(
    "O'qituvchilar", "teachers",
    "SELECT t.id, d.name, t.first_name, t.last_name, t.phone FROM teachers t "
    "JOIN departments d ON d.id = t.department_id",
    ["ID", "Kafedra", "Ism", "Familiya", "Telefon"],
    [Field("department_id", "Kafedra", "fk", "SELECT id, name FROM departments ORDER BY name"),
     Field("first_name", "Ism"), Field("last_name", "Familiya"), Field("phone", "Telefon")],
)

SUBJECTS = Module(
    "Fanlar", "subjects",
    "SELECT s.id, t.last_name || ' ' || t.first_name, s.name, s.credit FROM subjects s "
    "JOIN teachers t ON t.id = s.teacher_id",
    ["ID", "O'qituvchi", "Nomi", "Kredit"],
    [Field("teacher_id", "O'qituvchi", "fk", "SELECT id, last_name || ' ' || first_name FROM teachers ORDER BY 2"),
     Field("name", "Nomi"), Field("credit", "Kredit", "int", lo=1, hi=30)],
)

ALL = [STUDENTS, GRADES, FACULTIES, DEPARTMENTS, DIRECTIONS, GROUPS, TEACHERS, SUBJECTS]

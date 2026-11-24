-- Namuna: 2 fakultet, 2 guruh, 2 o'qituvchi, 3 talaba.
INSERT INTO faculties (name) VALUES ('Axborot texnologiyalari'), ('Iqtisodiyot');
INSERT INTO departments (faculty_id, name) VALUES (1, 'Dasturiy injiniring'), (2, 'Buxgalteriya');
INSERT INTO directions (faculty_id, name) VALUES (1, 'Dasturiy injiniring'), (2, 'Iqtisodiyot');
INSERT INTO student_groups (direction_id, name, course) VALUES (1, 'DI-101', 1), (2, 'IQ-201', 2);
INSERT INTO teachers (department_id, first_name, last_name, phone)
    VALUES (1, 'Aziz', 'Karimov', '+998901112233'), (2, 'Dilnoza', 'Rahimova', '+998902223344');
INSERT INTO subjects (teacher_id, name, credit) VALUES (1, 'Python dasturlash', 6), (2, 'Buxgalteriya asoslari', 4);
INSERT INTO students (group_id, first_name, last_name)
    VALUES (1, 'Ali', 'Valiyev'), (1, 'Madina', 'Yusupova'), (2, 'Jasur', 'Toshmatov');
INSERT INTO grades (student_id, subject_id, score, graded_at)
    VALUES (1, 1, 90, '2026-11-01'), (2, 1, 75, '2026-11-01'), (3, 2, 82, '2026-11-02');

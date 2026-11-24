-- 8 ta jadval. Ota jadvallar birinchi yaratiladi.
CREATE TABLE IF NOT EXISTS faculties (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS departments (
    id         SERIAL PRIMARY KEY,
    faculty_id INT  NOT NULL REFERENCES faculties(id),
    name       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS directions (
    id         SERIAL PRIMARY KEY,
    faculty_id INT  NOT NULL REFERENCES faculties(id),
    name       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS groups (
    id           SERIAL PRIMARY KEY,
    direction_id INT  NOT NULL REFERENCES directions(id),
    name         TEXT NOT NULL,
    course       INT  NOT NULL CHECK (course BETWEEN 1 AND 6)
);

CREATE TABLE IF NOT EXISTS teachers (
    id            SERIAL PRIMARY KEY,
    department_id INT  NOT NULL REFERENCES departments(id),
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    phone         TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS subjects (
    id         SERIAL PRIMARY KEY,
    teacher_id INT  NOT NULL REFERENCES teachers(id),
    name       TEXT NOT NULL,
    credit     INT  NOT NULL CHECK (credit > 0)
);

CREATE TABLE IF NOT EXISTS students (
    id         SERIAL PRIMARY KEY,
    group_id   INT  NOT NULL REFERENCES groups(id),
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL
);

-- Talaba o'chirilsa, uning baholari ham o'chadi (CASCADE).
CREATE TABLE IF NOT EXISTS grades (
    id         SERIAL PRIMARY KEY,
    student_id INT  NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    subject_id INT  NOT NULL REFERENCES subjects(id),
    score      INT  NOT NULL CHECK (score BETWEEN 0 AND 100),
    graded_at  DATE NOT NULL DEFAULT CURRENT_DATE
);

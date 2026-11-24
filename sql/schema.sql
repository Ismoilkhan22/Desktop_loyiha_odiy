-- 8 ta jadval. Ota jadvallar birinchi yaratiladi.
CREATE TABLE IF NOT EXISTS faculties (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS departments (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT NOT NULL,
    name       VARCHAR(150) NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculties(id)
);

CREATE TABLE IF NOT EXISTS directions (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT NOT NULL,
    name       VARCHAR(150) NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculties(id)
);

-- "groups" MySQL da zahiralangan so'z, shuning uchun student_groups
CREATE TABLE IF NOT EXISTS student_groups (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    direction_id INT NOT NULL,
    name         VARCHAR(50) NOT NULL,
    course       INT NOT NULL CHECK (course BETWEEN 1 AND 6),
    FOREIGN KEY (direction_id) REFERENCES directions(id)
);

CREATE TABLE IF NOT EXISTS teachers (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT NOT NULL,
    first_name    VARCHAR(100) NOT NULL,
    last_name     VARCHAR(100) NOT NULL,
    phone         VARCHAR(30)  NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS subjects (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    name       VARCHAR(150) NOT NULL,
    credit     INT NOT NULL CHECK (credit > 0),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS students (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    group_id   INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    FOREIGN KEY (group_id) REFERENCES student_groups(id)
);

-- Talaba o'chirilsa, uning baholari ham o'chadi (CASCADE).
CREATE TABLE IF NOT EXISTS grades (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    score      INT NOT NULL CHECK (score BETWEEN 0 AND 100),
    graded_at  DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

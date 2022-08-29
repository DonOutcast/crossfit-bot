import sqlite3 as sq


class Database:
    """For database"""
    def __init__(self, name: str) -> None:
        self.name = name
        self.base = sq.connect(f"{self.name}")
        self.cur = self.base.cursor()
        self.create_table_exercises()
        self.create_table_complex()
        self.create_table_training()

    def create_table_exercises(self):
        if self.base:
            print("Data base: tables  connected OK!")
            query = """CREATE TABLE IF NOT EXISTS 
                        exercises (  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     complex_id INTEGER,
                                     name VARCHAR(40) NOT NULL,
                                     reps INTEGER DEFAULT 1,
                                     again TEXT,
                                     temp VARCHAR(20), /*амрап емом*/
                                     type VARCHAR(20), /*пишем метры или кг*/
                                     female INTEGER,
                                     male INTEGER,
                                     relax_time INTEGER,
                                     work_time INTEGER,
                                     FOREIGN KEY(complex_id) REFERENCES complex(id)
                                     )"""
            self.cur.execute(query)
            self.base.commit()

    def create_table_complex(self):
        if self.base:
            print("Data base: table complex connected OK!")
            query = """CREATE TABLE IF NOT EXISTS 
                        complex (id INTEGER PRIMARY KEY AUTOINCREMENT,      
                                 complex_name VARCHAR(20) NOT NULL,
                                 training_id INTEGER,
                                 repeat INTEGER,
                                 FOREIGN KEY(training_id) REFERENCES training(id)
                                 )"""
            self.cur.execute(query)
            self.base.commit()

    def create_table_training(self):
        if self.base:
            print("Data base: table training connected OK!")
            query = """CREATE TABLE IF NOT EXISTS 
                        training (  id INTEGER PRIMARY KEY AUTOINCREMENT,    
                                    name VARCHAR(20) NOT NULL,
                                    lvl_training VARCHAR(20)
                                    )"""
            self.cur.execute(query)
            self.base.commit()

    def insert_into_training(self, data: tuple):
        if self.base:
            query = """INSERT INTO training (name, lvl_training) 
                        VALUES (?, ?)"""
            print(data)
            self.cur.execute(query, data)
            self.base.commit()

    def insert_into_complex(self, data: tuple):
        if self.base:
            query = """INSERT INTO complex (complex_name, training_id, repeat)
                        VALUES (?, ?, ?)"""
            self.cur.execute(query, data)
            self.base.commit()

    def insert_into_exercises(self, data: tuple):
        if self.base:
            query = """INSERT INTO exercises (complex_id, name, reps, again, temp, type, female, male, relax_time, work_time)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            self.cur.execute(query, data)
            self.base.commit()


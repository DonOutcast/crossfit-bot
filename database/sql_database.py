import sqlite3 as sq


class Database:
    """For database"""
    def __init__(self, name: str) -> None:
        self.name = name
        self.base = sq.connect(f"{self.name}")
        self.cur = self.base.cursor()

    def create_table_exercises(self):
        if self.base:
            print("Data base: tables  connected OK!")
            query = """CREATE TABLE IF NOT EXISTS 
                        exercises (  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     complex_id INTEGER,     
                                     name VARCHAR(40) NOT NULL,
                                     reps INTEGER DEFAULT 1,
                                     type VARCHAR(20), /*пишем метры или кг*/
                                     female INTEGER,
                                     male INTEGER,
                                     FOREIGN KEY(complex_id) REFERENCES complex(id)
                                     )"""
            self.cur.execute(query)
            self.base.commit()

    def create_table_complex(self):
        if self.base:
            print("Data base: tables complex connected OK!")
            query = """CREATE TABLE IF NOT EXISTS 
                        complex (id INTEGER PRIMARY KEY AUTOINCREMENT,      
                                 name VARCHAR(20) NOT NULL,
                                 training_id INTEGER,
                                 type VARCHAR(20),
                                 work_time INTEGER,
                                 relax_time INTEGER,
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
                                    rounds INTEGER,
                                    type VARCHAR(20)
                                    )"""
            self.cur.execute(query)
            self.base.commit()

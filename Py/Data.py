import pymysql
import pickle

class Data:
    conn = pymysql.connect('localhost','Danil','$password','Tabl')
    cur = conn.cursor()

    def Table(self, table: str):
        with self.conn:
            result = [[] for i in range(2)]
            self.cur.execute("SELECT * FROM " + table)
            rows = self.cur.fetchall()
            for row in rows:
                result[0].append(row)
            self.cur.execute("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME=%s", table)
            rows2 = self.cur.fetchall()
            for row in rows2:
                result[1].append(str(row[3]))
            result = pickle.dumps(result)
            return result

    def updateTable(self, data):
        with self.conn:
            try:
                str = ", "
                str = str.join(data[-1])
                print(str)
                self.cur.execute('DELETE FROM ' + data[-2])
                self.conn.commit()
                for item in data[:-2]:
                    print(data[-2])
                    self.cur.execute("INSERT INTO " + data[-2] + " (" + str + ") VALUES (%s, %s, %s)",[item[0], item[1], item[2]])
                    self.conn.commit()
            except (self.conn.DatabaseError) as e:
                print(e)
                return None

    def TableList(self):
        with self.conn:
            try:
                result = []
                self.cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='mainChema' ")
                row = [item[0] for item in self.cur.fetchall()]
                return row
            except:
                print("Ошибка достать имя таблицы")

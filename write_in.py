import xlrd
import pymysql as sql

df = xlrd.open_workbook("QRcode.xlsx")
table = df.sheets()[0]

base = sql.connect(host="localhost", user="root", password="*IK<.lo9sql")
cur = base.cursor()
cur.execute("use students;")

query = "insert into stu_info values ({subject},{bar});"

for subject, bar in zip(table.col_values(7)[1:], table.col_values(16)[1:]):
    print(subject, bar)
    cur.execute(query.format(subject=int(subject), bar=int(bar)))
    base.commit()  # 不commit等于白做！！！

cur.execute("select * from stu_info;")
print(cur.fetchall())
cur.close()
base.close()
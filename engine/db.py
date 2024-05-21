import sqlite3

con = sqlite3.connect("小页.db")
cursor = con.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)
#注意:此处的"C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"执行路径必须正确，保证此路径可以打开word
#query = "INSERT INTO sys_command VALUES (null,'word', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE')"
#cursor.execute(query)
#con.commit()

#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO web_command VALUES (null,'有道词典', 'https://dict.youdao.com/')"
#cursor.execute(query)
#con.commit()

app_name="word"
cursor.execute('SELECT path FROM sys_command WHERE name IN(?)',(app_name,))
results=cursor.fetchall()
print(results[0][0])
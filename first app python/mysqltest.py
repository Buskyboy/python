import mysql.connector

class Show:
    def __init__(self, title, discription, total_seats):
        self.title = title
        self.discription = discription
        self.total_seats = total_seats

    def save_to_db(self, db_cursor):
        sql = "INSERT INTO shows (title, discription, total_seats) VALUES (%s, %s, %s)"
        val = (self.title, self.discription, self.total_seats)
        db_cursor.execute(sql, val)    

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CocoPop123" ,
    database="test_db"
)
    
print("Connected to MySQL database!")
    
db_cursor = db.cursor()
db_cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")
db_cursor.execute("USE test_db")

db_cursor.execute   ("CREATE TABLE IF NOT EXISTS shows (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), discription VARCHAR(255) ,total_seats INT)") 

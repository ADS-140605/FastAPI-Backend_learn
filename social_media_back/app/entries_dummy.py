from database import connect
import time
cursor = connect()
entries = []
for i in entries:
    cursor.execute(
        """
        INSERT INTO posts(
            title,
            content,
            published,
            rating
        )
        VALUES(%s,%s,%s,%s)
        """,
        i
    )
    cursor.connection.commit()
    print("Inserted:", i[0])
    time.sleep(2)
from database import connect
import time
cursor = connect()
entries = [
    (
        "Getting Started with Python",
        "Day 1",
        True,
        4.5
    ),

    (
        "FastAPI CRUD Operations",
        "Learning GET POST PUT DELETE",
        False,
        3.8
    ),

    (
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
        True,
        5.0
    ),

    (
        "@@@###$$$%%%^^^",
        "!<>?:{}|~`",
        False,
        2.5
    ),

    (
        "नमस्ते 🚀 Python",
        "Testing unicode characters 測試 テスト",
        True,
        4.7
    ),

    (
        "No Rating Post",
        "This post has no rating",
        True,
        0
    ),

    (
        "Minimum Rating",
        "Lowest possible rating",
        False,
        0
    ),

    (
        "Maximum Rating",
        "Highest possible rating",
        True,
        5
    ),

    (
        "Integer Rating",
        "Rating as integer",
        True,
        4
    ),

    (
        "Published False",
        "Testing false value",
        False,
        1.2
    ),

    (
        "'; DROP TABLE posts; --",
        "SQL Injection payload",
        False,
        1.0
    ),

    (
        "<script>alert('XSS')</script>",
        "<h1>Injected HTML</h1>",
        True,
        2.2
    ),

    (
        "Duplicate Post",
        "Same content",
        True,
        4.0
    ),

    (
        "Duplicate Post",
        "Same content",
        True,
        4.0
    ),

    (
        "Big Numbers",
        "1000000000000000000",
        True,
        4.9
    ),

    (
        "Heloooooooooooooooooooooooo",
        "Day 1",
        True,
        0
    )
]
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
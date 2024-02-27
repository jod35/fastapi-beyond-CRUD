import random

books = [
    {
        "id": 1,
        "title": "Python Cookbook",
        "author": "<NAME>",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2021-01-01",
        "page_count": 100,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Django By Example",
        "author": "<NAME>",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-01-19",
        "page_count": 100,
        "language": "English",
    },
    {
        "id": 3,
        "title": "The webocket handbook",
        "author": "<NAME>",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2021-01-01",
        "page_count": 100,
        "language": "English",
    },
    {
        "id": 4,
        "title": "Headfirst Javascript",
        "author": "<NAME>",
        "publisher": "Oreilly Ltd",
        "published_date": "2021-01-01",
        "page_count": 100,
        "language": "English",
    },
    {
        "id": 5,
        "title": "Python Cookbook",
        "author": "<NAME>", 
        "publisher": "Packt Publishing Ltd",
        "published_date": "2021-01-01",
        "page_count": 100,
        "language": "English",
    },
    {
        "id": 6,
        "title": "Python Cookbook",
        "author": "<NAME>",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2021-01-01",
        "page_count": 100,
        "language": "English",
    }
]



for book in books:
    book['page_count']= random.randint(200, 10000)

print(books)


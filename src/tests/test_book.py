from src.books.schemas import BookCreateModel

books_prefix = f"/api/v1/books"


def test_get_all_books(test_client,fake_book_service,fake_session):
    response = test_client.get(
        url=f"{books_prefix}"
    )

    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)


def test_create_book(test_client, fake_book_service, fake_session):
    book_data = {
        "title":"Test Title",
        "author" : "Test Author",
        "publisher": "Test Publications",
        "published_date":"2024-12-10",
        "language": "English",
        "page_count": 215
    }
    response = test_client.post(
        url=f"{books_prefix}",
        json=book_data
    )
    
    book_create_data = BookCreateModel(**book_data)
    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(book_create_data, fake_session)


def test_get_book_by_uid(test_client, fake_book_service,test_book, fake_session):
    response = test_client.get(f"{books_prefix}/{test_book.uid}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.uid,fake_session)


def test_update_book_by_uid(test_client, fake_book_service,test_book, fake_session):
    response = test_client.put(f"{books_prefix}/{test_book.uid}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.uid,fake_session)


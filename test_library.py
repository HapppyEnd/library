import unittest
from unittest.mock import mock_open, patch
from pathlib import Path
import json
from main import Book, Library


class TestBook(unittest.TestCase):
    def test_book_creation(self):
        book = Book("Test Title", "Test Author", 2021, "available")
        self.assertEqual(book.title, "Test Title")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year, 2021)
        self.assertEqual(book.status, "available")

    def test_to_dict(self):
        book = Book("Test Title", "Test Author", 2021, "available")
        book_dict = book.to_dict()
        self.assertIn("id", book_dict)
        self.assertEqual(book_dict["title"], "Test Title")


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.test_file = Path("test_library.json")
        with open(self.test_file, 'w') as f:
            json.dump([{"title": "Test Title", "author": "Test Author",
                        "year": 2021, "status": "available"}], f)

        self.library = Library(self.test_file)

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()

    def test_load_books(self):
        self.library.load_books()
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Title")
        self.assertEqual(self.library.books[0].author, "Test Author")
        self.assertEqual(self.library.books[0].year, 2021)
        self.assertEqual(self.library.books[0].status, "available")

    def test_save_books(self):
        self.library.books = [
            Book("Test Title 2", "Test Author 2", 2022, "available")]
        self.library.save_books()
        with open(self.test_file, 'r') as f:
            content = json.load(f)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]["title"], "Test Title 2")
        self.assertEqual(content[0]["author"], "Test Author 2")
        self.assertEqual(content[0]["year"], 2022)
        self.assertEqual(content[0]["status"], "available")

    def test_add_book(self):
        self.library.add_book("Test Title", "Test Author", 2021)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Title")

    def test_delete_book(self):
        self.library.add_book("Test Title", "Test Author", 2021)
        book_id = self.library.books[0].id

        with patch('builtins.input', return_value=book_id):
            self.library.delete_book()

        self.assertEqual(len(self.library.books), 0)

    def test_find_by_title(self):
        self.library.add_book("Test Title", "Test Author", 2021)
        results = self.library.find_by_title("Test Title")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Test Title")


if __name__ == '__main__':
    unittest.main()

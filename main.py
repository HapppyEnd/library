import json
import uuid
from datetime import datetime
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("library.log", encoding='utf-8'),
                    ])


class Book:
    """Class for representing a book in the library."""

    def __init__(self, book_id: str, title: str, author: str, year: int,
                 status: str) -> None:
        """Initialize a book.

        Args:
            book_id (str): Unique identifier for the book.
            title (str): Title of the book.
            author (str): Author of the book.
            year (int): Year of publication.
            status (str): Status of the book (e.g., 'available', 'checked out').
        """
        self.id: str = book_id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> Dict[str, Any]:
        """Convert the book to a dictionary for serialization.

        Returns:
            dict: Dictionary containing book data.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Book':
        """Create a book from a dictionary.

        Args:
            data (dict): Dictionary containing book data.

        Returns:
            Book: An instance of the book.
        """
        return Book(data['id'], data['title'], data['author'], data['year'],
                    data['status'])


class Library:
    """Class for managing the library."""

    def __init__(self, filename: Path) -> None:
        """Initialize the library.

        Args:
            filename (Path): Path to the file for storing book data.
        """
        self.books: List[Book] = []
        self.filename: Path = filename
        self.load_books()

    def load_books(self) -> None:
        """Load books from a file."""
        if self.filename.exists():
            try:
                with self.filename.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(book) for book in data]
                logging.info(f'Books loaded from file {self.filename}.')
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logging.error(f'Error loading books: {e}')

    def save_books(self) -> None:
        """Save books to a file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump([book.to_dict() for book in self.books], file,
                          indent=4, ensure_ascii=False)
            logging.info(f'Books saved to file {self.filename}.')
        except IOError as e:
            logging.error(f'Error saving books: {e}')

    def add_book(self, title: str, author: str, year: int) -> None:
        """Add a new book to the library.

        Args:
            title (str): Title of the book.
            author (str): Author of the book.
            year (int): Year of publication.
        """
        book_id: str = str(uuid.uuid4())
        new_book: Book = Book(book_id, title, author, year, status='в наличии')
        self.books.append(new_book)
        self.save_books()
        logging.info(f'Book "{title}" added with ID {book_id}.')
        print(f'Книга "{title}" добавлена с ID {book_id}.')

    def delete_book(self) -> None:
        """Delete a book from the library by ID."""
        while True:
            book_id = get_non_empty_input(
                'Введите ID книги для удаления '
                '(или введите "выход" для возврата в главное меню): ')
            if book_id.lower() == 'выход':
                return
            book: Optional[Book] = next(
                (book for book in self.books if book.id == book_id), None)
            if book:
                self.books.remove(book)
                self.save_books()
                logging.info(f'Book with ID {book_id} deleted.')
                print(f'Книга с ID {book_id} удалена.')
                return
            else:
                print(f'Книга с ID {book_id} не найдена. Попробуйте снова.')

    def find_by_title(self, title: str) -> List[Book]:
        """Search for books by title.

        Args:
            title (str): Title of the book to search for.

        Returns:
            list[Book]: List of books matching the given title.
        """
        return [book for book in self.books if
                title.lower() in book.title.lower()]

    def find_by_author(self, author: str) -> List[Book]:
        """Search for books by author.

        Args:
            author (str): Author of the book to search for.

        Returns:
            list[Book]: List of books matching the given author.
        """
        return [book for book in self.books if
                author.lower() in book.author.lower()]

    def find_by_year(self, year: int) -> List[Book]:
        """Search for books by publication year.

        Args:
            year (int): Publication year of the book to search for.

        Returns:
            list[Book]: List of books matching the given year.
        """
        return [book for book in self.books if book.year == year]

    def show_books(self) -> None:
        """Display all books in the library."""
        if not self.books:
            logging.info('No books in the library.')
            print('В библиотеке нет книг.')
        else:
            for book in self.books:
                print(f'ID: {book.id}, Title: {book.title}, '
                      f'Author: {book.author}, Year: {book.year}, '
                      f'Status: {book.status}')

    def change_status(self, book_id: str, new_status: str) -> None:
        """Change the status of a book.

        Args:
            book_id (str): ID of the book whose status needs to be changed.
            new_status (str): New status of the book (available/checked out).
        """
        new_status = new_status.lower()
        book: Optional[Book] = next(
            (book for book in self.books if book.id == book_id), None)

        if new_status not in ['в наличии', 'выдана']:
            logging.warning(
                'Invalid status. Available statuses: available/checked out.')
            print('Некорректный статус. Доступные статусы: в наличии/выдана.')
            return

        if book is None:
            logging.warning(f'Book with ID {book_id} not found.')
            print(f'Книга с ID {book_id} не найдена.')
            return

        book.status = new_status
        self.save_books()
        logging.info(
            f'Status of book with ID {book_id} changed to "{new_status}".')
        print(f'Статус книги с ID {book_id} изменён на "{new_status}".')


def change_book_status(library: Library) -> None:
    """Change the status of a book by ID."""
    while True:
        book_id = get_non_empty_input(
            'Введите ID книги для изменения статуса '
            '(или введите "выход" для возврата в главное меню): ')
        if book_id.lower() == 'выход':
            return
        book: Optional[Book] = next(
            (book for book in library.books if book.id == book_id), None)
        if book is None:
            print(f'Книга с ID {book_id} не найдена.')
        else:
            while True:
                new_status = get_non_empty_input(
                    'Введите новый статус (в наличии/выдана): ')
                if new_status.lower() in ['в наличии', 'выдана']:
                    library.change_status(book_id, new_status)
                    return
                else:
                    print('Пожалуйста, введите в наличии/выдана')


def get_non_empty_input(prompt: str) -> str:
    """Get non-empty input from the user.

    Args:
        prompt (str): Message to prompt for input.

    Returns:
        str: Non-empty string entered by the user.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print('Ввод не может быть пустым. Пожалуйста, попробуйте снова.')


def get_year_input() -> int:
    """Get valid publication year input from the user.

    Returns:
        int: Valid publication year.
    """
    while True:
        year = input('Введите год издания книги: ')
        try:
            year = int(year)
            if year <= 0:
                raise ValueError('Year must be positive.')
            if year > datetime.now().year:
                raise ValueError(
                    'Year cannot be greater than the current year.')
            return year

        except ValueError as e:
            logging.warning(f'Invalid year input: {e}')
            print('Некорректный ввод. Пожалуйста, введите корректный год.')


def search_books(library: Library, search_type: str, query: str) -> List[Book]:
    """Search for books in the library by given criteria.

    Args:
        library (Library): Library instance to search for books.
        search_type (str): Type of search ('title', 'author', 'year').
        query (str): Query for the search.

    Returns:
        list[Book]: List of books matching the search criteria.
    """
    if search_type == 'title':
        return library.find_by_title(query)
    elif search_type == 'author':
        return library.find_by_author(query)
    elif search_type == 'year':
        return library.find_by_year(int(query))
    return []


def handle_add_book(library: Library) -> None:
    """Handle adding a new book.

    Args:
        library (Library): Library instance to add a book.
    """
    title = get_non_empty_input('Введите название книги: ')
    author = get_non_empty_input('Введите автора книги: ')
    year = get_year_input()
    library.add_book(title, author, year)


def handle_delete_book(library: Library) -> None:
    """Handle deleting a book.

    Args:
        library (Library): Library instance to delete a book.
    """
    library.delete_book()


def handle_search_books(library: Library) -> None:
    """Handle searching for books.

    Args:
        library (Library): Library instance to search for books.
    """
    while True:
        search_choice = get_non_empty_input(
            'Выберите критерий поиска:\n1. Поиск по названию\n2. '
            'Поиск по автору\n3. Поиск по году\nВведите номер критерия: ')

        if search_choice == '1':
            query = get_non_empty_input('Введите название книги для поиска: ')
            results = search_books(library, 'title', query)
            break
        elif search_choice == '2':
            query = get_non_empty_input('Введите автора для поиска: ')
            results = search_books(library, 'author', query)
            break
        elif search_choice == '3':
            year = get_year_input()
            results = search_books(library, 'year', str(year))
            break
        else:
            print('Недопустимый выбор. Пожалуйста, попробуйте снова.')

    if results:
        for book in results:
            print(f'ID: {book.id}, Название: {book.title}, '
                  f'Автор: {book.author}, Год: {book.year}, '
                  f'Статус: {book.status}')
    else:
        print('Книги не найдены.')


def main() -> None:
    """Main function to run the program."""
    library = Library(Path('library.json'))
    while True:
        print('Команды: ')
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Поиск книги')
        print('4. Отобразить все книги')
        print('5. Изменить статус книги')
        print('6. Выход')

        choice = input('Выберите команду: ')
        if choice == '1':
            handle_add_book(library)
        elif choice == '2':
            handle_delete_book(library)
        elif choice == '3':
            handle_search_books(library)
        elif choice == '4':
            library.show_books()
        elif choice == '5':
            change_book_status(library)
        elif choice == '6':
            logging.info('Выход из программы.')
            print('До свидания!')
            break
        else:
            print('Некорректный выбор. Пожалуйста, попробуйте снова.')


if __name__ == '__main__':
    main()

import json
import os
import uuid


class Book:
    """
    Represents a book in the library.

    Attributes:
        id (str): Unique identifier for the book.
        title (str): Title of the book.
        author (str): Author of the book.
        year (int): Year of publication.
        status (str): Availability status of the book.
    """

    def __init__(self, book_id: str, title: str, author: str, year: int,
                 status: str):
        self.id: str = book_id if book_id is not None else str(uuid.uuid4())
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> dict:
        """
        Convert the Book instance to a dictionary.

        :return: Dictionary representation of the book.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @staticmethod
    def from_dict(data: dict) -> 'Book':
        """
        Create a Book instance from a dictionary.

        :param data: Dictionary containing book information.
        :return: A Book instance.
        """
        return Book(data['id'], data['title'], data['author'], data['year'],
                    data['status'])


class Library:
    """
    Represents a library that contains a collection of books.

    Attributes:
        books (list[Book]): List of books in the library.
        filename (str): The filename for saving and loading books.
    """

    def __init__(self, filename: str):
        self.books: list[Book] = []
        self.filename: str = filename
        self.load_book()

    def load_book(self):
        """
        Load books from the JSON file.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.books = [Book.from_dict(book) for book in data]

    def save_book(self):
        """
        Save the current list of books to the JSON file.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4,
                      ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int):
        """
        Add a new book to the library.

        :param title: Title of the book.
        :param author: Author of the book.
        :param year: Year of publication.
        """
        book_id: str = str(uuid.uuid4())
        new_book: Book = Book(book_id, title, author, year, status='в наличии')
        self.books.append(new_book)
        self.save_book()
        print(f'Книга "{title}" добавлена с ID {book_id}.')

    def delete_book(self, book_id: str):
        """
        Delete a book from the library.

        :param book_id: Unique identifier of the book to be deleted.
        """
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_book()
                print(f'Книга с ID {book_id} удалена.')
                return
        print(f'Книга с ID {book_id} не найдена.')

    def find_by_title(self, title: str) -> list[Book]:
        """
        Find books by title.

        :param title: Title to search for.
        :return: List of books matching the title.
        """
        results: list[Book] = [book for book in self.books if
                               title.lower() in book.title.lower()]
        return results

    def find_by_author(self, author: str) -> list[Book]:
        """
        Find books by author.

        :param author: Author to search for.
        :return: List of books matching the author.
        """
        results: list[Book] = [book for book in self.books if
                               author.lower() in book.author.lower()]
        return results

    def find_by_year(self, year: int) -> list[Book]:
        """
        Find books by publication year.

        :param year: Year to search for.
        :return: List of books published in the specified year.
        """
        results: list[Book] = [book for book in self.books if
                               book.year == year]
        return results

    def show_books(self):
        """
        Display all books in the library.
        """
        if not self.books:
            print('В библиотеке нет книг.')
        else:
            for book in self.books:
                print(f'ID: {book.id}, Название: {book.title}, '
                      f'Автор: {book.author}, Год: {book.year}, '
                      f'Статус: {book.status}')

    def change_status(self, book_id: str, new_status: str):
        """
        Change the status of a book.

        :param book_id: Unique identifier of the book.
        :param new_status: New status to set for the book.
        """
        book: Book = next((book for book in self.books if book.id == book_id),
                          None)
        if new_status not in ['в наличии', 'выдана']:
            print(
                'Некорректный статус. Доступные статусы: "в наличии", "выдана".')
            return

        if book is None:
            print(f'Книга с ID {book_id} не найдена.')
            return

        book.status = new_status
        self.save_book()
        print(f'Статус книги с ID {book_id} изменён на "{new_status}".')


def get_search_choice() -> str:
    """
    Get the user's choice for search criteria.

    :return: The selected search criteria.
    """
    while True:
        print('Выберите критерий поиска:')
        print('1. Поиск по названию')
        print('2. Поиск по автору')
        print('3. Поиск по году')
        search_choice: str = input('Введите номер критерия: ').strip()
        if search_choice in ['1', '2', '3']:
            return search_choice
        print('Некорректный выбор критерия.')


def get_year_input() -> int:
    """
    Get the year of publication from user input.

    :return: The year entered by the user.
    """
    while True:
        try:
            year: int = int(input('Введите год издания книги: '))
            return year
        except ValueError:
            print('Некорректный ввод. Пожалуйста, введите корректный год.')


def main():
    """
    Main function to run the library management system.
    """
    library: Library = Library('library.json')
    while True:
        print('Команды: ')
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Поиск книги')
        print('4. Отобразить все книги')
        print('5. Изменить статус книги')
        print('6. Выход')

        choice: str = input('Выберите команду: ')

        if choice == '1':
            title: str = input('Введите название книги: ')
            author: str = input('Введите автора книги: ')
            year: int = get_year_input()
            library.add_book(title, author, year)

        elif choice == '2':
            book_id: str = input('Введите ID книги для удаления: ')
            library.delete_book(book_id)

        elif choice == '3':
            search_choice: str = get_search_choice()
            query: str = input('Введите значение для поиска: ').strip()

            if not query:
                print('Ошибка: Ввод не может быть пустым.')
                continue

            results: list[Book] = []
            if search_choice == '1':
                results = library.find_by_title(query)
            elif search_choice == '2':
                results = library.find_by_author(query)
            elif search_choice == '3':
                try:
                    year: int = int(query)
                    results = library.find_by_year(year)
                except ValueError:
                    print(
                        'Некорректный ввод года. Пожалуйста, введите числовое значение.')
                    continue

            if results:
                for book in results:
                    print(f'ID: {book.id}, Название: {book.title}, '
                          f'Автор: {book.author}, Год: {book.year}, '
                          f'Статус: {book.status}')
            else:
                print('Книги не найдены.')

        elif choice == '4':
            library.show_books()

        elif choice == '5':
            book_id: str = input('Введите ID книги для изменения статуса: ')
            book: Book = next(
                (book for book in library.books if book.id == book_id), None)

            if book is None:
                print(f'Книга с ID {book_id} не найдена.')
            else:
                new_status: str = input(
                    'Введите новый статус (в наличии/выдана): ')
                library.change_status(book_id, new_status)

        elif choice == '6':
            print('Выход из программы.')
            break

        else:
            print('Некорректный выбор. Пожалуйста, попробуйте снова.')


if __name__ == '__main__':
    main()

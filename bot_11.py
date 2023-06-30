import datetime


class Field:
    def __init__(self, value=None):
        self._value = value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return repr(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self._validate_phone_number()

    def _validate_phone_number(self):
        if self._value is not None and not self._value.isdigit():
            raise ValueError("Phone number must contain only digits.")


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self._validate_birthday()

    def _validate_birthday(self):
        if self._value is not None:
            try:
                datetime.datetime.strptime(self._value, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    "Invalid birthday format. Please use the format YYYY-MM-DD."
                )

    def days_to_birthday(self):
        if self._value is None:
            return None
        today = datetime.date.today()
        birthday = (
            datetime.datetime.strptime(self._value, "%Y-%m-%d")
            .date()
            .replace(year=today.year)
        )
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        return (birthday - today).days


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"{self.name.value}: {self.phone.value}"

    def __repr__(self):
        return f"Record({repr(self.name)}, {repr(self.phone)}, {repr(self.birthday)})"

    def days_to_birthday(self):
        return self.birthday.days_to_birthday()


class AddressBook:
    def __init__(self):
        self.data = {}

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        del self.data[name]

    def search_records(self, keyword):
        results = []
        for record in self.data.values():
            if keyword in record.name.value or (
                record.phone.value and keyword in record.phone.value
            ):
                results.append(record)
        return results

    def iterator(self, page_size):
        keys = list(self.data.keys())
        total_records = len(keys)
        num_pages = total_records // page_size + (total_records % page_size > 0)

        for i in range(num_pages):
            start_idx = i * page_size
            end_idx = start_idx + page_size
            yield [self.data[key] for key in keys[start_idx:end_idx]]


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдений."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Неправильна команда."

    return wrapper


@input_error
def handle_hello():
    return "How can I help you?"


@input_error
def handle_add_contact(name, number, birthday=None):
    contact = Record(name, number, birthday)
    address_book.add_record(contact)
    return "Контакт успішно доданий!"


@input_error
def handle_change_number(name, number):
    contact = address_book.data[name]
    contact.phone.value = number
    return "Номер телефону змінено!"


@input_error
def handle_show_number(name):
    contact = address_book.data[name]
    return contact.phone.value


@input_error
def handle_show_all():
    if not address_book.data:
        return "Список контактів порожній."
    else:
        result = "Список контактів:\n"
        for record in address_book.data.values():
            result += f"{record}\n"
        return result


@input_error
def handle_search(keyword):
    results = address_book.search_records(keyword)
    if not results:
        return "Збігів не знайдено."
    else:
        result = "Результати пошуку:\n"
        for record in results:
            result += f"{record}\n"
        return result


@input_error
def handle_days_to_birthday(name):
    contact = address_book.data[name]
    days = contact.days_to_birthday()
    if days is None:
        return "Дата народження не вказана."
    elif days == 0:
        return "Сьогодні день народження!"
    elif days > 0:
        return f"До дня народження залишилося {days} днів."
    else:
        return f"День народження вже минув {abs(days)} днів тому."


def main():
    while True:
        command = input("Введіть команду: ").lower()

        if command == "hello":
            print(handle_hello())
        elif command.startswith("add"):
            _, name, number, *birthday = command.split(" ")
            print(handle_add_contact(name, number, *birthday))
        elif command.startswith("change"):
            _, name, number = command.split(" ")
            print(handle_change_number(name, number))
        elif command.startswith("phone"):
            _, name = command.split(" ")
            print(handle_show_number(name))
        elif command == "show all":
            print(handle_show_all())
        elif command.startswith("search"):
            _, keyword = command.split(" ")
            print(handle_search(keyword))
        elif command.startswith("days to birthday"):
            _, name = command.split(" ")
            print(handle_days_to_birthday(name))
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    address_book = AddressBook()
    main()

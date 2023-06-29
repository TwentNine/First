class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_record(self, record):
        self.contacts[record.name.value] = record

    def search_by_name(self, name):
        if name in self.contacts:
            return self.contacts[name]
        else:
            raise KeyError("Контакт не знайдений.")

    def show_all_records(self):
        if not self.contacts:
            return "Список контактів порожній."
        else:
            result = "Список контактів:\n"
            for name, record in self.contacts.items():
                result += f"{name}: {record}\n"
            return result


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise KeyError("Номер телефону не знайдений.")

    def __str__(self):
        result = f"Name: {self.name.value}\n"
        if self.phones:
            result += "Phones:\n"
            for phone in self.phones:
                result += f"- {phone}\n"
        return result


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


def handle_hello():
    return "How can I help you?"


def handle_add_contact(name, number):
    record = Record(name)
    record.add_phone(Phone(number))
    address_book.add_record(record)
    return "Контакт успішно доданий!"


def handle_change_number(name, number):
    record = address_book.search_by_name(name)
    record.remove_phone(record.phones[0])  # Remove the first phone number
    record.add_phone(Phone(number))
    return "Номер телефону змінено!"


def handle_show_number(name):
    record = address_book.search_by_name(name)
    if record.phones:
        return f"Name: {record.name.value}\nPhone: {record.phones[0].value}"
    else:
        return "Номер телефону не знайдений."


def handle_show_all():
    return address_book.show_all_records()


def main():
    while True:
        command = input("Введіть команду: ").lower()

        if command == "hello":
            print(handle_hello())
        elif command.startswith("add"):
            _, name, number = command.split(" ")
            print(handle_add_contact(name, number))
        elif command.startswith("change"):
            _, name, number = command.split(" ")
            print(handle_change_number(name, number))
        elif command.startswith("phone"):
            _, name = command.split(" ")
            print(handle_show_number(name))
        elif command == "show all":
            print(handle_show_all())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    address_book = AddressBook()
    main()

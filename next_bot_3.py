import json


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

    def save_to_file(self, filename):
        data = {"contacts": [record.__dict__ for record in self.contacts.values()]}
        with open(filename, "w") as file:
            json.dump(data, file)

    def load_from_file(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            contacts = data.get("contacts", [])
            self.contacts = {
                record["name"]["_value"]: Record.from_dict(record)
                for record in contacts
            }

    def search_by_content(self, search_string):
        matching_records = []
        for record in self.contacts.values():
            if search_string in record.name.value or any(
                search_string in phone.value for phone in record.phones
            ):
                matching_records.append(record)
        return matching_records


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise KeyError("Номер телефону не знайдений.")

    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()
        else:
            return None

    def __str__(self):
        result = f"Name: {self.name.value}\n"
        if self.phones:
            result += "Phones:\n"
            for phone in self.phones:
                result += f"- {phone}\n"
        if self.birthday:
            result += f"Birthday: {self.birthday.value}\n"
        return result

    @classmethod
    def from_dict(cls, data):
        record = cls(data["name"]["_value"], data.get("birthday"))
        for phone_data in data.get("phones", []):
            record.add_phone(Phone(phone_data["_value"]))
        return record


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        if not new_value.isdigit():
            raise ValueError("Номер телефону повинен містити тільки цифри.")
        self._value = new_value


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value):
        self._value = new_value

    def days_to_birthday(self):
        pass


def handle_hello():
    return "How can I help you?"


def handle_add_contact(name, number, birthday=None):
    record = Record(name, birthday)
    record.add_phone(Phone(number))
    address_book.add_record(record)
    return "Контакт успішно доданий!"


def handle_change_number(name, number):
    record = address_book.search_by_name(name)
    record.remove_phone(record.phones[0])  # Видалення номера телефону
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


def handle_save_to_file(filename):
    address_book.save_to_file(filename)
    return "Адресну книгу збережено на диск."


def handle_load_from_file(filename):
    address_book.load_from_file(filename)
    return "Адресну книгу завантажено з диска."


def handle_search_by_content(search_string):
    matching_records = address_book.search_by_content(search_string)
    if matching_records:
        result = "Знайдені контакти:\n"
        for record in matching_records:
            result += f"{record}\n"
        return result
    else:
        return "Не знайдено жодного контакту."


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
        elif command.startswith("save"):
            _, filename = command.split(" ")
            print(handle_save_to_file(filename))
        elif command.startswith("load"):
            _, filename = command.split(" ")
            print(handle_load_from_file(filename))
        elif command.startswith("search"):
            _, search_string = command.split(" ")
            print(handle_search_by_content(search_string))
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    address_book = AddressBook()
    main()

contacts = {}


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдений."
        except ValueError:
            return "Неправильний формат введення."
        except IndexError:
            return "Неправильна команда."

    return wrapper


@input_error
def handle_hello():
    return "How can I help you?"


@input_error
def handle_add_contact(name, number):
    contacts[name] = number
    return "Контакт успішно доданий!"


@input_error
def handle_change_number(name, number):
    contacts[name] = number
    return "Номер телефону змінено!"


@input_error
def handle_show_number(name):
    return contacts[name]


@input_error
def handle_show_all():
    if not contacts:
        return "Список контактів порожній."
    else:
        result = "Список контактів:\n"
        for name, number in contacts.items():
            result += f"{name}: {number}\n"
        return result


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
    main()

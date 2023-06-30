import datetime


class Birthday:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return f"{self.day}/{self.month}/{self.year}"


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, Birthday: {self.birthday}"

    def days_to_birthday(self):
        if self.birthday is None:
            return None
        current_date = datetime.datetime.now().date()
        next_birthday = datetime.date(
            current_date.year, self.birthday.month, self.birthday.day
        )
        if next_birthday < current_date:
            next_birthday = datetime.date(
                current_date.year + 1, self.birthday.month, self.birthday.day
            )
        days_left = (next_birthday - current_date).days
        return days_left


def get_birthdays_per_week(users):
    current_date = datetime.datetime.now().date()
    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())

    days_of_week = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }

    for user in users:
        birthday = user["birthday"].replace(year=current_date.year).date()
        if start_of_week <= birthday <= start_of_week + datetime.timedelta(days=6):
            weekday = days_of_week[birthday.weekday()]
            if weekday == 5 or weekday == 6:
                days_of_week[0].append(user["name"])
            else:
                days_of_week[weekday].append(user["name"])

    for day, users in days_of_week.items():
        if day == 0:
            if users:
                print("Monday:", ", ".join(users))
        else:
            if users:
                print(days_of_week[day] + ":", ", ".join(users))


# Список користувачів
users = [
    {"name": "Bill", "birthday": Birthday(27, 6, 1990)},
    {"name": "Jill", "birthday": Birthday(28, 6, 1992)},
    {"name": "Kim", "birthday": Birthday(30, 6, 1988)},
    {"name": "Jan", "birthday": Birthday(2, 7, 1995)},
]

# Виклик функції для виведення списку ім'янинників
get_birthdays_per_week(users)

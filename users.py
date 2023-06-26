import datetime


def get_birthdays_per_week(users):
    current_date = datetime.datetime.now().date()

    days_of_week = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": [],
    }

    for user in users:
        birthday = user["birthday"].date()
        if (birthday - current_date).days <= 7:
            weekday = birthday.strftime("%A")
            days_of_week[weekday].append(user["name"])

    for day, users in days_of_week.items():
        if day == "Saturday" or day == "Sunday":
            if users:
                print("Monday:", ", ".join(users))
        else:
            if users:
                print(day + ":", ", ".join(users))


# Cписок користувачів
users = [
    {"name": "Bill", "birthday": datetime.datetime(2023, 6, 27)},
    {"name": "Jill", "birthday": datetime.datetime(2023, 6, 28)},
    {"name": "Kim", "birthday": datetime.datetime(2023, 6, 30)},
    {"name": "Jan", "birthday": datetime.datetime(2023, 7, 2)},
]

# Виклик функції для виведення списку ім'янинників
get_birthdays_per_week(users)

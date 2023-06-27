import datetime


def get_birthdays_per_week(users):
    current_date = datetime.datetime.now().date()
    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())

    days_of_week = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }

    for user in users:
        birthday = user["birthday"].date().replace(year=current_date.year)
        if start_of_week <= birthday <= start_of_week + datetime.timedelta(days=6):
            weekday = days_of_week[birthday.weekday()]
            if weekday == "Saturday" or weekday == "Sunday":
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


# Cписок користувачів
users = [
    {"name": "Bill", "birthday": datetime.datetime(1990, 6, 27)},
    {"name": "Jill", "birthday": datetime.datetime(1992, 6, 28)},
    {"name": "Kim", "birthday": datetime.datetime(1988, 6, 30)},
    {"name": "Jan", "birthday": datetime.datetime(1995, 7, 2)},
]

# Виклик функції для виведення списку ім'янинників
get_birthdays_per_week(users)

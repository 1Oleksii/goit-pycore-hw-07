from collections import UserDict
import re
from datetime import datetime, timedelta

# Define the base class for fields
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Create the Name class for storing contact names
class Name(Field):
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        super().__init__(value)

# Create the Phone class for storing phone numbers
class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must consist of 10 digits")
        super().__init__(value)

    def validate_phone(self, phone):
        return isinstance(phone, str) and re.match(r'^\d{10}$', phone) is not None

# Create the Birthday class for storing birthdays
class Birthday(Field):
    def __init__(self, value):
        try:
            # Validate and convert string to datetime object
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

# Modify the Record class to include the birthday field
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        birthday_str = f"Birthday: {self.birthday.value}" if self.birthday else "No birthday set"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, {birthday_str}"

# Modify the AddressBook class to handle birthday logic
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)

                # If the birthday already passed this year, move it to next year 
                if birthday_this_year < today:
                    birthday_this_year = record.birthday.value.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days <= 7:
                    congratulation_date = birthday_this_year

                    # If the birthday is on the weekend (Saturday or Sunday), move to next Monday
                    if congratulation_date.weekday() in [5, 6]:  # Saturday or Sunday
                        shift_days = 7 - congratulation_date.weekday()
                        congratulation_date += timedelta(days=shift_days)

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays


def main():
    book = AddressBook()

    # Creating a record for John with a birthday
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("05.04.1985")
    book.add_record(john_record)

    # Creating a record for Jane with a birthday
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("03.04.1990")
    book.add_record(jane_record)

    # Create and add more records if necessary...

    # Print all contacts in the AddressBook
    for name, record in book.data.items():
        print(record)

    # Find and edit John's phone
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    # Get upcoming birthdays
    upcoming_birthdays = book.get_upcoming_birthdays()

    # Print upcoming birthdays with additional debug output
    print("Upcoming birthdays:", upcoming_birthdays)


if __name__ == "__main__":
    main()

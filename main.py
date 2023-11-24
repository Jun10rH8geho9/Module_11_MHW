from collections import UserDict
from datetime import datetime, timedelta
import re

# Батьківський клас
class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)
    # Клас де зберігаємо ім'я 
class Name(Field):
    pass
    # Клас де зберігаємо номер телефону 
class Phone(Field):
    @Field.value.setter
    def value(self, value):
        # Проходмо валідацію. Якщо  номер не цифри або довжина менше 10
        if not str(value).isdigit() or len(str(value)) != 10:
            raise ValueError("Телефон повинен мати 10 цифр та не мати букв")
        super().value.fset(self, value)

        # Клас для створення дати народження
class Birthday(Field):
        # Перевірка, чи відповідає нове значення формату DD-MM-YYYY
    @Field.value.setter
    def value(self, value):
        if not re.match(r'\d{2}-\d{2}-\d{4}', value):
            raise ValueError("Дата народження повинна бути у форматі DD-MM-YYYY")
        super().value.fset(self, datetime.strptime(value, '%d-%m-%Y'))

    # Метод для обчислення кількості днів до дня народження
    def days_to_birthday(self):
        now = datetime.now()
        next_birthday = datetime(year=now.year, month=self.value.month, day=self.value.day)
        if now > next_birthday:
            next_birthday += timedelta(days=365)
        return (next_birthday - now).days
        # Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів. Відповідає за логіку додавання/видалення/редагування
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        if birthday is not None:
            self.birthday = Birthday(birthday)

        # Додадємо номер
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
        # Знаходимо номер
    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return i
        return None
        
        # Видаляємо номер
    def remove_phone(self, phone):
        self.phones = [i for i in self.phones if i.value != phone]
        
        # Редагуємо номер
    def edit_phone(self, old_phone, new_phone):
        found = False
        for i in self.phones:
            if i.value == old_phone:
                i.value = new_phone
                found = True
        if not found:
            raise ValueError(f"Телефонний номер {old_phone} не знайдено")
        
        # Кількість днів до дня народження
    def days_to_birthday(self):
        if self.birthday is not None:
            return self.birthday.days_to_birthday() 

    def __str__(self):
        return f"Ім'я контакта: {self.name.value}, телефони: {'; '.join(i.value for i in self.phones)}"
    
    # Клас для зберігання та управління записами. Містить логіку пошуку за записами до цього класу
class AddressBook(UserDict):
    # Додадємо номер
    def add_record(self, record):
        self.data[record.name.value] = record

    # Знаходимо номер
    def find(self, name):
        return self.data.get(name, None)
    
    # Видаляємо номер
    def delete(self, name):
        if name in self.data:
            del self.data[name]

     # Метод для ітерації по записам
    def iterator(self, n):
        records = list(self.data.values())
        while records:
            yield records[:n]
            records = records[n:]
    
    # Метод для виведення всіх записів
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())
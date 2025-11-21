import random
from abc import ABC, abstractmethod

# 1. BankAccount
class BankAccount:
    def __init__(self, name, balance, password):
        self.name = name
        self._balance = balance
        self.__password = password

    def deposit(self, amount, password):
        if password == self.__password:
            self._balance += amount
            return self._balance
        return "Неверный пароль!"

    def withdraw(self, amount, password):
        if password != self.__password:
            return "Неверный пароль!"
        if self._balance < amount:
            return "Недостаточно средств!"
        self._balance -= amount
        return self._balance

    def change_password(self, old_password, new_password):
        if old_password == self.__password:
            self.__password = new_password
            return "Пароль изменён"
        return "Старый пароль неверный"

    def get_balance(self, password):
        if password == self.__password:
            return self._balance
        return "Неверный пароль!"

    def reset_pin(self, password):
        if password != self.__password:
            return "Неверный пароль!"
        new_pin = self.__generate_pin()
        self.__password = new_pin
        return new_pin

    def __generate_pin(self):
        return f"{random.randint(0,9999):04d}"

# 2. NotificationSender + наследники
class NotificationSender(ABC):
    @abstractmethod
    def send(self, message, recipient):
        pass

class EmailSender(NotificationSender):
    def __init__(self):
        self._service = "Gmail"
    def send(self, message, recipient):
        return f"Email sent to {recipient}"
    def get_service(self):
        return f"Сервис: {self._service}"

class SmsSender(NotificationSender):
    def __init__(self):
        self._service = "Twilio"
    def send(self, message, recipient):
        return f"SMS sent to {recipient}"
    def get_service(self):
        return f"Сервис: {self._service}"

class PushSender(NotificationSender):
    def __init__(self):
        self._service = "Firebase"
    def send(self, message, recipient):
        return f"Push sent to {recipient}"
    def get_service(self):
        return f"Сервис: {self._service}"

# 3. UserAuth
class UserAuth:
    def __init__(self, username, account: BankAccount, notifier: NotificationSender):
        self.username = username
        self.account = account
        self.notifier = notifier

    def login(self, password):
        if isinstance(self.account.get_balance(password), (int,float)):
            print(self.notifier.send(f"Успешный вход: {self.username}", "system"))
            return True
        return False

    def transfer(self, amount, password, recipient_account: BankAccount):
        withdraw_result = self.account.withdraw(amount, password)
        if isinstance(withdraw_result, str):
            print(withdraw_result)
            return withdraw_result
        recipient_account._balance += amount
        print(self.notifier.send(f"Перевод {amount} отправлен", "system"))
        print(self.notifier.send(f"Получено {amount} от {self.username}", "system"))
        print(f"Перевод успешен. Новый баланс: {self.account._balance}")
        return self.account._balance
    
if __name__ == "__main__":
    print("=== Тест BankAccount ===")
    john = BankAccount("John", 100, "123qwerty")
    print(john.deposit(150, "123qwerty"))
    print(john.withdraw(100, "123qwerty"))
    print(john.get_balance("123qwerty"))
    print(john.change_password("wrong", "newpass"))
    print(john.change_password("123qwerty", "newpass"))
    new_pin = john.reset_pin("newpass")
    print(new_pin)
    print(john.get_balance(new_pin))

    print("\n=== Тест NotificationSender ===")
    email = EmailSender()
    sms = SmsSender()
    push = PushSender()
    print(email.send("Привет", "test@mail.ru"))
    print(email.get_service())
    print(sms.get_service())

    print("\n=== Тест UserAuth ===")
    john_acc = BankAccount("John", 80, "abc123")
    alice_acc = BankAccount("Alice", 50, "pass")
    notifier = SmsSender()
    auth = UserAuth("john_doe", john_acc, notifier)
    auth.login("abc123")
    auth.transfer(70, "abc123", alice_acc)
    print(f"John balance: {john_acc._balance}")
    print(f"Alice balance: {alice_acc._balance}")

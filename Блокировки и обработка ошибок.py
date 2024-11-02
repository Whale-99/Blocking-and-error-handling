import threading
from random import randint
from time import sleep

class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            # Генерация случайного числа для пополнения баланса
            amount = randint(50, 500)
            self.balance += amount
            print(f"Пополнение: {amount}. Баланс: {self.balance}")

            # Проверка на разблокировку, если баланс больше или равен 500
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()

            # Задержка на 0.001 секунды
            sleep(0.001)

    def take(self):
        for _ in range(100):
            # Генерация случайного числа для снятия средств
            amount = randint(50, 500)
            print(f"Запрос на {amount}")

            # Проверка возможности снятия средств
            if amount <= self.balance:
                self.balance -= amount
                print(f"Снятие: {amount}. Баланс: {self.balance}")
            else:
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()

            # Задержка на 0.001 секунды
            sleep(0.001)

# Создание объекта класса Bank
bk = Bank()

# Создание и запуск потоков для методов deposit и take
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

# Ожидание завершения потоков
th1.join()
th2.join()

# Итоговый баланс
print(f'Итоговый баланс: {bk.balance}')

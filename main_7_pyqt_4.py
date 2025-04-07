import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout
)


class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Трекер трат")
        self.setGeometry(100, 100, 800, 600)

        # Основной контейнер
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Поля ввода данных
        self.days_label = QLabel("Введите количество дней:")
        self.days_input = QLineEdit()
        self.total_expense_label = QLabel("Введите общую сумму трат:")
        self.total_expense_input = QLineEdit()

        # Кнопка для начала расчетов
        self.start_button = QPushButton("Начать отслеживание")
        self.start_button.clicked.connect(self.start_tracking)

        # Таблица для вывода статистики
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["День", "Трата"])

        # Элементы для ввода текущих трат
        self.current_expense_label = QLabel("Текущая трата:")
        self.current_expense_input = QLineEdit()
        self.current_expense_input.setPlaceholderText("Введите текущую трату")
        self.add_expense_button = QPushButton("Добавить трату")
        self.finish_day_button = QPushButton("Завершить день")
        self.info_label = QLabel("Ожидание ввода...")

        # Добавление элементов в макет
        self.layout.addWidget(self.days_label)
        self.layout.addWidget(self.days_input)
        self.layout.addWidget(self.total_expense_label)
        self.layout.addWidget(self.total_expense_input)
        self.layout.addWidget(self.start_button)

        # Горизонтальный макет для кнопок и ввода текущих трат
        self.expense_layout = QHBoxLayout()
        self.expense_layout.addWidget(self.current_expense_label)
        self.expense_layout.addWidget(self.current_expense_input)
        self.expense_layout.addWidget(self.add_expense_button)
        self.expense_layout.addWidget(self.finish_day_button)
        self.layout.addLayout(self.expense_layout)

        # Информационная метка
        self.layout.addWidget(self.info_label)

        # Таблица статистики
        self.layout.addWidget(self.table)

        self.central_widget.setLayout(self.layout)

        # Переменные для хранения данных
        self.days = 0
        self.total_expense = 0
        self.daily_expenses_actual = []
        self.remaining_total = 0
        self.remaining_days = 0
        self.daily_expense = 0
        self.current_day = 1
        self.accumulated_expense_for_day = 0

        # Начальные состояния кнопок
        self.add_expense_button.setEnabled(False)
        self.finish_day_button.setEnabled(False)

    def start_tracking(self):
        try:
            # Получение данных из полей ввода
            self.days = int(self.days_input.text())
            self.total_expense = float(self.total_expense_input.text())

            if self.days <= 0 or self.total_expense < 0:
                self.info_label.setText("Ошибка: Количество дней должно быть положительным числом, а сумма трат — неотрицательной.")
                return

            # Инициализация переменных
            self.remaining_total = self.total_expense
            self.remaining_days = self.days
            self.daily_expense = self.total_expense / self.days
            self.daily_expenses_actual = []
            self.current_day = 1
            self.accumulated_expense_for_day = 0

            # Включение кнопок
            self.add_expense_button.setEnabled(True)
            self.finish_day_button.setEnabled(True)

            # Обновление информации
            self.update_info()

        except ValueError:
            self.info_label.setText("Ошибка: Введите корректные числовые значения.")

    def update_info(self):
        # Обновление информационной метки
        remaining_for_day = self.daily_expense - self.accumulated_expense_for_day
        self.info_label.setText(
            f"День {self.current_day}:\n"
            f"Планируемая трата: {self.daily_expense:.2f}\n"
            f"Остаток на текущий день: {remaining_for_day:.2f}\n"
            f"Общий остаток: {self.remaining_total:.2f}"
        )

    def add_current_expense(self):
        try:
            current_expense = float(self.current_expense_input.text())
            if current_expense < 0:
                self.info_label.setText("Ошибка: Текущая трата не может быть отрицательной.")
                return

            # Добавляем текущую трату к накопленным тратам дня
            self.accumulated_expense_for_day += current_expense
            self.remaining_total -= current_expense
            self.current_expense_input.clear()

            # Обновляем информацию
            self.update_info()

            # Проверка на превышение общей суммы трат
            if self.remaining_total <= 0:
                self.info_label.setText("Внимание: Все деньги потрачены!")

            # Если остаток на день меньше нуля, предупреждение
            remaining_for_day = self.daily_expense - self.accumulated_expense_for_day
            if remaining_for_day < 0:
                self.info_label.setText("Внимание: Вы превысили планируемую трата на текущий день!")

        except ValueError:
            self.info_label.setText("Ошибка: Введите корректное числовое значение.")

    def finish_current_day(self):
        # Сохраняем фактическую трату за день
        self.daily_expenses_actual.append(self.accumulated_expense_for_day)

        # Обновляем таблицу статистики
        self.show_statistics()

        # Переход к следующему дню
        self.remaining_days -= 1
        if self.remaining_days > 0 and self.remaining_total > 0:
            self.daily_expense = self.remaining_total / self.remaining_days
            self.current_day += 1
            self.accumulated_expense_for_day = 0
            self.update_info()
        else:
            self.info_label.setText("Все дни завершены!")
            self.add_expense_button.setEnabled(False)
            self.finish_day_button.setEnabled(False)

    def show_statistics(self):
        # Очистка таблицы
        self.table.setRowCount(len(self.daily_expenses_actual))

        total_spent = 0
        for row, expense in enumerate(self.daily_expenses_actual):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.table.setItem(row, 1, QTableWidgetItem(f"{expense:.2f}"))
            total_spent += expense

        # Добавление строки с итоговой суммой
        self.table.insertRow(len(self.daily_expenses_actual))
        self.table.setItem(len(self.daily_expenses_actual), 0, QTableWidgetItem("Итого:"))
        self.table.setItem(len(self.daily_expenses_actual), 1, QTableWidgetItem(f"{total_spent:.2f}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()

    # Привязка кнопок к методам
    window.add_expense_button.clicked.connect(window.add_current_expense)
    window.finish_day_button.clicked.connect(window.finish_current_day)

    window.show()
    sys.exit(app.exec_())
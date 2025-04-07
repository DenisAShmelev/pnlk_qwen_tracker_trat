import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
)


class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Трекер трат")
        self.setGeometry(100, 100, 600, 400)

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

        # Добавление элементов в макет
        self.layout.addWidget(self.days_label)
        self.layout.addWidget(self.days_input)
        self.layout.addWidget(self.total_expense_label)
        self.layout.addWidget(self.total_expense_input)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.table)

        self.central_widget.setLayout(self.layout)

        # Переменные для хранения данных
        self.days = 0
        self.total_expense = 0
        self.daily_expenses_actual = []

    def start_tracking(self):
        try:
            # Получение данных из полей ввода
            self.days = int(self.days_input.text())
            self.total_expense = float(self.total_expense_input.text())

            if self.days <= 0 or self.total_expense < 0:
                QMessageBox.warning(self, "Ошибка", "Количество дней должно быть положительным числом, а сумма трат — неотрицательной.")
                return

            # Инициализация переменных
            self.remaining_total = self.total_expense
            self.remaining_days = self.days
            self.daily_expense = self.total_expense / self.days
            self.daily_expenses_actual = []

            # Запуск процесса отслеживания
            self.track_day(1)

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения.")

    def track_day(self, day):
        if day > self.days:
            self.show_statistics()
            return

        # Создание диалогового окна для ввода текущих трат
        dialog = DayExpenseDialog(day, self.daily_expense, self.remaining_total, self)
        if dialog.exec_():
            accumulated_expense_for_day = dialog.get_accumulated_expense()
            self.remaining_total -= accumulated_expense_for_day
            self.remaining_days -= 1

            # Сохранение фактической траты за день
            self.daily_expenses_actual.append(accumulated_expense_for_day)

            # Пересчет планируемой траты на оставшиеся дни
            if self.remaining_days > 0 and self.remaining_total > 0:
                self.daily_expense = self.remaining_total / self.remaining_days

            # Переход к следующему дню
            self.track_day(day + 1)

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


class DayExpenseDialog(QMessageBox):
    def __init__(self, day, daily_expense, remaining_total, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"День {day}")
        self.setText(f"Планируемая трата: {daily_expense:.2f}\nОбщий остаток: {remaining_total:.2f}")

        # Сохраняем планируемую трату для вычисления остатка
        self.daily_expense = daily_expense

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Введите текущую трату")
        self.layout().addWidget(self.input)

        self.addButton("Добавить", QMessageBox.AcceptRole)
        self.addButton("Завершить день", QMessageBox.RejectRole)

        self.accumulated_expense = 0

    def exec_(self):
        while True:
            result = super().exec_()
            if result == QMessageBox.RejectRole:
                return True

            try:
                current_expense = float(self.input.text())
                if current_expense < 0:
                    QMessageBox.warning(self, "Ошибка", "Текущая трата не может быть отрицательной.")
                    continue

                self.accumulated_expense += current_expense
                self.input.clear()

                # Вычисляем остаток на текущий день
                remaining_for_day = self.daily_expense - self.accumulated_expense
                QMessageBox.information(self, "Остаток", f"Остаток на текущий день: {remaining_for_day:.2f}")

                # Если превышена планируемая трата, показываем предупреждение
                if remaining_for_day < 0:
                    QMessageBox.warning(self, "Внимание", "Вы превысили планируемую трата на текущий день!")

            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Введите корректное числовое значение.")

    def get_accumulated_expense(self):
        return self.accumulated_expense


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec_())
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class ExpenseTracker(toga.App):
    def startup(self):
        # Основной контейнер
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Поля ввода данных
        self.days_label = toga.Label("Введите количество дней:", style=Pack(padding=(0, 0, 5, 0)))
        self.days_input = toga.TextInput(style=Pack(flex=1))
        days_box = toga.Box(children=[self.days_label, self.days_input], style=Pack(direction=ROW, padding=5))

        self.total_expense_label = toga.Label("Введите общую сумму трат:", style=Pack(padding=(0, 0, 5, 0)))
        self.total_expense_input = toga.TextInput(style=Pack(flex=1))
        total_expense_box = toga.Box(children=[self.total_expense_label, self.total_expense_input], style=Pack(direction=ROW, padding=5))

        # Кнопка для начала расчетов
        self.start_button = toga.Button("Начать отслеживание", on_press=self.start_tracking, style=Pack(padding=10))

        # Таблица для вывода статистики
        self.table = toga.Table(headings=["День", "Трата"], style=Pack(flex=1, padding=10))

        # Элементы для ввода текущих трат
        self.current_expense_label = toga.Label("Текущая трата:", style=Pack(padding=(0, 0, 5, 0)))
        self.current_expense_input = toga.TextInput(placeholder="Введите текущую трату", style=Pack(flex=1))
        self.add_expense_button = toga.Button("Добавить трату", on_press=self.add_current_expense, style=Pack(padding=5))
        self.finish_day_button = toga.Button("Завершить день", on_press=self.finish_current_day, style=Pack(padding=5))

        expense_buttons_box = toga.Box(
            children=[self.current_expense_label, self.current_expense_input, self.add_expense_button, self.finish_day_button],
            style=Pack(direction=ROW, padding=5)
        )

        # Информационная метка
        self.info_label = toga.Label("Ожидание ввода...", style=Pack(padding=(10, 0, 0, 0)))

        # Добавление элементов в макет
        main_box.add(days_box)
        main_box.add(total_expense_box)
        main_box.add(self.start_button)
        main_box.add(expense_buttons_box)
        main_box.add(self.info_label)
        main_box.add(self.table)

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
        self.add_expense_button.enabled = False
        self.finish_day_button.enabled = False

        # Главное окно
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def start_tracking(self, widget):
        try:
            # Получение данных из полей ввода
            self.days = int(self.days_input.value)
            self.total_expense = float(self.total_expense_input.value)

            if self.days <= 0 or self.total_expense < 0:
                self.info_label.text = "Ошибка: Количество дней должно быть положительным числом, а сумма трат — неотрицательной."
                return

            # Инициализация переменных
            self.remaining_total = self.total_expense
            self.remaining_days = self.days
            self.daily_expense = self.total_expense / self.days
            self.daily_expenses_actual = []
            self.current_day = 1
            self.accumulated_expense_for_day = 0

            # Включение кнопок
            self.add_expense_button.enabled = True
            self.finish_day_button.enabled = True

            # Обновление информации
            self.update_info()

        except ValueError:
            self.info_label.text = "Ошибка: Введите корректные числовые значения."

    def update_info(self):
        # Обновление информационной метки
        remaining_for_day = self.daily_expense - self.accumulated_expense_for_day
        self.info_label.text = (
            f"День {self.current_day}:\n"
            f"Планируемая трата: {self.daily_expense:.2f}\n"
            f"Остаток на текущий день: {remaining_for_day:.2f}\n"
            f"Общий остаток: {self.remaining_total:.2f}"
        )

    def add_current_expense(self, widget):
        try:
            current_expense = float(self.current_expense_input.value)
            if current_expense < 0:
                self.info_label.text = "Ошибка: Текущая трата не может быть отрицательной."
                return

            # Добавляем текущую трату к накопленным тратам дня
            self.accumulated_expense_for_day += current_expense
            self.remaining_total -= current_expense
            self.current_expense_input.clear()

            # Обновляем информацию
            self.update_info()

            # Проверка на превышение общей суммы трат
            if self.remaining_total <= 0:
                self.info_label.text = "Внимание: Все деньги потрачены!"

            # Если остаток на день меньше нуля, предупреждение
            remaining_for_day = self.daily_expense - self.accumulated_expense_for_day
            if remaining_for_day < 0:
                self.info_label.text = "Внимание: Вы превысили планируемую трата на текущий день!"

        except ValueError:
            self.info_label.text = "Ошибка: Введите корректное числовое значение."

    def finish_current_day(self, widget):
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
            self.info_label.text = "Все дни завершены!"
            self.add_expense_button.enabled = False
            self.finish_day_button.enabled = False

    def show_statistics(self):
        # Очистка таблицы
        self.table.data.clear()

        total_spent = 0
        for day, expense in enumerate(self.daily_expenses_actual, start=1):
            self.table.data.append([str(day), f"{expense:.2f}"])
            total_spent += expense

        # Добавление строки с итоговой суммой
        self.table.data.append(["Итого:", f"{total_spent:.2f}"])


def main():
    return ExpenseTracker("Трекер трат", "org.example.expensetracker")


if __name__ == "__main__":
    app = main()
    app.main_loop()
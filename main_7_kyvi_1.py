from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

# Основной класс приложения
class ExpenseTrackerApp(App):
    def build(self):
        self.title = "Трекер трат"
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Ввод количества дней
        self.days_input = TextInput(hint_text="Введите количество дней", multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(Label(text="Количество дней:"))
        self.layout.add_widget(self.days_input)
        
        # Ввод общей суммы трат
        self.total_expense_input = TextInput(hint_text="Введите общую сумму трат", multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(Label(text="Общая сумма трат:"))
        self.layout.add_widget(self.total_expense_input)
        
        # Кнопка для начала расчета
        self.start_button = Button(text="Начать расчет", size_hint_y=None, height=50)
        self.start_button.bind(on_press=self.start_calculation)
        self.layout.add_widget(self.start_button)
        
        # Область для вывода результатов
        self.result_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))
        self.scroll_view = ScrollView(size_hint=(1, 0.6))
        self.scroll_view.add_widget(self.result_layout)
        self.layout.add_widget(self.scroll_view)
        
        return self.layout

    def start_calculation(self, instance):
        try:
            # Очистка предыдущих результатов
            self.result_layout.clear_widgets()
            
            # Получение входных данных
            days = int(self.days_input.text)
            total_expense = float(self.total_expense_input.text)
            
            if days <= 0 or total_expense < 0:
                self.result_layout.add_widget(Label(text="Ошибка: Количество дней должно быть положительным, а сумма трат — неотрицательной."))
                return
            
            # Расчет планируемой траты на каждый день
            daily_expense = total_expense / days
            remaining_total = total_expense
            remaining_days = days
            daily_expenses_actual = []
            
            for day in range(1, days + 1):
                self.result_layout.add_widget(Label(text=f"День {day}: Планируемая трата - {daily_expense:.2f}"))
                
                accumulated_expense_for_day = 0
                
                while True:
                    # Ввод текущей траты через диалоговое окно
                    current_expense = self.show_input_dialog(f"Введите текущую трату для дня {day} (или 'end' для завершения):")
                    
                    if current_expense.lower() == 'end':
                        break
                    
                    current_expense = float(current_expense)
                    if current_expense < 0:
                        self.result_layout.add_widget(Label(text="Ошибка: Текущая трата не может быть отрицательной."))
                        continue
                    
                    # Добавляем текущую трату к накопленным тратам дня
                    accumulated_expense_for_day += current_expense
                    remaining_total -= current_expense
                    
                    # Вычисление остатка на текущий день
                    remaining_for_day = daily_expense - accumulated_expense_for_day
                    
                    self.result_layout.add_widget(Label(text=f"Остаток на текущий день: {remaining_for_day:.2f}"))
                    self.result_layout.add_widget(Label(text=f"Общий остаток на все дни: {remaining_total:.2f}"))
                    
                    if remaining_for_day < 0:
                        self.result_layout.add_widget(Label(text="Внимание: Вы превысили планируемую трата на текущий день!"))
                    
                    if remaining_total <= 0:
                        self.result_layout.add_widget(Label(text="Внимание: Все деньги потрачены!"))
                        break
                
                # Сохраняем фактическую трату за день
                daily_expenses_actual.append(accumulated_expense_for_day)
                
                # Пересчет планируемой суммы на оставшиеся дни
                remaining_days -= 1
                if remaining_days > 0 and remaining_total > 0:
                    daily_expense = remaining_total / remaining_days
                    self.result_layout.add_widget(Label(text=f"Новая планируемая трата на следующие дни: {daily_expense:.2f}"))
                else:
                    if remaining_days > 0:
                        self.result_layout.add_widget(Label(text="Планируемая трата на следующие дни: 0.00 (нет оставшихся средств)."))
                    else:
                        self.result_layout.add_widget(Label(text="Это был последний день. Больше дней для перерасчета нет."))
            
            # Вывод статистики
            self.result_layout.add_widget(Label(text="\n--- Статистика трат ---"))
            self.result_layout.add_widget(Label(text=f"{'День':<10}{'Трата':<15}"))
            self.result_layout.add_widget(Label(text="-" * 25))
            
            total_spent = 0
            for day, expense in enumerate(daily_expenses_actual, start=1):
                self.result_layout.add_widget(Label(text=f"{day:<10}{expense:.2f}"))
                total_spent += expense
            
            self.result_layout.add_widget(Label(text="-" * 25))
            self.result_layout.add_widget(Label(text=f"Итого потрачено: {total_spent:.2f}"))
        
        except ValueError:
            self.result_layout.add_widget(Label(text="Ошибка: Введите корректные числовые значения."))

    def show_input_dialog(self, message):
        """Функция для отображения диалогового окна ввода."""
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        
        content = BoxLayout(orientation='vertical', spacing=10)
        input_field = TextInput(multiline=False)
        button = Button(text="OK", size_hint=(1, 0.5))
        popup = Popup(title=message, content=content, size_hint=(0.8, 0.4))
        
        def on_button_press(instance):
            popup.dismiss()
        
        button.bind(on_press=on_button_press)
        content.add_widget(input_field)
        content.add_widget(button)
        
        popup.open()
        popup.bind(on_dismiss=lambda _: setattr(self, 'user_input', input_field.text))
        return self.user_input


if __name__ == "__main__":
    Window.size = (400, 600)  # Установка размера окна
    ExpenseTrackerApp().run()
def main():
    # Ввод данных от пользователя
    try:
        days = int(input("Введите количество дней: "))
        total_expense = float(input("Введите общую сумму трат: "))
        
        if days <= 0 or total_expense < 0:
            print("Количество дней должно быть положительным числом, а сумма трат — неотрицательной.")
            return
        
        # Расчет планируемой траты на каждый день
        daily_expense = total_expense / days
        remaining_total = total_expense  # Оставшаяся сумма трат
        remaining_days = days  # Оставшиеся дни
        
        # Список для хранения трат по дням
        daily_expenses_actual = []
        
        for day in range(1, days + 1):
            print(f"\nДень {day}: Планируемая трата - {daily_expense:.2f}")
            
            # Накопленные траты для текущего дня
            accumulated_expense_for_day = 0
            
            # Цикл для ввода текущих трат
            while True:
                try:
                    current_expense = input("Введите текущую трату (или 'end' для завершения дня): ")
                    
                    if current_expense.lower() == 'end':
                        break
                    
                    current_expense = float(current_expense)
                    if current_expense < 0:
                        print("Текущая трата не может быть отрицательной. Попробуйте снова.")
                        continue
                    
                    # Добавляем текущую трату к накопленным тратам дня
                    accumulated_expense_for_day += current_expense
                    remaining_total -= current_expense
                    
                    # Проверка на превышение общей суммы трат
                    if remaining_total <= 0:
                        print("\nВнимание: Все деньги потрачены!")
                    
                    # Вычисление остатка на текущий день
                    remaining_for_day = daily_expense - accumulated_expense_for_day
                    
                    print(f"Остаток на текущий день: {remaining_for_day:.2f}")
                    print(f"Общий остаток на все дни: {remaining_total:.2f}")
                    
                    # Если остаток на день меньше нуля, предупреждение
                    if remaining_for_day < 0:
                        print("Внимание: Вы превысили планируемую трата на текущий день!")
                
                except ValueError:
                    print("Ошибка: Введите корректное числовое значение или 'end'.")
            
            # Сохраняем фактическую трату за день
            daily_expenses_actual.append(accumulated_expense_for_day)
            
            # После завершения дня пересчитываем планируемую сумму на оставшиеся дни
            remaining_days -= 1  # Уменьшаем количество оставшихся дней
            if remaining_days > 0 and remaining_total > 0:
                daily_expense = remaining_total / remaining_days
                print(f"\nНовая планируемая трата на следующие дни: {daily_expense:.2f}")
            else:
                if remaining_days > 0:
                    print("\nПланируемая трата на следующие дни: 0.00 (нет оставшихся средств).")
                else:
                    print("\nЭто был последний день. Больше дней для перерасчета нет.")
        
        # Вывод статистики
        print("\n--- Статистика трат ---")
        print(f"{'День':<10}{'Трата':<15}")
        print("-" * 25)
        
        total_spent = 0
        for day, expense in enumerate(daily_expenses_actual, start=1):
            print(f"{day:<10}{expense:.2f}")
            total_spent += expense
        
        print("-" * 25)
        print(f"Итого потрачено: {total_spent:.2f}")
    
    except ValueError:
        print("Ошибка: Введите корректные числовые значения.")

if __name__ == "__main__":
    main()
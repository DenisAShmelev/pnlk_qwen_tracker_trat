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
                        return
                    
                    # Вычисление остатка на текущий день
                    remaining_for_day = daily_expense - accumulated_expense_for_day
                    
                    print(f"Остаток на текущий день: {remaining_for_day:.2f}")
                    print(f"Общий остаток на все дни: {remaining_total:.2f}")
                    
                    # Если остаток на день меньше нуля, предупреждение
                    if remaining_for_day < 0:
                        print("Внимание: Вы превысили планируемую трата на текущий день!")
                
                except ValueError:
                    print("Ошибка: Введите корректное числовое значение или 'end'.")
            
            # После завершения дня пересчитываем планируемую сумму на оставшиеся дни
            remaining_days -= 1  # Уменьшаем количество оставшихся дней
            if remaining_days > 0:
                daily_expense = remaining_total / remaining_days
                print(f"\nНовая планируемая трата на следующие дни: {daily_expense:.2f}")
            else:
                print("\nЭто был последний день. Больше дней для перерасчета нет.")
    
    except ValueError:
        print("Ошибка: Введите корректные числовые значения.")

if __name__ == "__main__":
    main()